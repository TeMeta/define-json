"""
Define-JSON: Data Implementation Definition for Clinical Data Contracts

A description of data implementation for both demand and supply data contracts
to complement CDISC USDM, ODM, and Dataset-JSON.
"""

__version__ = "0.1.0"
__author__ = "Define-JSON Team"

from .converters.xml_to_json import DefineXMLToJSONConverter
from .converters.json_to_xml import DefineJSONToXMLConverter
from .validation.roundtrip import run_roundtrip_test, validate_true_roundtrip

__all__ = [
    "DefineXMLToJSONConverter",
    "DefineJSONToXMLConverter", 
    "run_roundtrip_test",
    "validate_true_roundtrip"
]
