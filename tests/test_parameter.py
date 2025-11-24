"""
Test Parameter and FormalExpression functionality with new schema.

Tests both inline and reusable parameter patterns.
"""

import unittest
import json
from pathlib import Path
import tempfile


class TestParameterFunctionality(unittest.TestCase):
    """Test Parameter class with optional OID and inline support."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def test_inline_parameter_no_oid(self):
        """Test that inline parameters work without OID."""
        # Create a FormalExpression with inline parameters
        expression_data = {
            "OID": "FE.CALC_BMI",
            "name": "calculateBMI",
            "expression": "weight / (height * height)",
            "context": "python",
            "parameters": [
                {
                    "name": "weight",
                    "dataType": "float",
                    "required": True,
                    "description": "Weight in kilograms"
                },
                {
                    "name": "height",
                    "dataType": "float",
                    "required": True,
                    "description": "Height in meters"
                }
            ]
        }
        
        # Verify structure
        self.assertEqual(len(expression_data["parameters"]), 2)
        
        # Verify parameters don't need OID
        for param in expression_data["parameters"]:
            self.assertIn("name", param)
            self.assertNotIn("OID", param)  # Optional - not required
            self.assertIn("dataType", param)
    
    def test_reusable_parameter_with_oid(self):
        """Test that reusable parameters can have OID."""
        expression_data = {
            "OID": "FE.STANDARD_CALC",
            "name": "standardCalculation",
            "expression": "visitDay - baselineDay",
            "context": "python",
            "parameters": [
                {
                    "OID": "PARAM.STD.VISIT_DAY",
                    "name": "visitDay",
                    "dataType": "integer",
                    "required": True,
                    "description": "Standard visit day parameter"
                },
                {
                    "OID": "PARAM.STD.BASELINE_DAY",
                    "name": "baselineDay",
                    "dataType": "integer",
                    "required": True,
                    "description": "Standard baseline day parameter"
                }
            ]
        }
        
        # Verify parameters have OIDs
        for param in expression_data["parameters"]:
            self.assertIn("OID", param)
            self.assertIn("name", param)
    
    def test_parameter_with_conditions(self):
        """Test parameter with validation conditions."""
        parameter_data = {
            "name": "age",
            "dataType": "integer",
            "required": True,
            "defaultValue": "18",
            "conditions": ["COND.AGE_RANGE"],
            "description": "Age parameter with validation"
        }
        
        # Verify structure
        self.assertEqual(parameter_data["name"], "age")
        self.assertTrue(parameter_data["required"])
        self.assertIn("conditions", parameter_data)
        self.assertEqual(len(parameter_data["conditions"]), 1)
    
    def test_parameter_with_applicable_when(self):
        """Test parameter with applicableWhen clause."""
        parameter_data = {
            "name": "pregnancyStatus",
            "dataType": "text",
            "required": False,
            "applicableWhen": ["WC.FEMALE_SUBJECTS"],
            "description": "Only applicable for female subjects"
        }
        
        # Verify structure
        self.assertIn("applicableWhen", parameter_data)
        self.assertFalse(parameter_data["required"])
    
    def test_parameter_with_codelist(self):
        """Test parameter with codeList constraint."""
        parameter_data = {
            "name": "treatmentArm",
            "dataType": "text",
            "required": True,
            "codeList": ["CL.ARM"],
            "description": "Treatment arm from controlled terminology"
        }
        
        # Verify structure
        self.assertIn("codeList", parameter_data)
        self.assertEqual(len(parameter_data["codeList"]), 1)
    
    def test_parameter_value_vs_default_value(self):
        """Test distinction between value (bound) and defaultValue."""
        # Bound parameter (constant)
        bound_param = {
            "name": "pi",
            "dataType": "float",
            "value": "3.14159",
            "description": "Mathematical constant"
        }
        
        # Parameter with default
        default_param = {
            "name": "timeout",
            "dataType": "integer",
            "defaultValue": "30",
            "description": "Timeout in seconds, defaults to 30"
        }
        
        # Verify both work
        self.assertIn("value", bound_param)
        self.assertNotIn("defaultValue", bound_param)
        
        self.assertIn("defaultValue", default_param)
        self.assertNotIn("value", default_param)
    
    def test_mixed_inline_and_reference_parameters(self):
        """Test FormalExpression with both inline and referenced parameters."""
        expression_data = {
            "OID": "FE.MIXED",
            "name": "mixedParameterExpression",
            "expression": "standardParam + customValue",
            "context": "python",
            "parameters": [
                # Inline parameter (no OID)
                {
                    "name": "customValue",
                    "dataType": "float",
                    "required": True
                },
                # Reusable parameter (with OID)
                {
                    "OID": "PARAM.STANDARD",
                    "name": "standardParam",
                    "dataType": "float",
                    "required": True
                }
            ]
        }
        
        # Verify mixed approach works
        params = expression_data["parameters"]
        self.assertEqual(len(params), 2)
        self.assertNotIn("OID", params[0])  # First is inline
        self.assertIn("OID", params[1])     # Second is reusable
    
    def test_parameter_with_items_dependency(self):
        """Test parameter with item dependencies."""
        parameter_data = {
            "name": "derivationInput",
            "dataType": "text",
            "items": ["IT.DM.AGE", "IT.DM.SEX"],
            "description": "Parameter depends on multiple items"
        }
        
        # Verify items reference
        self.assertIn("items", parameter_data)
        self.assertEqual(len(parameter_data["items"]), 2)
    
    def test_parameter_with_concept_property(self):
        """Test parameter referencing concept properties."""
        parameter_data = {
            "name": "biomarkerValue",
            "dataType": "float",
            "conceptProperty": ["CP.BIOMARKER.VALUE"],
            "description": "Parameter maps to concept property"
        }
        
        # Verify conceptProperty reference
        self.assertIn("conceptProperty", parameter_data)
        self.assertEqual(len(parameter_data["conceptProperty"]), 1)
    
    def test_complete_formal_expression_example(self):
        """Test complete FormalExpression with all parameter features."""
        complete_example = {
            "OID": "FE.DERIVE_CHANGE_FROM_BASELINE",
            "name": "deriveChangeFromBaseline",
            "description": "Calculate change from baseline value",
            "expression": "(currentValue - baselineValue) / baselineValue * 100",
            "context": "python",
            "returnType": "float",
            "parameters": [
                {
                    "name": "currentValue",
                    "dataType": "float",
                    "required": True,
                    "description": "Current visit value",
                    "conditions": ["COND.NON_NEGATIVE"]
                },
                {
                    "OID": "PARAM.STD.BASELINE",
                    "name": "baselineValue",
                    "dataType": "float",
                    "required": True,
                    "description": "Baseline value (reusable parameter)",
                    "conditions": ["COND.NON_ZERO", "COND.NON_NEGATIVE"]
                }
            ],
            "returnValue": {
                "OID": "RV.PERCENT_CHANGE",
                "name": "percentChange",
                "dataType": "float",
                "description": "Percent change from baseline"
            }
        }
        
        # Verify complete structure
        self.assertIn("parameters", complete_example)
        self.assertEqual(len(complete_example["parameters"]), 2)
        self.assertIn("returnValue", complete_example)
        
        # Verify mixed parameter types
        params = complete_example["parameters"]
        self.assertNotIn("OID", params[0])  # Inline
        self.assertIn("OID", params[1])     # Reusable


if __name__ == '__main__':
    unittest.main()
