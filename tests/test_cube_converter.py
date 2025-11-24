"""
Tests for CubeConfigConverter
"""

import pytest
from pathlib import Path

from define_json.utils.cube_config_converter import CubeConfigConverter
from define_json.schema.define import (
    Item,
    DataStructureDefinition,
    Dimension,
    Measure,
    DataAttribute,
    DataType
)


class TestCubeConfigConverter:
    """Test suite for CubeConfigConverter"""
    
    @pytest.fixture
    def lab_config_path(self):
        """Path to laboratory cube config"""
        return str(Path(__file__).parent.parent / 'configs' / 'laboratory_cube.yaml')
    
    @pytest.fixture
    def vs_config_path(self):
        """Path to vital signs cube config"""
        return str(Path(__file__).parent.parent / 'configs' / 'vital_signs_cube.yaml')
    
    def test_load_yaml_config(self, lab_config_path):
        """Test loading YAML config"""
        config = CubeConfigConverter.load_yaml_config(lab_config_path)
        
        assert config is not None
        assert 'items' in config
        assert 'components' in config
        assert 'data_structure_definition' in config
    
    def test_yaml_to_schema_basic(self, lab_config_path):
        """Test basic YAML to schema conversion"""
        items_dict, components_dict, dsd = CubeConfigConverter.validate_and_convert(lab_config_path)
        
        # Check items
        assert len(items_dict) == 10
        assert 'IT001' in items_dict
        assert isinstance(items_dict['IT001'], Item)
        assert items_dict['IT001'].OID == 'IT001'
        assert items_dict['IT001'].name == 'Subject ID'
        
        # Check components
        assert len(components_dict) == 10
        assert 'DIM001' in components_dict
        assert isinstance(components_dict['DIM001'], Dimension)
        
        # Check DSD
        assert isinstance(dsd, DataStructureDefinition)
        assert dsd.OID == 'DSD002'
        assert len(dsd.dimensions) == 5
        assert len(dsd.measures) == 3
        assert len(dsd.attributes) == 2
    
    def test_datatype_mapping(self, lab_config_path):
        """Test dataType enum mapping"""
        items_dict, _, _ = CubeConfigConverter.validate_and_convert(lab_config_path)
        
        # String → text
        assert items_dict['IT001'].dataType == DataType.text
        
        # Integer → integer
        assert items_dict['IT002'].dataType == DataType.integer
        
        # Float → float
        assert items_dict['IT006'].dataType == DataType.float
    
    def test_component_roles(self, lab_config_path):
        """Test component role classification"""
        _, components_dict, _ = CubeConfigConverter.validate_and_convert(lab_config_path)
        
        # Dimensions
        assert isinstance(components_dict['DIM001'], Dimension)
        assert isinstance(components_dict['DIM002'], Dimension)
        
        # Measures
        assert isinstance(components_dict['MEAS001'], Measure)
        assert isinstance(components_dict['MEAS002'], Measure)
        
        # Attributes
        assert isinstance(components_dict['ATTR001'], DataAttribute)
        assert isinstance(components_dict['ATTR002'], DataAttribute)
    
    def test_item_references(self, lab_config_path):
        """Test that components correctly reference items"""
        items_dict, components_dict, _ = CubeConfigConverter.validate_and_convert(lab_config_path)
        
        # DIM001 should reference IT001
        assert components_dict['DIM001'].item == 'IT001'
        assert 'IT001' in items_dict
        
        # MEAS001 should reference IT006
        assert components_dict['MEAS001'].item == 'IT006'
        assert 'IT006' in items_dict
    
    def test_roundtrip_conversion(self, vs_config_path):
        """Test roundtrip: YAML → Schema → YAML"""
        # Load original
        original_config = CubeConfigConverter.load_yaml_config(vs_config_path)
        
        # Convert to schema
        items_dict, components_dict, dsd = CubeConfigConverter.yaml_to_schema(original_config)
        
        # Convert back to YAML
        regenerated_config = CubeConfigConverter.schema_to_yaml(
            items_dict, 
            components_dict, 
            dsd,
            include_metadata=True
        )
        
        # Verify structure preservation
        assert len(regenerated_config['items']) == len(original_config['items'])
        assert len(regenerated_config['components']) == len(original_config['components'])
        
        orig_dsd = original_config['data_structure_definition']
        regen_dsd = regenerated_config['data_structure_definition']
        
        assert len(regen_dsd['dimensions']) == len(orig_dsd['dimensions'])
        assert len(regen_dsd['measures']) == len(orig_dsd['measures'])
        assert len(regen_dsd['attributes']) == len(orig_dsd['attributes'])
    
    def test_schema_validation(self):
        """Test that schema validation works"""
        # Valid item should work
        item = Item(
            OID='TEST001',
            name='Test Item',
            dataType=DataType.text
        )
        assert item.OID == 'TEST001'
        
        # Invalid dataType should fail
        with pytest.raises(Exception):  # Pydantic ValidationError
            Item(
                OID='TEST002',
                name='Invalid Item',
                dataType='invalid_type'
            )
    
    def test_oid_field_mapping(self, lab_config_path):
        """Test that 'id' in YAML maps to 'OID' in schema"""
        config = CubeConfigConverter.load_yaml_config(lab_config_path)
        items_dict, components_dict, dsd = CubeConfigConverter.yaml_to_schema(config)
        
        # YAML has 'id', schema should have 'OID'
        assert config['items']['IT001']['id'] == 'IT001'
        assert items_dict['IT001'].OID == 'IT001'
        
        assert config['components']['DIM001']['id'] == 'DIM001'
        assert components_dict['DIM001'].OID == 'DIM001'
        
        assert config['data_structure_definition']['id'] == 'DSD002'
        assert dsd.OID == 'DSD002'
    
    def test_both_configs_work(self, lab_config_path, vs_config_path):
        """Test that both example configs can be converted"""
        # Laboratory
        lab_items, lab_comps, lab_dsd = CubeConfigConverter.validate_and_convert(lab_config_path)
        assert len(lab_items) > 0
        assert len(lab_comps) > 0
        assert lab_dsd is not None
        
        # Vital Signs
        vs_items, vs_comps, vs_dsd = CubeConfigConverter.validate_and_convert(vs_config_path)
        assert len(vs_items) > 0
        assert len(vs_comps) > 0
        assert vs_dsd is not None

