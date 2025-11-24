#!/usr/bin/env python3
"""
Comprehensive test suite for DataCube functionality with visual outputs and clinical scenarios.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Add parent directory to path to import datacube_engine
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from define_json.utils.datacube_engine import DataCubeEngine, load_example_config, get_available_examples
    DATACUBE_AVAILABLE = True
except ImportError:
    DATACUBE_AVAILABLE = False
    logger.warning("DataCube engine not available. Tests will be skipped.")

class TestDataCubeEngine(unittest.TestCase):
    """Test suite for DataCube engine with visual outputs and clinical scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_output_dir = Path("test_outputs")
        self.test_output_dir.mkdir(exist_ok=True)
    
    @unittest.skipUnless(DATACUBE_AVAILABLE, "DataCube engine not available")
    def test_vital_signs_datacube_transformation(self):
        """Test complete vital signs transformation with clinical analysis."""
        print("\n" + "="*60)
        print("🏥 VITAL SIGNS DATACUBE TRANSFORMATION TEST")
        print("="*60)
        
        # Load vital signs configuration
        engine = load_example_config('vital_signs')
        
        # Build datacube
        datacube_df = engine.build_datacube()
        
        # Clinical validation
        self.assertIsInstance(datacube_df, pd.DataFrame)
        self.assertGreater(len(datacube_df), 0)
        
        # Required clinical columns
        expected_columns = {'subject', 'test', 'result', 'sex', 'age'}
        self.assertTrue(expected_columns.issubset(datacube_df.columns))
        
        # Visual clinical summary
        self._print_clinical_summary("Vital Signs", datacube_df)
        self._generate_vital_signs_plots(datacube_df)
        
        # Clinical insights
        self._analyze_vital_signs_clinically(datacube_df)
        
        print("✅ Vital signs datacube transformation successful")
    
    @unittest.skipUnless(DATACUBE_AVAILABLE, "DataCube engine not available")
    def test_laboratory_datacube_transformation(self):
        """Test complete laboratory transformation with clinical analysis."""
        print("\n" + "="*60)
        print("🔬 LABORATORY DATACUBE TRANSFORMATION TEST")
        print("="*60)
        
        # Load laboratory configuration
        engine = load_example_config('laboratory')
        datacube_df = engine.build_datacube()
        
        # Clinical validation
        self.assertIsInstance(datacube_df, pd.DataFrame)
        self.assertGreater(len(datacube_df), 0)
        
        # Visual clinical summary
        self._print_clinical_summary("Laboratory", datacube_df)
        self._generate_laboratory_plots(datacube_df)
        
        # Clinical insights
        self._analyze_laboratory_clinically(datacube_df)
        
        print("✅ Laboratory datacube transformation successful")
    
    @unittest.skipUnless(DATACUBE_AVAILABLE, "DataCube engine not available")
    def test_schema_item_component_relationship(self):
        """Test that Items and Components work together in schema."""
        print("\n" + "="*60)
        print("🔗 SCHEMA ITEM-COMPONENT RELATIONSHIP TEST")
        print("="*60)
        
        engine = load_example_config('vital_signs')
        schema_info = engine.get_schema_info()
        
        # Validate schema structure
        self.assertIn('items', schema_info)
        self.assertIn('components', schema_info)
        self.assertIn('dsd', schema_info)
        
        items = schema_info['items']
        components = schema_info['components']
        
        # Visual schema representation
        self._print_schema_visual(items, components)
        
        # Validate Item-Component relationships
        for comp_id, component in components.items():
            if 'item' in component:
                item_ref = component['item']
                self.assertIn(item_ref, items, f"Component {comp_id} references non-existent item {item_ref}")
        
        print("✅ Schema relationships validated")
    
    @unittest.skipUnless(DATACUBE_AVAILABLE, "DataCube engine not available")
    def test_clinical_data_quality_assessment(self):
        """Test data quality from clinical perspective."""
        print("\n" + "="*60)
        print("📊 CLINICAL DATA QUALITY ASSESSMENT")
        print("="*60)
        
        engine = load_example_config('vital_signs')
        datacube_df = engine.build_datacube()
        
        # Clinical data quality checks
        quality_report = self._assess_clinical_data_quality(datacube_df)
        
        # Visual quality dashboard
        self._generate_quality_dashboard(quality_report, datacube_df)
        
        # Assert minimum quality standards
        self.assertGreaterEqual(quality_report['completeness'], 0.8, "Data completeness below 80%")
        self.assertGreaterEqual(quality_report['validity'], 0.9, "Data validity below 90%")
        
        print("✅ Clinical data quality assessment complete")
    
    def _print_clinical_summary(self, domain_name: str, df: pd.DataFrame):
        """Print clinical summary of the datacube."""
        print(f"\n📋 {domain_name} Clinical Summary:")
        print("-" * 40)
        print(f"Total observations: {len(df)}")
        print(f"Unique subjects: {df['subject'].nunique()}")
        print(f"Unique tests: {df['test'].nunique()}")
        
        if 'sex' in df.columns:
            print(f"Sex distribution: {df['sex'].value_counts().to_dict()}")
        
        if 'age' in df.columns:
            print(f"Age range: {df['age'].min():.0f} - {df['age'].max():.0f} years")
        
        if 'test' in df.columns:
            print(f"Tests performed: {list(df['test'].unique())}")
    
    def _generate_vital_signs_plots(self, df: pd.DataFrame):
        """Generate clinical visualizations for vital signs."""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Vital Signs Clinical Analysis', fontsize=16, fontweight='bold')
        
        # Blood pressure by sex
        if 'result' in df.columns and 'sex' in df.columns and 'test' in df.columns:
            bp_data = df[df['test'].str.contains('BP', na=False)]
            if isinstance(bp_data, pd.DataFrame) and not bp_data.empty:
                sns.boxplot(data=bp_data, x='test', y='result', hue='sex', ax=axes[0,0])
                axes[0,0].set_title('Blood Pressure by Sex')
                axes[0,0].set_ylabel('mmHg')
        
        # Age distribution
        if 'age' in df.columns:
            df['age'].hist(bins=15, ax=axes[0,1], alpha=0.7, color='skyblue')
            axes[0,1].set_title('Age Distribution')
            axes[0,1].set_xlabel('Age (years)')
        
        # Test frequency
        if 'test' in df.columns:
            test_counts = df['test'].value_counts()
            test_counts.plot(kind='bar', ax=axes[1,0], color='lightcoral')
            axes[1,0].set_title('Test Frequency')
            axes[1,0].tick_params(axis='x', rotation=45)
        
        # Results by visit
        if 'visit' in df.columns and 'result' in df.columns:
            visit_data = df.groupby('visit')['result'].mean()
            visit_data.plot(kind='line', marker='o', ax=axes[1,1], color='green')
            axes[1,1].set_title('Average Results by Visit')
        
        plt.tight_layout()
        output_path = self.test_output_dir / "vital_signs_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Vital signs visualization saved: {output_path}")
        plt.close()
    
    def _generate_laboratory_plots(self, df: pd.DataFrame):
        """Generate clinical visualizations for laboratory data."""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Laboratory Data Clinical Analysis', fontsize=16, fontweight='bold')
        
        # Lab values by test
        if 'test' in df.columns and 'result' in df.columns:
            sns.boxplot(data=df, x='test', y='result', ax=axes[0,0])
            axes[0,0].set_title('Lab Values by Test')
            axes[0,0].tick_params(axis='x', rotation=45)
        
        # Results by sex
        if 'sex' in df.columns and 'result' in df.columns:
            sns.violinplot(data=df, x='sex', y='result', ax=axes[0,1])
            axes[0,1].set_title('Results by Sex')
        
        # Age vs Results correlation
        if 'age' in df.columns and 'result' in df.columns:
            axes[1,0].scatter(df['age'], df['result'], alpha=0.6, color='purple')
            axes[1,0].set_title('Age vs Lab Results')
            axes[1,0].set_xlabel('Age (years)')
            axes[1,0].set_ylabel('Result')
        
        # Test distribution
        if 'test' in df.columns:
            test_counts = df['test'].value_counts()
            axes[1,1].pie(test_counts.values, labels=test_counts.index, autopct='%1.1f%%')
            axes[1,1].set_title('Test Distribution')
        
        plt.tight_layout()
        output_path = self.test_output_dir / "laboratory_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Laboratory visualization saved: {output_path}")
        plt.close()
    
    def _analyze_vital_signs_clinically(self, df: pd.DataFrame):
        """Perform clinical analysis of vital signs data."""
        print("\n🔍 Clinical Insights - Vital Signs:")
        print("-" * 40)
        
        # Blood pressure analysis
        if 'test' in df.columns and isinstance(df['test'], pd.Series):
            bp_data = df[df['test'].str.contains('BP', na=False)]
            if isinstance(bp_data, pd.DataFrame) and not bp_data.empty:
                sys_bp = bp_data[bp_data['test'].str.contains('Systolic', na=False)]['result']
                dia_bp = bp_data[bp_data['test'].str.contains('Diastolic', na=False)]['result']
                
                if isinstance(sys_bp, pd.Series) and not sys_bp.empty:
                    hypertensive = (sys_bp >= 140).sum()
                    print(f"  • Hypertensive readings (≥140 mmHg): {hypertensive}/{len(sys_bp)} ({hypertensive/len(sys_bp)*100:.1f}%)")
                
                if isinstance(dia_bp, pd.Series) and not dia_bp.empty:
                    high_dia = (dia_bp >= 90).sum()
                    print(f"  • High diastolic (≥90 mmHg): {high_dia}/{len(dia_bp)} ({high_dia/len(dia_bp)*100:.1f}%)")
        
        # Age-based analysis
        if 'age' in df.columns and 'subject' in df.columns:
            elderly = df[df['age'] >= 65]
            if isinstance(elderly, pd.DataFrame) and not elderly.empty:
                unique_elderly = elderly['subject'].nunique()
                print(f"  • Elderly patients (≥65): {unique_elderly}")
    
    def _analyze_laboratory_clinically(self, df: pd.DataFrame):
        """Perform clinical analysis of laboratory data."""
        print("\n🔍 Clinical Insights - Laboratory:")
        print("-" * 40)
        
        # Reference range analysis (simplified)
        lab_ranges = {
            'Glucose': (70, 100),
            'Cholesterol': (0, 200),
            'Hemoglobin': (12, 16)
        }
        
        if 'test' in df.columns and isinstance(df['test'], pd.Series):
            for test, (low, high) in lab_ranges.items():
                test_data = df[df['test'].str.contains(test, na=False, case=False)]['result']
                if isinstance(test_data, pd.Series) and not test_data.empty:
                    out_of_range = ((test_data < low) | (test_data > high)).sum()
                    print(f"  • {test} out of range ({low}-{high}): {out_of_range}/{len(test_data)} ({out_of_range/len(test_data)*100:.1f}%)")
    
    def _assess_clinical_data_quality(self, df: pd.DataFrame) -> dict:
        """Assess data quality from clinical perspective."""
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        
        # Completeness
        completeness = 1 - (missing_cells / total_cells)
        
        # Validity (basic checks)
        validity_issues = 0
        
        # Check for negative vital signs
        if 'result' in df.columns and 'test' in df.columns:
            vital_tests = df[df['test'].str.contains('BP|Pulse|Temp', na=False)]
            negative_vitals = (vital_tests['result'] < 0).sum()
            validity_issues += negative_vitals
        
        # Check for impossible ages
        if 'age' in df.columns:
            impossible_ages = ((df['age'] < 0) | (df['age'] > 120)).sum()
            validity_issues += impossible_ages
        
        validity = 1 - (validity_issues / len(df))
        
        return {
            'completeness': completeness,
            'validity': validity,
            'missing_cells': missing_cells,
            'validity_issues': validity_issues
        }
    
    def _generate_quality_dashboard(self, quality_report: dict, df: pd.DataFrame):
        """Generate data quality dashboard."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Clinical Data Quality Dashboard', fontsize=16, fontweight='bold')
        
        # Completeness gauge
        completeness = quality_report['completeness']
        axes[0,0].bar(['Completeness'], [completeness], color='green' if completeness > 0.8 else 'orange')
        axes[0,0].set_ylim(0, 1)
        axes[0,0].set_title(f'Data Completeness: {completeness:.1%}')
        
        # Validity gauge
        validity = quality_report['validity']
        axes[0,1].bar(['Validity'], [validity], color='green' if validity > 0.9 else 'red')
        axes[0,1].set_ylim(0, 1)
        axes[0,1].set_title(f'Data Validity: {validity:.1%}')
        
        # Missing data by column
        missing_by_col = df.isnull().sum()
        missing_by_col.plot(kind='bar', ax=axes[1,0], color='coral')
        axes[1,0].set_title('Missing Data by Column')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Data types distribution
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(exclude=[np.number]).columns
        
        type_counts = {'Numeric': len(numeric_cols), 'Categorical': len(categorical_cols)}
        axes[1,1].pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%')
        axes[1,1].set_title('Data Types Distribution')
        
        plt.tight_layout()
        output_path = self.test_output_dir / "data_quality_dashboard.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"📊 Quality dashboard saved: {output_path}")
        plt.close()
    
    def _print_schema_visual(self, items: dict, components: dict):
        """Print visual representation of schema structure."""
        print("\n🔗 Schema Structure Visualization:")
        print("-" * 50)
        
        # Items summary
        print("📋 ITEMS:")
        for item_id, item in items.items():
            data_type = item.get('dataType', 'unknown')
            name = item.get('name', 'unnamed')
            print(f"  {item_id}: {name} ({data_type})")
        
        print("\n🔧 COMPONENTS:")
        for comp_id, component in components.items():
            role = component.get('role', 'unknown')
            name = component.get('name', 'unnamed')
            item_ref = component.get('item', 'none')
            print(f"  {comp_id}: {name} [{role}] → Item: {item_ref}")
        
        # Relationship mapping
        print("\n🔗 ITEM-COMPONENT RELATIONSHIPS:")
        for comp_id, component in components.items():
            if 'item' in component:
                item_id = component['item']
                comp_name = component.get('name', comp_id)
                item_name = items.get(item_id, {}).get('name', 'unknown')
                print(f"  {comp_name} ←→ {item_name}")

if __name__ == '__main__':
    # Create output directory
    Path("test_outputs").mkdir(exist_ok=True)
    
    # Run tests with verbose output
    unittest.main(verbosity=2) 