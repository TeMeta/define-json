#!/usr/bin/env python3
"""
Minimal CDISC Variable Type Classifier - Standalone Version

Streamlined classifier focused on topic detection for dataset deconstruction.
No external dependencies beyond pandas and standard library.

Variable Types (DECs):
- IDENTIFIER: Study/Subject/Record identifiers (STUDYID, USUBJID, etc.)
- TIMING: Time-related variables (VISITNUM, --DTC, --DY, etc.)
- TOPIC: Context/dimension variables (--TESTCD, --PARAMCD, --DECOD, --TRT)
- RESULT: Measurement values (--ORRES, --STRESN, AVAL, CHG)
- ATTRIBUTE: Everything else
"""

import logging
import pandas as pd
import re
from typing import Optional, Dict, List
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class CDISCVariableType(Enum):
    """CDISC Variable Types based on Data Element Concept (DEC) classification."""
    IDENTIFIER = "identifier"    # STUDYID, USUBJID, --SEQ
    TIMING = "timing"           # VISITNUM, --DTC, --DY
    TOPIC = "topic"            # --TESTCD, --PARAMCD, --DECOD (contexts)
    RESULT = "result"          # --ORRES, --STRESN, AVAL (measures)
    ATTRIBUTE = "attribute"    # Everything else


@dataclass
class VariableClassification:
    """Result of variable classification."""
    variable_name: str
    variable_type: CDISCVariableType
    confidence: float
    reason: str
    domain_prefix: Optional[str] = None
    suffix: Optional[str] = None


class CDISCVariableClassifier:
    """
    Minimal CDISC variable classifier for topic detection.
    
    Focused on identifying TOPIC variables vs RESULT/IDENTIFIER/ATTRIBUTE.
    """
    
    def __init__(self):
        """Initialize the classifier with essential patterns."""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Core patterns - only what's needed for topic detection
        self.identifier_patterns = {
            'study': ['studyid', 'study_id', 'study'],
            'subject': ['usubjid', 'subjectid', 'subject_id', 'subjid'],
            'sequence': ['seq', 'seqnum'],
            'domain': ['domain', 'rdomain']
        }
        
        self.timing_patterns = {
            'visit': ['visitnum', 'visit', 'visitdy'],
            'date_time': ['dtc', 'dt', 'dat'],
            'study_day': ['dy', 'day', 'stdy', 'endy']
        }
        
        # TOPIC patterns - critical for structure detection
        self.topic_patterns = {
            'test_code_suffix': ['testcd', 'test'],
            'parameter_suffix': ['paramcd', 'param'],
            'decode_suffix': ['decod', 'term'],
            'treatment_suffix': ['trt']
        }
        
        # RESULT patterns - to distinguish from topics
        self.result_patterns = {
            'original_result': ['orres'],
            'standard_result': ['stresn', 'stresc'],
            'analysis_value': ['aval', 'avalc'],
            'change': ['chg', 'pchg'],
            'baseline': ['base', 'baseline'],
            'unit': ['orresu', 'stresu', 'avalu']
        }
        
        # Compile patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.compiled_patterns = {}
        
        for category, patterns in [
            ('identifier', self.identifier_patterns),
            ('timing', self.timing_patterns), 
            ('topic', self.topic_patterns),
            ('result', self.result_patterns)
        ]:
            self.compiled_patterns[category] = {}
            for subtype, pattern_list in patterns.items():
                pattern_regex = '|'.join([
                    f"^{p}$|{p}$|^{p}_|_{p}_|_{p}$" 
                    for p in pattern_list
                ])
                self.compiled_patterns[category][subtype] = re.compile(
                    pattern_regex, re.IGNORECASE
                )
    
    def classify_variable(self, variable_name: str, data: Optional[pd.Series] = None, 
                         context_columns: Optional[List[str]] = None) -> VariableClassification:
        """
        Classify a variable according to CDISC DEC standards.
        
        Args:
            variable_name: Name of the variable to classify
            data: Optional data series for data-driven analysis
            context_columns: Optional list of other columns in the dataset
            
        Returns:
            VariableClassification with type, confidence, and reasoning
        """
        var_lower = variable_name.lower()
        context_columns = context_columns or []
        
        # Extract domain prefix if present (e.g., VS in VSTESTCD)
        domain_prefix = self._extract_domain_prefix(variable_name)
        
        # Try each classification in order
        result = (
            self._classify_as_identifier(variable_name, var_lower, domain_prefix, data) or
            self._classify_as_timing(variable_name, var_lower, domain_prefix, data) or
            self._classify_as_topic(variable_name, var_lower, domain_prefix, data) or
            self._classify_as_result(variable_name, var_lower, domain_prefix, data) or
            VariableClassification(
                variable_name=variable_name,
                variable_type=CDISCVariableType.ATTRIBUTE,
                confidence=0.5,
                reason="No specific pattern matched - classified as attribute",
                domain_prefix=domain_prefix
            )
        )
        
        self.logger.debug(f"Variable '{variable_name}' classified as {result.variable_type.value}: {result.reason}")
        return result
    
    def _extract_domain_prefix(self, variable_name: str) -> Optional[str]:
        """Extract CDISC domain prefix (e.g., VS from VSTESTCD)."""
        match = re.match(r'^([A-Z]{2})([A-Z]+)$', variable_name.upper())
        if match:
            prefix = match.group(1)
            known_domains = ['AE', 'CM', 'DM', 'EG', 'EX', 'LB', 'MH', 'PR', 'QS', 'SC', 'SU', 'VS', 
                           'CE', 'CV', 'DX', 'FA', 'GF', 'IS', 'MB', 'PC', 'PF', 'RS', 'TR']
            if prefix in known_domains:
                return prefix
        return None
    
    def _classify_as_identifier(self, var_name: str, var_lower: str, 
                               domain_prefix: Optional[str], data: Optional[pd.Series]) -> Optional[VariableClassification]:
        """Check if variable is an identifier."""
        for subtype, pattern in self.compiled_patterns['identifier'].items():
            if pattern.search(var_lower):
                confidence = 0.95
                if data is not None:
                    uniqueness = len(data.unique()) / len(data) if len(data) > 0 else 0
                    if uniqueness > 0.8:
                        confidence = 0.98
                
                return VariableClassification(
                    variable_name=var_name,
                    variable_type=CDISCVariableType.IDENTIFIER,
                    confidence=confidence,
                    reason=f"Matches identifier pattern '{subtype}'",
                    domain_prefix=domain_prefix
                )
        return None
    
    def _classify_as_timing(self, var_name: str, var_lower: str,
                           domain_prefix: Optional[str], data: Optional[pd.Series]) -> Optional[VariableClassification]:
        """Check if variable is timing-related."""
        for subtype, pattern in self.compiled_patterns['timing'].items():
            if pattern.search(var_lower):
                return VariableClassification(
                    variable_name=var_name,
                    variable_type=CDISCVariableType.TIMING,
                    confidence=0.9,
                    reason=f"Matches timing pattern '{subtype}'",
                    domain_prefix=domain_prefix
                )
        return None
    
    def _classify_as_topic(self, var_name: str, var_lower: str,
                          domain_prefix: Optional[str], data: Optional[pd.Series]) -> Optional[VariableClassification]:
        """Check if variable is a topic (context/dimension)."""
        for subtype, pattern in self.compiled_patterns['topic'].items():
            if pattern.search(var_lower):
                confidence = 0.9
                if data is not None:
                    uniqueness = len(data.unique()) / len(data) if len(data) > 0 else 0
                    if 0.1 <= uniqueness <= 0.8:  # Moderate uniqueness
                        confidence = 0.95
                
                return VariableClassification(
                    variable_name=var_name,
                    variable_type=CDISCVariableType.TOPIC,
                    confidence=confidence,
                    reason=f"Matches topic pattern '{subtype}' - defines measurement context",
                    domain_prefix=domain_prefix
                )
        return None
    
    def _classify_as_result(self, var_name: str, var_lower: str,
                           domain_prefix: Optional[str], data: Optional[pd.Series]) -> Optional[VariableClassification]:
        """Check if variable is a result (measurement value)."""
        for subtype, pattern in self.compiled_patterns['result'].items():
            if pattern.search(var_lower):
                confidence = 0.9
                if data is not None and pd.api.types.is_numeric_dtype(data):
                    confidence = 0.95
                
                return VariableClassification(
                    variable_name=var_name,
                    variable_type=CDISCVariableType.RESULT,
                    confidence=confidence,
                    reason=f"Matches result pattern '{subtype}' - contains measurement values",
                    domain_prefix=domain_prefix
                )
        return None
    
    def classify_dataset_columns(self, df: pd.DataFrame) -> Dict[str, VariableClassification]:
        """
        Classify all columns in a dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary mapping column names to their classifications
        """
        self.logger.info(f"Classifying {len(df.columns)} variables in dataset")
        
        classifications = {}
        column_list = list(df.columns)
        
        for col_name in df.columns:
            classification = self.classify_variable(
                variable_name=col_name,
                data=df[col_name],
                context_columns=column_list
            )
            classifications[col_name] = classification
        
        # Log summary
        type_counts = {}
        for classification in classifications.values():
            var_type = classification.variable_type.value
            type_counts[var_type] = type_counts.get(var_type, 0) + 1
        
        self.logger.info(f"Classification summary: {type_counts}")
        return classifications
    
    def get_variables_by_type(self, classifications: Dict[str, VariableClassification], 
                             variable_type: CDISCVariableType) -> List[str]:
        """Get all variables of a specific type."""
        return [
            var_name for var_name, classification in classifications.items()
            if classification.variable_type == variable_type
        ]

