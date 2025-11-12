#!/usr/bin/env python3
"""
Test suite for Define-JSON schema validation.
"""

import unittest
import yaml
from pathlib import Path
import logging

# Configure logger
logger = logging.getLogger(__name__)

try:
    from linkml_runtime import SchemaView
    LINKML_AVAILABLE = True
except ImportError:
    LINKML_AVAILABLE = False
    logger.warning("LinkML not available. Schema structure tests will be skipped.")

class TestDefineJSONSchema(unittest.TestCase):
    """Test suite for Define-JSON schema validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.schema_path = Path("define-json.yaml")
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
        assert self.schema_data is not None
        self.assertIn('classes', self.schema_data)
        self.assertIn('enums', self.schema_data)
        
    def test_mixin_consistency(self):
        """Test that mixins are properly defined and used."""
        assert self.schema_data is not None
        classes = self.schema_data.get('classes', {})
        
        for class_name, class_def in classes.items():
            if 'mixins' in class_def:
                mixins = class_def['mixins']
                for mixin in mixins:
                    self.assertIn(mixin, classes, f"Class {class_name} references undefined mixin: {mixin}")
    
    @unittest.skipUnless(LINKML_AVAILABLE, "LinkML not available")
    def test_linkml_schema_loading(self):
        """Test that the schema can be loaded by LinkML."""
        schema_path = Path("define-json.yaml")
        sv = SchemaView(str(schema_path))
        self.assertIsNotNone(sv)

def run_tests():
    """Run all tests."""
    # Change to tests directory
    import os
    os.chdir(Path(__file__).parent)
    
    # Run tests
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests() 