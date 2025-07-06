#!/usr/bin/env python3
"""
Test suite for Define-JSON schema validation and fit-for-purpose testing.
"""

import unittest
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List

try:
    from linkml_runtime import SchemaView
    from linkml_runtime.utils.yamlutils import as_yaml
    LINKML_AVAILABLE = True
except ImportError:
    LINKML_AVAILABLE = False
    print("Warning: LinkML not available. Some tests will be skipped.")

class TestDefineJSONSchema(unittest.TestCase):
    """Test suite for Define-JSON schema validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.schema_path = Path("../define-json.yaml")
        self.schema_data = None
        
        # Load schema
        try:
            with open(self.schema_path, 'r') as f:
                self.schema_data = yaml.safe_load(f)
        except Exception as e:
            self.fail(f"Failed to load schema: {e}")
    
    def test_schema_loads(self):
        """Test that the schema file loads without errors."""
        self.assertIsNotNone(self.schema_data)
        self.assertIn('classes', self.schema_data)
        self.assertIn('enums', self.schema_data)
    
    def test_required_sections(self):
        """Test that all required schema sections are present."""
        required_sections = ['id', 'name', 'description', 'prefixes', 'classes', 'enums']
        for section in required_sections:
            self.assertIn(section, self.schema_data, f"Missing required section: {section}")
    
    def test_class_definitions(self):
        """Test that all classes have required attributes."""
        classes = self.schema_data.get('classes', {})
        self.assertGreater(len(classes), 0, "No classes defined")
        
        for class_name, class_def in classes.items():
            self.assertIn('description', class_def, f"Class {class_name} missing description")
            
            # Check for Aristotelian description pattern
            description = class_def['description']
            if isinstance(description, str):
                self.assertTrue(
                    description.startswith('A ') or description.startswith('An '),
                    f"Class {class_name} description should start with 'A ' or 'An '"
                )
    
    def test_enum_definitions(self):
        """Test that all enums have required attributes."""
        enums = self.schema_data.get('enums', {})
        
        for enum_name, enum_def in enums.items():
            self.assertIn('description', enum_def, f"Enum {enum_name} missing description")
            self.assertIn('permissible_values', enum_def, f"Enum {enum_name} missing permissible_values")
    
    def test_mixin_consistency(self):
        """Test that mixins are properly defined and used."""
        classes = self.schema_data.get('classes', {})
        
        for class_name, class_def in classes.items():
            if 'mixins' in class_def:
                mixins = class_def['mixins']
                for mixin in mixins:
                    self.assertIn(mixin, classes, f"Class {class_name} references undefined mixin: {mixin}")
    
    def test_attribute_definitions(self):
        """Test that attributes are properly defined."""
        classes = self.schema_data.get('classes', {})
        
        for class_name, class_def in classes.items():
            if 'attributes' in class_def:
                attributes = class_def['attributes']
                for attr_name, attr_def in attributes.items():
                    self.assertIn('description', attr_def, f"Attribute {attr_name} in {class_name} missing description")
                    self.assertIn('range', attr_def, f"Attribute {attr_name} in {class_name} missing range")
    
    def test_no_full_stops_in_descriptions(self):
        """Test that descriptions don't end with full stops (except for multi-line descriptions)."""
        classes = self.schema_data.get('classes', {})
        
        for class_name, class_def in classes.items():
            description = class_def.get('description', '')
            if isinstance(description, str) and not description.startswith('>'):
                self.assertFalse(
                    description.endswith('.'),
                    f"Class {class_name} description ends with full stop: {description}"
                )
            
            # Check attributes
            if 'attributes' in class_def:
                for attr_name, attr_def in class_def['attributes'].items():
                    attr_desc = attr_def.get('description', '')
                    if isinstance(attr_desc, str) and not attr_desc.startswith('>'):
                        self.assertFalse(
                            attr_desc.endswith('.'),
                            f"Attribute {attr_name} in {class_name} description ends with full stop: {attr_desc}"
                        )

class TestLinkMLCompatibility(unittest.TestCase):
    """Test LinkML-specific functionality."""
    
    @unittest.skipUnless(LINKML_AVAILABLE, "LinkML not available")
    def test_linkml_schema_loading(self):
        """Test that the schema can be loaded by LinkML."""
        schema_path = Path("../define-json.yaml")
        sv = SchemaView(str(schema_path))
        self.assertIsNotNone(sv)
    
    @unittest.skipUnless(LINKML_AVAILABLE, "LinkML not available")
    def test_linkml_class_validation(self):
        """Test that all classes can be validated by LinkML."""
        schema_path = Path("../define-json.yaml")
        sv = SchemaView(str(schema_path))
        
        # Test that we can get all classes
        classes = sv.all_classes()
        self.assertGreater(len(classes), 0)
        
        # Test that we can get all enums
        enums = sv.all_enums()
        self.assertGreater(len(enums), 0)

class TestFitForPurpose(unittest.TestCase):
    """Test that the schema is fit for its intended purpose."""
    
    def setUp(self):
        """Set up test fixtures."""
        schema_path = Path("../define-json.yaml")
        with open(schema_path, 'r') as f:
            self.schema_data = yaml.safe_load(f)
    
    def test_cdisc_compatibility(self):
        """Test that the schema supports CDISC use cases."""
        classes = self.schema_data.get('classes', {})
        
        # Check for CDISC-specific classes
        cdisc_classes = ['Item', 'ItemGroup', 'CodeList', 'MetaDataVersion']
        for class_name in cdisc_classes:
            self.assertIn(class_name, classes, f"Missing CDISC class: {class_name}")
    
    def test_fhir_compatibility(self):
        """Test that the schema supports FHIR use cases."""
        classes = self.schema_data.get('classes', {})
        
        # Check for FHIR-compatible classes
        fhir_classes = ['Resource', 'DocumentReference']
        for class_name in fhir_classes:
            self.assertIn(class_name, classes, f"Missing FHIR-compatible class: {class_name}")
    
    def test_sdmx_compatibility(self):
        """Test that the schema supports SDMX use cases."""
        classes = self.schema_data.get('classes', {})
        
        # Check for SDMX-compatible classes
        sdmx_classes = ['Dataset', 'Dataflow', 'DataStructureDefinition']
        for class_name in sdmx_classes:
            self.assertIn(class_name, classes, f"Missing SDMX-compatible class: {class_name}")
    
    def test_data_cube_support(self):
        """Test that the schema supports data cube operations."""
        classes = self.schema_data.get('classes', {})
        
        # Check for data cube classes
        cube_classes = ['Dimension', 'Measure', 'DataAttribute']
        for class_name in cube_classes:
            self.assertIn(class_name, classes, f"Missing data cube class: {class_name}")
    
    def test_relationship_support(self):
        """Test that the schema supports relationship modeling."""
        classes = self.schema_data.get('classes', {})
        
        # Check for relationship classes
        relationship_classes = ['Relationship', 'CodingMapping']
        for class_name in relationship_classes:
            self.assertIn(class_name, classes, f"Missing relationship class: {class_name}")

def run_tests():
    """Run all tests."""
    # Change to tests directory
    import os
    os.chdir(Path(__file__).parent)
    
    # Run tests
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests() 