"""
Validation module for Data Definition Specification.

Comprehensive validation and roundtrip testing functionality.
"""

from .roundtrip import run_roundtrip_test, validate_true_roundtrip
from .schema import validate_data_definition_spec

__all__ = [
    "run_roundtrip_test",
    "validate_true_roundtrip", 
    "validate_data_definition_spec"
]
