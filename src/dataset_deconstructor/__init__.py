"""
Standalone Dataset Deconstructor Package

A self-contained dataset analysis tool with no external dependencies beyond pandas.

Main Components:
- DatasetDeconstructor: Main class for dataset analysis
- TopicDetector: Detects dataset structure and topics
- CDISCVariableClassifier: Classifies CDISC variable types
- SpecialisationBuilder: Builds Define-JSON structures

Usage:
    from dataset_deconstructor_standalone import DatasetDeconstructor
    import pandas as pd
    
    df = pd.read_csv("my_dataset.csv")
    deconstructor = DatasetDeconstructor()
    breakdown = deconstructor.deconstruct_dataset(df, "MyDataset")
    
    print(f"Structure: {breakdown.structure.structure_type}")
    print(f"Topics: {[t.topic_name for t in breakdown.structure.topics]}")
"""

from .dataset_deconstructor import DatasetDeconstructor, DeconstructionConfig, deconstruct_dataset
from .topic_detector import TopicDetector, TopicInfo, DatasetStructure, StructureType
from .variable_classifier import CDISCVariableClassifier, CDISCVariableType, VariableClassification
from .specialisation_builder import SpecialisationBuilder, SpecialisationComponents
from .models import DatasetBreakdown, TopicBreakdown, ReifiedConceptInfo
from .column_analyzer import ColumnAnalysis, ColumnRole

__version__ = "1.0.0"
__all__ = [
    # Main classes
    'DatasetDeconstructor',
    'DeconstructionConfig',
    'TopicDetector',
    'CDISCVariableClassifier',
    'SpecialisationBuilder',
    
    # Data models
    'DatasetBreakdown',
    'TopicBreakdown',
    'DatasetStructure',
    'TopicInfo',
    'ColumnAnalysis',
    'ReifiedConceptInfo',
    'SpecialisationComponents',
    'VariableClassification',
    
    # Enums
    'StructureType',
    'CDISCVariableType',
    'ColumnRole',
    
    # Convenience functions
    'deconstruct_dataset',
]

