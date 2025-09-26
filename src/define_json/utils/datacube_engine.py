"""
Data Cube Engine for SDTM to Data Cube Transformation
Generic engine that loads configurations and examples to create data cubes
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional


class DataCubeEngine:
    """Generic engine for transforming SDTM data to data cubes using configurations"""
    
    def __init__(self):
        self.config = None
        self.sdtm_data = {}
        self.items = {}
        self.components = {}
        self.dsd = None
        self.datacube_df = None
        
    def load_config(self, config_path: str) -> None:
        """Load a data cube configuration file"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Extract configuration sections
        self.items = self.config.get('items', {})
        self.components = self.config.get('components', {})
        self.dsd = self.config.get('data_structure_definition', {})
        self.data_mapping = self.config.get('data_mapping', {})
        
        print(f"✅ Loaded configuration: {self.config.get('name', 'Unknown')}")
        print(f"   • Items: {len(self.items)}")
        print(f"   • Components: {len(self.components)}")
        print(f"   • Data Structure Definition: {self.dsd.get('name', 'Unknown')}")
    
    def load_example_data(self, example_path: str) -> None:
        """Load example SDTM data from YAML file"""
        with open(example_path, 'r') as f:
            self.sdtm_data = yaml.safe_load(f)
        
        # Convert to DataFrames
        for domain, data in self.sdtm_data.items():
            if isinstance(data, list) and data:
                self.sdtm_data[domain] = pd.DataFrame(data)
        
        print(f"✅ Loaded example data:")
        for domain, df in self.sdtm_data.items():
            if isinstance(df, pd.DataFrame):
                print(f"   • {domain}: {len(df)} records")
    
    def build_datacube(self) -> pd.DataFrame:
        """Transform SDTM data to data cube format using configuration"""
        if not self.config or not self.sdtm_data:
            raise ValueError("Configuration and data must be loaded first")
        
        observations = []
        
        # Get the main measurement domain (VS or LB) - handle both with and without sdtm_ prefix
        measurement_domains = ['VS', 'LB', 'sdtm_vs', 'sdtm_lb']
        measurement_domain = None
        for domain in measurement_domains:
            if domain in self.sdtm_data:
                measurement_domain = domain
                break
        
        if not measurement_domain:
            raise ValueError("No measurement domain (VS or LB) found in data")
        
        # Get DM domain for demographics - handle both with and without sdtm_ prefix
        dm_df = self.sdtm_data.get('DM', pd.DataFrame())
        if dm_df.empty:
            dm_df = self.sdtm_data.get('sdtm_dm', pd.DataFrame())
        
        # Process measurement domain
        if measurement_domain in ['VS', 'sdtm_vs']:
            observations = self._process_vital_signs(dm_df)
        elif measurement_domain in ['LB', 'sdtm_lb']:
            observations = self._process_laboratory(dm_df)
        
        self.datacube_df = pd.DataFrame(observations)
        return self.datacube_df
    
    def _process_vital_signs(self, dm_df: pd.DataFrame) -> List[Dict]:
        """Process vital signs data"""
        # Get VS data - handle both with and without sdtm_ prefix
        vs_df = self.sdtm_data.get('VS', pd.DataFrame())
        if vs_df.empty:
            vs_df = self.sdtm_data.get('sdtm_vs', pd.DataFrame())
        
        observations = []
        
        for _, vs_record in vs_df.iterrows():
            # Get corresponding DM record
            dm_record = dm_df[dm_df['USUBJID'] == vs_record['USUBJID']]
            if dm_record.empty:
                continue
            dm_record = dm_record.iloc[0]
            
            # Map test codes to test names
            test_mapping = {
                'SYSBP': 'Systolic BP',
                'DIABP': 'Diastolic BP',
                'PULSE': 'Pulse Rate',
                'TEMP': 'Temperature',
                'HEIGHT': 'Height',
                'WEIGHT': 'Weight'
            }
            
            test_name = test_mapping.get(vs_record['VSTESTCD'], vs_record['VSTESTCD'])
            
            observation = {
                'subject': vs_record['USUBJID'],
                'age': dm_record.get('AGE', None),
                'sex': dm_record.get('SEX', None),
                'race': dm_record.get('RACE', None),
                'visit': vs_record.get('VISIT', None),
                'test': test_name,
                'result': vs_record.get('VSORRES', None),
                'unit': vs_record.get('VSORRESU', None),
                'arm': dm_record.get('ARM', None),
                'date': vs_record.get('VSDTC', None)
            }
            observations.append(observation)
        
        return observations
    
    def _process_laboratory(self, dm_df: pd.DataFrame) -> List[Dict]:
        """Process laboratory data"""
        # Get LB data - handle both with and without sdtm_ prefix
        lb_df = self.sdtm_data.get('LB', pd.DataFrame())
        if lb_df.empty:
            lb_df = self.sdtm_data.get('sdtm_lb', pd.DataFrame())
        
        observations = []
        
        for _, lb_record in lb_df.iterrows():
            # Get corresponding DM record
            dm_record = dm_df[dm_df['USUBJID'] == lb_record['USUBJID']]
            if dm_record.empty:
                continue
            dm_record = dm_record.iloc[0]
            
            observation = {
                'subject': lb_record['USUBJID'],
                'age': dm_record.get('AGE', None),
                'sex': dm_record.get('SEX', None),
                'race': dm_record.get('RACE', None),
                'visit': lb_record.get('VISIT', None),
                'test': lb_record.get('LBTEST', lb_record['LBTESTCD']),
                'result': lb_record.get('LBORRES', None),
                'unit': lb_record.get('LBORRESU', None),
                'arm': dm_record.get('ARM', None),
                'date': lb_record.get('LBDTC', None)
            }
            observations.append(observation)
        
        return observations
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get information about the schema transformation"""
        return {
            'items': self.items,
            'components': self.components,
            'dsd': self.dsd,
            'data_mapping': self.data_mapping
        }
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary statistics for the data cube"""
        if self.datacube_df is None:
            return {}
        
        summary = {
            'total_observations': len(self.datacube_df),
            'unique_subjects': self.datacube_df['subject'].nunique(),
            'unique_tests': self.datacube_df['test'].nunique(),
            'tests': self.datacube_df['test'].value_counts().to_dict(),
            'sex_distribution': self.datacube_df['sex'].value_counts().to_dict() if 'sex' in self.datacube_df.columns else {},
            'arm_distribution': self.datacube_df['arm'].value_counts().to_dict() if 'arm' in self.datacube_df.columns else {},
            'numeric_summary': {}
        }
        
        # Add numeric summaries for result column
        if 'result' in self.datacube_df.columns:
            summary['numeric_summary'] = self.datacube_df['result'].describe().to_dict()
        
        return summary


def load_example_config(example_type: str = 'vital_signs') -> DataCubeEngine:
    """Helper function to load a specific example configuration"""
    engine = DataCubeEngine()
    
    # Map example types to config and data files
    config_mapping = {
        'vital_signs': 'configs/vital_signs_cube.yaml',
        'laboratory': 'configs/laboratory_cube.yaml'
    }
    
    data_mapping = {
        'vital_signs': 'examples/vital_signs_data.yaml',
        'laboratory': 'examples/laboratory_data.yaml',
        'full': 'examples/sdtm_sample_data.yaml'
    }
    
    config_path = config_mapping.get(example_type, 'configs/vital_signs_cube.yaml')
    data_path = data_mapping.get(example_type, 'examples/vital_signs_data.yaml')
    
    engine.load_config(config_path)
    engine.load_example_data(data_path)
    
    return engine


def get_available_examples() -> List[str]:
    """Get list of available example types"""
    return ['vital_signs', 'laboratory', 'full'] 