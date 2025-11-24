#!/usr/bin/env python3
"""
Dataset Deconstructor - Standalone Version

Self-contained dataset deconstructor with no external dependencies beyond pandas.
Focuses on building dataset specialisations from analysis results.

Single Responsibility: Build Dataset Specialisations from analysis results.
"""

import pandas as pd
import logging
from typing import Dict, List, Any
from dataclasses import dataclass

try:
    from .topic_detector import TopicDetector, StructureType, DatasetStructure
    from .models import DatasetBreakdown, TopicBreakdown, ReifiedConceptInfo
    from .column_analyzer import ColumnAnalysis, ColumnRole
    from .specialisation_builder import SpecialisationBuilder
except ImportError:
    from topic_detector import TopicDetector, StructureType, DatasetStructure
    from models import DatasetBreakdown, TopicBreakdown, ReifiedConceptInfo
    from column_analyzer import ColumnAnalysis, ColumnRole
    from specialisation_builder import SpecialisationBuilder

logger = logging.getLogger(__name__)


@dataclass
class DeconstructionConfig:
    """Configuration for dataset deconstruction."""
    enable_sdtm_patterns: bool = True
    enable_concept_mapping: bool = False  # Disabled in standalone
    enable_specialisation_building: bool = True
    
    def __post_init__(self):
        pass


class DatasetDeconstructor:
    """
    Standalone Dataset Deconstructor.
    
    This class focuses on:
    1. Analyzing dataset structure (vertical vs horizontal)
    2. Identifying topics, dimensions, measures, and attributes
    3. Building specialisations from analysis results
    4. Zero external dependencies beyond pandas
    """
    
    def __init__(self, config: DeconstructionConfig = None):
        """
        Initialize the dataset deconstructor.
        
        Args:
            config: Configuration for deconstruction process
        """
        self.config = config or DeconstructionConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize topic detector (uses local variable_classifier)
        self.topic_detector = TopicDetector()
        self.logger.info("✅ Standalone Dataset Deconstructor initialized")
        
        # Initialize specialisation builder if enabled
        if self.config.enable_specialisation_building:
            self.specialisation_builder = SpecialisationBuilder()
        else:
            self.specialisation_builder = None
    
    def deconstruct_dataset(self, df: pd.DataFrame, dataset_name: str = None) -> DatasetBreakdown:
        """
        Deconstruct a dataset into structured metadata specialisations.
        
        Args:
            df: Input dataset as pandas DataFrame
            dataset_name: Optional name for the dataset
            
        Returns:
            Complete dataset breakdown with all components
        """
        self.logger.info(f"🔍 Starting dataset deconstruction for: {dataset_name or 'unnamed'}")
        
        # Step 1: Basic structure detection and analysis
        structure = self.topic_detector.analyze_structure(df)
        self.logger.info(f"📊 Detected structure type: {structure.structure_type.value}")
        self.logger.info(f"   - Key dimensions: {structure.key_dimensions}")
        self.logger.info(f"   - Topics found: {len(structure.topics)}")
        self.logger.info(f"   - Measure columns: {len(structure.measure_columns)}")
        self.logger.info(f"   - Attribute columns: {len(structure.attribute_columns)}")
        
        # Step 2: Analyze columns
        key_dimension_analyses = self._analyze_columns(df, structure.key_dimensions, ColumnRole.KEY)
        global_attribute_analyses = self._analyze_columns(df, structure.attribute_columns, ColumnRole.ATTRIBUTE)
        
        # Step 3: Create topic breakdowns
        topic_breakdowns = self._create_topic_breakdowns(df, structure)
        
        # Step 4: Create complete breakdown
        breakdown = DatasetBreakdown(
            structure=structure,
            key_dimensions=key_dimension_analyses,
            topic_breakdowns=topic_breakdowns,
            global_attributes=global_attribute_analyses,
            data_structure_definition_oid=f"DSD_{dataset_name or 'dataset'}",
            dataset_oid=f"DATASET_{dataset_name or 'dataset'}"
        )
        
        self.logger.info(f"✅ Dataset deconstruction complete. Found {len(structure.topics)} topics.")
        return breakdown
    
    def _analyze_columns(self, df: pd.DataFrame, column_names: List[str], role: ColumnRole) -> List[ColumnAnalysis]:
        """Analyze a set of columns."""
        analyses = []
        
        for col_name in column_names:
            if col_name not in df.columns:
                continue
                
            col_data = df[col_name]
            
            # Get unique values (limit to 20 for performance)
            unique_vals = col_data.dropna().unique()
            if len(unique_vals) > 20:
                unique_vals = unique_vals[:20]
            
            analysis = ColumnAnalysis(
                name=col_name,
                role=role,
                data_type=str(col_data.dtype),
                null_count=int(col_data.isna().sum()),
                unique_values=[str(v) for v in unique_vals],
                coding_suggestions=[f"role:{role.value}", f"type:{col_data.dtype}"]
            )
            analyses.append(analysis)
        
        return analyses
    
    def _create_topic_breakdowns(self, df: pd.DataFrame, structure: DatasetStructure) -> List[TopicBreakdown]:
        """Create detailed breakdowns for each topic."""
        breakdowns = []
        
        for topic_info in structure.topics:
            # Analyze topic-related columns
            measure_analyses = self._analyze_columns(df, structure.measure_columns, ColumnRole.MEASURE)
            property_analyses = []  # Would need more sophisticated analysis
            attribute_analyses = []  # Would need more sophisticated analysis
            
            # Create WHERE clause for vertical structures
            where_clause = ""
            if structure.structure_type == StructureType.VERTICAL and structure.topic_dimension:
                where_clause = f"{structure.topic_dimension} = '{topic_info.topic_name}'"
            
            # Create item group OID
            item_group_oid = f"IG_{topic_info.topic_id}"
            
            # Create reified concept (simplified - no registry lookup)
            reified_concept = None
            if self.config.enable_concept_mapping:
                reified_concept = ReifiedConceptInfo(
                    OID=f"RC_{topic_info.topic_id}",
                    name=topic_info.topic_name,
                    description=f"Reified concept for {topic_info.topic_name}"
                )
            
            breakdown = TopicBreakdown(
                topic_info=topic_info,
                reified_concept=reified_concept,
                measure_columns=measure_analyses,
                property_columns=property_analyses,
                attribute_columns=attribute_analyses,
                where_clause=where_clause,
                item_group_oid=item_group_oid
            )
            breakdowns.append(breakdown)
        
        return breakdowns
    
    def build_specialisation(self, breakdown: DatasetBreakdown) -> Dict[str, Any]:
        """
        Build a complete Dataset Specialisation from breakdown.
        
        Args:
            breakdown: Dataset breakdown from deconstruct_dataset()
            
        Returns:
            Complete Dataset Specialisation as dictionary
        """
        if not self.specialisation_builder:
            raise RuntimeError("Specialisation building not enabled in config")
        
        return self.specialisation_builder.build_specialisation_dict(breakdown)
    
    def deconstruct_and_build(self, df: pd.DataFrame, dataset_name: str = None) -> Dict[str, Any]:
        """
        One-step deconstruction and specialisation building.
        
        Args:
            df: Input dataset as pandas DataFrame
            dataset_name: Optional name for the dataset
            
        Returns:
            Complete Dataset Specialisation
        """
        breakdown = self.deconstruct_dataset(df, dataset_name)
        
        if self.config.enable_specialisation_building:
            return self.build_specialisation(breakdown)
        else:
            # Return simplified representation
            return {
                "structure_type": breakdown.structure.structure_type.value,
                "key_dimensions": [col.name for col in breakdown.key_dimensions],
                "topics": [tb.topic_info.topic_name for tb in breakdown.topic_breakdowns],
                "topic_breakdowns": [
                    {
                        "topic_name": tb.topic_info.topic_name,
                        "where_clause": tb.where_clause,
                        "item_group_oid": tb.item_group_oid,
                        "measures": [col.name for col in tb.measure_columns]
                    }
                    for tb in breakdown.topic_breakdowns
                ]
            }


# Convenience function
def deconstruct_dataset(df: pd.DataFrame, dataset_name: str = None, 
                       build_specialisation: bool = False) -> Dict[str, Any]:
    """
    Convenience function to deconstruct a dataset.
    
    Args:
        df: Input dataset as pandas DataFrame
        dataset_name: Optional name for the dataset
        build_specialisation: Whether to build full specialisation
        
    Returns:
        Dataset analysis results or complete specialisation
    """
    config = DeconstructionConfig(enable_specialisation_building=build_specialisation)
    deconstructor = DatasetDeconstructor(config)
    
    if build_specialisation:
        return deconstructor.deconstruct_and_build(df, dataset_name)
    else:
        breakdown = deconstructor.deconstruct_dataset(df, dataset_name)
        return {
            "structure_type": breakdown.structure.structure_type.value,
            "key_dimensions": [col.name for col in breakdown.key_dimensions],
            "topics": [tb.topic_info.topic_name for tb in breakdown.topic_breakdowns],
            "measure_columns": [col.name for col in breakdown.topic_breakdowns[0].measure_columns] if breakdown.topic_breakdowns else []
        }

