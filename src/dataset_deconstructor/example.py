#!/usr/bin/env python3
"""
Example Usage of Standalone Dataset Deconstructor

Demonstrates how to use the standalone dataset deconstructor
with no external dependencies beyond pandas.
"""

import pandas as pd
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

# Import from standalone package
try:
    from dataset_deconstructor import (
        DatasetDeconstructor,
        DeconstructionConfig,
        deconstruct_dataset
    )
except ImportError:
    # If running directly, add to path
    sys.path.insert(0, str(Path(__file__).parent))
    from dataset_deconstructor import (
        DatasetDeconstructor,
        DeconstructionConfig,
        deconstruct_dataset
    )


def create_example_vertical_dataset():
    """Create example vertical structure dataset (Vital Signs)."""
    data = {
        'STUDYID': ['STUDY01'] * 12,
        'USUBJID': ['SUBJ001'] * 6 + ['SUBJ002'] * 6,
        'VISITNUM': [1, 1, 1, 2, 2, 2] * 2,
        'VSTESTCD': ['SYSBP', 'DIABP', 'PULSE'] * 4,
        'VSTEST': ['Systolic Blood Pressure', 'Diastolic Blood Pressure', 'Pulse Rate'] * 4,
        'VSORRES': [120, 80, 72, 122, 82, 74, 118, 78, 70, 120, 80, 72],
        'VSORRESU': ['mmHg', 'mmHg', 'beats/min'] * 4,
        'VSDTC': ['2024-01-15'] * 12
    }
    return pd.DataFrame(data)


def create_example_horizontal_dataset():
    """Create example horizontal structure dataset (Demographics)."""
    data = {
        'STUDYID': ['STUDY01', 'STUDY01', 'STUDY01'],
        'USUBJID': ['SUBJ001', 'SUBJ002', 'SUBJ003'],
        'AGE': [45, 52, 38],
        'SEX': ['M', 'F', 'M'],
        'RACE': ['WHITE', 'BLACK', 'ASIAN'],
        'ETHNIC': ['NOT HISPANIC OR LATINO'] * 3,
        'WEIGHT': [75.5, 68.2, 82.1],
        'HEIGHT': [175, 162, 180]
    }
    return pd.DataFrame(data)


def example_1_quick_analysis():
    """Example 1: Quick convenience function."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Quick Convenience Function")
    print("="*70)
    
    df = create_example_vertical_dataset()
    
    # Quick analysis using convenience function
    result = deconstruct_dataset(df, "VS")
    
    print("\n📊 Quick Analysis Results:")
    print(f"  Structure Type: {result['structure_type']}")
    print(f"  Key Dimensions: {result['key_dimensions']}")
    print(f"  Topics Found: {result['topics']}")
    print(f"  Measure Columns: {result['measure_columns']}")


def example_2_detailed_analysis():
    """Example 2: Detailed deconstruction with full breakdown."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Detailed Deconstruction Analysis")
    print("="*70)
    
    df = create_example_vertical_dataset()
    
    # Create deconstructor
    deconstructor = DatasetDeconstructor()
    
    # Deconstruct dataset
    breakdown = deconstructor.deconstruct_dataset(df, "VS")
    
    print("\n🔍 Detailed Breakdown:")
    print(f"\n  Structure Type: {breakdown.structure.structure_type.value}")
    print(f"  Topic Dimension: {breakdown.structure.topic_dimension}")
    print(f"\n  Key Dimensions ({len(breakdown.key_dimensions)}):")
    for col in breakdown.key_dimensions:
        print(f"    - {col.name} ({col.data_type}, {col.null_count} nulls)")
    
    print(f"\n  Topics ({len(breakdown.structure.topics)}):")
    for topic in breakdown.structure.topics:
        print(f"    - {topic.topic_name} (from {topic.source_column})")
    
    print(f"\n  Topic Breakdowns ({len(breakdown.topic_breakdowns)}):")
    for tb in breakdown.topic_breakdowns:
        print(f"    - {tb.topic_info.topic_name}")
        print(f"      WHERE: {tb.where_clause}")
        print(f"      Item Group OID: {tb.item_group_oid}")
        print(f"      Measures: {[col.name for col in tb.measure_columns]}")


def example_3_horizontal_structure():
    """Example 3: Analyzing horizontal structure dataset."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Horizontal Structure (Demographics)")
    print("="*70)
    
    df = create_example_horizontal_dataset()
    
    # Deconstruct
    deconstructor = DatasetDeconstructor()
    breakdown = deconstructor.deconstruct_dataset(df, "DM")
    
    print("\n📋 Demographics Analysis:")
    print(f"  Structure Type: {breakdown.structure.structure_type.value}")
    print(f"  Key Dimensions: {breakdown.structure.key_dimensions}")
    
    print(f"\n  Topics (Each Column is a Topic):")
    for topic in breakdown.structure.topics:
        print(f"    - {topic.topic_name}")
    
    print(f"\n  Global Attributes:")
    for attr in breakdown.global_attributes:
        print(f"    - {attr.name} ({attr.data_type})")


def example_4_with_specialisation():
    """Example 4: Building full specialisation."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Building Complete Specialisation")
    print("="*70)
    
    df = create_example_vertical_dataset()
    
    # Enable specialisation building
    config = DeconstructionConfig(enable_specialisation_building=True)
    deconstructor = DatasetDeconstructor(config)
    
    # Build complete specialisation
    try:
        specialisation = deconstructor.deconstruct_and_build(df, "VS")
        
        print("\n✨ Complete Specialisation Built:")
        print(f"  Data Structure Definition: {specialisation['DataStructureDefinition']['OID']}")
        print(f"  Reified Concepts: {len(specialisation['ReifiedConcepts'])}")
        print(f"  Item Groups: {len(specialisation['ItemGroups'])}")
        print(f"  Items: {len(specialisation['Items'])}")
        print(f"  Code Lists: {len(specialisation['CodeLists'])}")
        
        print("\n  Sample Item Group:")
        if specialisation['ItemGroups']:
            ig = specialisation['ItemGroups'][0]
            print(f"    OID: {ig['OID']}")
            print(f"    Name: {ig['name']}")
            print(f"    Items: {ig.get('items', [])[:5]}...")  # First 5 items
    
    except Exception as e:
        print(f"\n⚠️ Specialisation building encountered an issue: {e}")
        print("   (This is expected if some dependencies are missing)")


def example_5_variable_classification():
    """Example 5: Using variable classifier directly."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Direct Variable Classification")
    print("="*70)
    
    from variable_classifier import CDISCVariableClassifier
    
    df = create_example_vertical_dataset()
    
    # Create classifier
    classifier = CDISCVariableClassifier()
    
    # Classify all columns
    classifications = classifier.classify_dataset_columns(df)
    
    print("\n🏷️ Variable Classifications:")
    for col_name, classification in classifications.items():
        print(f"  {col_name:15s} → {classification.variable_type.value:12s} "
              f"(confidence: {classification.confidence:.2f})")
        print(f"                  Reason: {classification.reason}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "="*70)
    print("STANDALONE DATASET DECONSTRUCTOR - EXAMPLES")
    print("="*70)
    print("\nDemonstrating standalone dataset deconstruction with zero dependencies")
    print("beyond pandas. All analysis is performed locally with built-in CDISC")
    print("variable classification.")
    
    try:
        example_1_quick_analysis()
        example_2_detailed_analysis()
        example_3_horizontal_structure()
        example_4_with_specialisation()
        example_5_variable_classification()
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(run_all_examples())

