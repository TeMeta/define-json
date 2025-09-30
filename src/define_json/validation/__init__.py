"""
Validation module for Define-JSON.

Comprehensive validation and roundtrip testing functionality.
"""

from .roundtrip import run_roundtrip_test, validate_true_roundtrip
from .schema import validate_define_json

__all__ = [
    "run_roundtrip_test",
    "validate_true_roundtrip", 
    "validate_define_json"
]
