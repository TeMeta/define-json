#!/usr/bin/env python3
"""
Topic Detector - Standalone Version

Provides topic detection functionality for analyzing dataset structures
and identifying observation topics, key dimensions, and data patterns.

Self-contained with local variable_classifier dependency only.
"""

import logging
import pandas as pd
import re
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# Import local CDISC Variable Classifier
try:
    from .variable_classifier import CDISCVariableClassifier, CDISCVariableType
    VARIABLE_CLASSIFIER_AVAILABLE = True
except ImportError:
    try:
        from variable_classifier import CDISCVariableClassifier, CDISCVariableType
        VARIABLE_CLASSIFIER_AVAILABLE = True
    except ImportError:
        logger.warning("CDISC Variable Classifier not available - using fallback patterns")
        VARIABLE_CLASSIFIER_AVAILABLE = False


class StructureType(Enum):
    """Types of dataset structures that can be detected."""
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    UNKNOWN = "unknown"


@dataclass
class TopicInfo:
    """Information about a detected topic."""
    topic_name: str
    topic_id: str = ""
    topic_values: List[str] = field(default_factory=list)
    source_column: Optional[str] = None
    concept_hints: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def __post_init__(self):
        if not self.topic_id:
            self.topic_id = f"TOPIC_{self.topic_name.upper().replace(' ', '_')}"


@dataclass
class DatasetStructure:
    """Information about the structure of a dataset."""
    structure_type: StructureType
    key_dimensions: List[str] = field(default_factory=list)
    measure_columns: List[str] = field(default_factory=list)
    attribute_columns: List[str] = field(default_factory=list)
    topic_dimension: Optional[str] = None
    topics: List[TopicInfo] = field(default_factory=list)


class TopicDetector:
    """
    Detects topics and structure in datasets - Standalone Version.
    
    Analyzes datasets to identify:
    - Dataset structure type (vertical vs horizontal)
    - Key dimensions (study, subject, time)
    - Observation topics
    - Measure and attribute columns
    """
    
    def __init__(self):
        """Initialize the topic detector."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize CDISC Variable Classifier for motivated reasoning
        if VARIABLE_CLASSIFIER_AVAILABLE:
            self.variable_classifier = CDISCVariableClassifier()
            self.logger.info("✅ Using CDISC Variable Classifier for motivated topic detection")
        else:
            self.variable_classifier = None
            self.logger.warning("⚠️ CDISC Variable Classifier not available - using fallback patterns")
        
        # Standard key dimension patterns
        self.key_dimension_patterns = {
            'study': ['studyid', 'study_id', 'study'],
            'subject': ['usubjid', 'subjectid', 'subject_id', 'subject'],
            'time': ['visitnum', 'visit', 'visit_id', 'timepoint', 'time'],
            'sequence': ['seq', 'sequence', 'seqnum']
        }
        
        # Topic dimension patterns (enhanced for CDISC)
        self.topic_dimension_patterns = {
            'test': ['testcd', 'test', 'test_code', 'testname'],
            'term': ['term', 'termcd', 'term_code', 'termname', 'decod'],
            'event': ['event', 'eventcd', 'event_code', 'eventname'],
            'param': ['paramcd', 'param', 'parameter'],
            'treatment': ['trt', 'treatment']
        }
        
        # Enhanced CDISC domain-specific patterns
        self.cdisc_topic_patterns = {
            'testcd_suffix': re.compile(r'(\w{2})TESTCD$'),  # VS|LB|EG|PE|QS|PC + TESTCD
            'paramcd': re.compile(r'PARAMCD$'),              # ADaM parameter code
            'term_suffix': re.compile(r'(\w{2})(TERM|DECOD)$'),  # AETERM, AEDECOD, etc.
            'treatment_suffix': re.compile(r'(\w{2})TRT$'),  # CMTRT, EXTRT, etc.
        }
        
        # Measure column patterns
        self.measure_patterns = ['orres', 'stresn', 'stresc', 'stresu', 'orresu',  # SDTM result/unit columns
                                'aval', 'avalc', 'chg', 'pchg', 'base', 'bnrind',  # ADaM analysis values  
                                'result', 'value', 'finding', 'measurement', 'score', 'rating',
                                'dose', 'concentration', 'level', 'count', 'volume', 'duration']
        
        # Attribute column patterns
        self.attribute_patterns = ['unit', 'method', 'position', 'category', 'severity', 'outcome']
        
        # Metadata/Administrative columns that should NOT be topics (unmotivated)
        self.metadata_patterns = [
            'description', 'label', 'notes', 'comment', 'comments', 'derivation', 
            'origin', 'type', 'role', 'format', 'method', 'status', 'predecessor',
            'qualifier', 'controlled_terms', 'sas_data_type', 'define_xml_data_type', 
            'codelist', 'variable', 'variable_name', 'used_in', 'parent_domain'
        ]
        
        # Clinical topic patterns that ARE motivated to be topics (CONTEXT/DIMENSIONS)
        self.clinical_topic_patterns = [
            # Subject-level characteristics (demographic contexts)
            'age', 'sex', 'race', 'height', 'weight', 'bmi',
            # Clinical contexts (what is being assessed)
            'hemoglobin', 'glucose', 'creatinine', 'albumin', 'bilirubin', 'cholesterol',
            'triglyceride', 'protein', 'sodium', 'potassium', 'chloride', 'hematocrit',
            'temperature', 'pulse', 'systolic', 'diastolic', 'blood_pressure', 'heart_rate',
            'respiration', 'oxygen',
            # Assessment contexts (what scale/test is being used)
            'scale', 'assessment', 'questionnaire', 'inventory', 'endpoint'
        ]
    
    def analyze_structure(self, df: pd.DataFrame) -> DatasetStructure:
        """
        Analyze the structure of a dataset.
        
        Args:
            df: Input dataset as pandas DataFrame
            
        Returns:
            DatasetStructure with detected structure information
        """
        self.logger.info(f"Analyzing structure for dataset with {len(df)} rows and {len(df.columns)} columns")
        
        # Detect structure type
        structure_type = self._detect_structure_type(df)
        
        # Identify key dimensions
        key_dimensions = self._identify_key_dimensions(df)
        
        # Identify topic dimension and topics
        topic_dimension, topics = self._identify_topics(df)
        
        # Identify measure and attribute columns
        measure_columns = self._identify_measure_columns(df)
        attribute_columns = self._identify_attribute_columns(df)
        
        structure = DatasetStructure(
            structure_type=structure_type,
            key_dimensions=key_dimensions,
            measure_columns=measure_columns,
            attribute_columns=attribute_columns,
            topic_dimension=topic_dimension,
            topics=topics
        )
        
        self.logger.info(f"Detected {structure_type.value} structure with {len(topics)} topics")
        return structure
    
    def _detect_structure_type(self, df: pd.DataFrame) -> StructureType:
        """
        Detect whether the dataset has vertical or horizontal structure.
        
        VERTICAL: Has a clear topic dimension column (like TESTCD, PARAMCD) that defines what is being measured
        HORIZONTAL: Each column represents a different attribute/observation type
        """
        if self.variable_classifier:
            # Use CDISC Variable Classifier for precise structure detection
            classifications = self.variable_classifier.classify_dataset_columns(df)
            
            # Look for TOPIC variables that could serve as topic dimensions
            topic_columns = [
                col for col, classification in classifications.items()
                if classification.variable_type == CDISCVariableType.TOPIC
            ]
            
            # Check if any topic column has repeated values AND represents a true topic dimension
            for col in topic_columns:
                if col in df.columns:
                    unique_ratio = len(df[col].unique()) / len(df) if len(df) > 0 else 0
                    unique_count = len(df[col].unique())
                    
                    # True topic dimensions have:
                    # 1. Low uniqueness (repeated values across rows)
                    # 2. Multiple distinct values (not just 2-3 categories like SEX)
                    # 3. Names that suggest they define "what" is being measured
                    is_true_topic_dimension = (
                        unique_ratio < 0.8 and  # Repeated values
                        unique_count >= 3 and   # More than just binary/ternary categories  
                        ('testcd' in col.lower() or 'paramcd' in col.lower() or 'decod' in col.lower())
                    )
                    
                    if is_true_topic_dimension:
                        self.logger.debug(f"Vertical structure detected: '{col}' is true topic dimension (uniqueness: {unique_ratio:.2f}, count: {unique_count})")
                        return StructureType.VERTICAL
            
            # If all topic columns are mostly unique, it's likely horizontal
            if topic_columns:
                self.logger.debug(f"Horizontal structure detected: Topic columns {topic_columns} are mostly unique")
                return StructureType.HORIZONTAL
            
            # No topic columns found - likely horizontal demographics/events
            return StructureType.HORIZONTAL
            
        else:
            # Fallback to pattern-based detection
            columns_lower = [col.lower() for col in df.columns]
            
            # Check for traditional vertical structure indicators (findings domains)
            vertical_indicators = [
                any('testcd' in col for col in columns_lower),
                any('termcd' in col for col in columns_lower),
                any('paramcd' in col for col in columns_lower),
            ]
            
            # Strong vertical indicators (if present with repeated values)
            for indicator_pattern in ['testcd', 'termcd', 'paramcd']:
                matching_cols = [col for col in df.columns if indicator_pattern in col.lower()]
                for col in matching_cols:
                    unique_ratio = len(df[col].unique()) / len(df) if len(df) > 0 else 0
                    if unique_ratio < 0.8:  # Repeated values suggest topic dimension
                        return StructureType.VERTICAL
            
            if any(vertical_indicators):
                return StructureType.VERTICAL
            
            # Default to horizontal for demographics, events, etc.
            return StructureType.HORIZONTAL
    
    def _identify_key_dimensions(self, df: pd.DataFrame) -> List[str]:
        """Identify key dimensions in the dataset."""
        key_dimensions = []
        columns_lower = [col.lower() for col in df.columns]
        
        for dimension_type, patterns in self.key_dimension_patterns.items():
            for pattern in patterns:
                if any(pattern in col for col in columns_lower):
                    # Find the actual column name
                    for col in df.columns:
                        if pattern in col.lower():
                            key_dimensions.append(col)
                            break
                    break
        
        return key_dimensions
    
    def _has_motivated_reason_to_be_topic(self, col_name: str, df: pd.DataFrame) -> bool:
        """
        Determine if a column has motivated clinical reason to be a topic.
        
        Uses CDISC Variable Type Classification for precise, standards-based reasoning.
        Only variables classified as TOPIC type become topics (contexts/dimensions).
        """
        if self.variable_classifier:
            # Use CDISC Variable Classifier for motivated reasoning
            classification = self.variable_classifier.classify_variable(
                variable_name=col_name,
                data=df[col_name],
                context_columns=list(df.columns)
            )
            
            is_topic = classification.variable_type == CDISCVariableType.TOPIC
            
            if is_topic:
                self.logger.debug(f"Column '{col_name}' motivated as topic: {classification.reason}")
            else:
                self.logger.debug(f"Column '{col_name}' not a topic: {classification.variable_type.value} - {classification.reason}")
            
            return is_topic
        else:
            # Fallback to pattern-based approach
            col_lower = col_name.lower()
            
            # Rule 1: Explicitly exclude metadata/administrative columns
            for metadata_pattern in self.metadata_patterns:
                if metadata_pattern in col_lower:
                    self.logger.debug(f"Column '{col_name}' excluded: metadata pattern '{metadata_pattern}'")
                    return False
            
            # Rule 2: Explicitly exclude MEASURE columns (these are values, not contexts)
            for measure_pattern in self.measure_patterns:
                if measure_pattern in col_lower:
                    self.logger.debug(f"Column '{col_name}' excluded: measure pattern '{measure_pattern}' (values, not context)")
                    return False
            
            # Rule 3: Strong clinical indicators (definitely topics/contexts)
            for clinical_pattern in self.clinical_topic_patterns:
                if clinical_pattern in col_lower:
                    self.logger.debug(f"Column '{col_name}' motivated as topic: clinical pattern '{clinical_pattern}'")
                    return True
            
            # Rule 4: CDISC domain-specific topic indicators (contexts like TESTCD, PARAMCD)
            if self._is_cdisc_clinical_variable(col_name):
                self.logger.debug(f"Column '{col_name}' motivated as topic: CDISC clinical variable")
                return True
            
            # Rule 5: Numeric columns with clinical-sounding names (likely demographic contexts)
            if self._appears_to_be_measurement(col_name, df):
                self.logger.debug(f"Column '{col_name}' motivated as topic: appears to be measurement context")
                return True
            
            # Rule 6: Default to NOT a topic (conservative approach)
            self.logger.debug(f"Column '{col_name}' not motivated as topic: no compelling reason found")
            return False
    
    def _is_cdisc_clinical_variable(self, col_name: str) -> bool:
        """Check if column name matches CDISC clinical variable patterns for CONTEXTS/TOPICS."""
        col_upper = col_name.upper()
        
        # CDISC TEST/PARAMETER codes (these ARE contexts/topics - WHAT is being measured)
        topic_suffixes = ['TESTCD', 'TEST', 'PARAMCD', 'PARAM', 'DECOD', 'TERM']
        if any(col_upper.endswith(suffix) for suffix in topic_suffixes):
            return True
        
        # CDISC domain-specific topic patterns  
        for pattern_name, pattern_regex in self.cdisc_topic_patterns.items():
            if pattern_regex.match(col_upper):
                return True
        
        # Subject-level characteristics that vary clinically (demographic contexts)
        if col_upper in ['AGE', 'AAGE', 'WEIGHT', 'HEIGHT', 'BMI', 'SEX', 'RACE', 'ETHNIC']:
            return True
        
        # Treatment contexts (WHAT treatment was given)
        if any(suffix in col_upper for suffix in ['TRT01P', 'TRT01A', 'CMTRT', 'EXTRT']):
            return True
        
        return False
    
    def _appears_to_be_measurement(self, col_name: str, df: pd.DataFrame) -> bool:
        """
        Check if a column appears to represent a clinical measurement.
        
        Heuristics:
        1. Numeric data type suggests measurement
        2. Column name suggests clinical relevance
        3. Data has reasonable clinical value ranges
        """
        if col_name not in df.columns:
            return False
        
        col_data = df[col_name]
        col_lower = col_name.lower()
        
        # Check if column contains primarily numeric data
        try:
            numeric_data = pd.to_numeric(col_data, errors='coerce')
            numeric_ratio = numeric_data.notna().sum() / len(col_data) if len(col_data) > 0 else 0
            
            # If mostly numeric and has clinical-sounding name
            if numeric_ratio > 0.7:  # 70% numeric
                # Look for clinical measurement indicators in name
                measurement_indicators = [
                    'test', 'exam', 'measure', 'value', 'level', 'count',
                    'time', 'date', 'age', 'duration', 'dose', 'score'
                ]
                
                if any(indicator in col_lower for indicator in measurement_indicators):
                    return True
                
                # Check if values are in reasonable clinical ranges
                if numeric_data.notna().any():
                    min_val = numeric_data.min()
                    max_val = numeric_data.max()
                    
                    # Reasonable clinical measurement ranges
                    if 0 <= min_val <= 1000 and 0 <= max_val <= 10000:
                        return True
        except:
            pass
        
        return False
    
    def _identify_topics(self, df: pd.DataFrame) -> Tuple[Optional[str], List[TopicInfo]]:
        """Identify topics in the dataset."""
        topics = []
        topic_dimension = None
        
        # For vertical structure, look for topic dimension
        if self._detect_structure_type(df) == StructureType.VERTICAL:
            topic_dimension, topics = self._identify_vertical_topics(df)
        else:
            # For horizontal structure, each column is a topic
            topics = self._identify_horizontal_topics(df)
        
        return topic_dimension, topics
    
    def _identify_vertical_topics(self, df: pd.DataFrame) -> Tuple[Optional[str], List[TopicInfo]]:
        """Identify topics in a vertical structure dataset with enhanced CDISC pattern recognition."""
        topics = []
        topic_dimension = None
        
        # First try enhanced CDISC patterns (more specific)
        for col in df.columns:
            # Check CDISC-specific patterns first
            for pattern_name, pattern_regex in self.cdisc_topic_patterns.items():
                if pattern_regex.match(col):
                    topic_dimension = col
                    self.logger.debug(f"Found topic dimension '{col}' using CDISC pattern '{pattern_name}'")
                    break
            if topic_dimension:
                break
        
        # Fallback to original pattern matching if no CDISC pattern matched
        if not topic_dimension:
            for col in df.columns:
                col_lower = col.lower()
                for pattern_type, patterns in self.topic_dimension_patterns.items():
                    if any(pattern in col_lower for pattern in patterns):
                        topic_dimension = col
                        self.logger.debug(f"Found topic dimension '{col}' using fallback pattern '{pattern_type}'")
                        break
                if topic_dimension:
                    break
        
        if topic_dimension:
            # Get unique topic values
            unique_topics = df[topic_dimension].dropna().unique()
            
            for topic_value in unique_topics:
                topic_info = TopicInfo(
                    topic_name=str(topic_value),
                    topic_id=f"TOPIC_{str(topic_value).upper().replace(' ', '_')}",
                    topic_values=[str(topic_value)],
                    source_column=topic_dimension,
                    confidence=0.9
                )
                topics.append(topic_info)
        
        return topic_dimension, topics
    
    def _identify_horizontal_topics(self, df: pd.DataFrame) -> List[TopicInfo]:
        """
        Identify topics in a horizontal structure dataset using motivated reasoning.
        
        Only columns with compelling clinical reasons become topics.
        Metadata/administrative columns become attributes attached to other dimensions.
        """
        topics = []
        key_dimensions = self._identify_key_dimensions(df)
        
        self.logger.debug(f"Applying motivated topic detection to {len(df.columns)} columns")
        
        # Only columns with motivated clinical reasons become topics
        for col in df.columns:
            if col not in key_dimensions:
                # Apply motivated reasoning
                if self._has_motivated_reason_to_be_topic(col, df):
                    topic_info = TopicInfo(
                        topic_name=col,
                        topic_id=f"TOPIC_{col.upper().replace(' ', '_')}",
                        topic_values=[col],
                        source_column=col,
                        confidence=0.9  # Higher confidence for motivated topics
                    )
                    topics.append(topic_info)
                    self.logger.debug(f"✅ '{col}' promoted to topic (motivated)")
                else:
                    self.logger.debug(f"❌ '{col}' remains attribute (unmotivated)")
        
        self.logger.info(f"Motivated topic detection: {len(topics)} topics from {len(df.columns)} columns")
        return topics
    
    def _identify_measure_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify measure columns in the dataset."""
        measure_columns = []
        
        for pattern in self.measure_patterns:
            for col in df.columns:
                if pattern in col.lower() and col not in measure_columns:
                    measure_columns.append(col)
        
        return measure_columns
    
    def _identify_attribute_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify attribute columns in the dataset."""
        attribute_columns = []
        
        for pattern in self.attribute_patterns:
            for col in df.columns:
                if pattern in col.lower() and col not in attribute_columns:
                    attribute_columns.append(col)
        
        return attribute_columns

