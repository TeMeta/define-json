"""
Define-JSON: Data Implementation Definition for Clinical Data Contracts

A description of data implementation for both demand and supply data contracts
to complement CDISC USDM, ODM, and Dataset-JSON.
"""

__version__ = "0.1.0"
__author__ = "Define-JSON Team"

from .converters.xml_to_json import DefineXMLToJSONConverter
from .converters.json_to_xml import DefineJSONToXMLConverter
from .converters.html_generator import DefineHTMLGenerator
from .converters.converter_helpers import (
    convert_computation_method_to_formal_expression,
    convert_programming_code_to_formal_expression,
    convert_translated_text_from_xml,
    extract_standards_from_attributes,
    convert_analysis_dataset_from_xml,
    convert_parameter_to_reified_concept
)
from .validation.roundtrip import run_roundtrip_test, validate_true_roundtrip

__all__ = [
    "DefineXMLToJSONConverter",
    "DefineJSONToXMLConverter",
    "DefineHTMLGenerator",
    "run_roundtrip_test",
    "validate_true_roundtrip",
    "convert_computation_method_to_formal_expression",
    "convert_programming_code_to_formal_expression",
    "convert_translated_text_from_xml",
    "extract_standards_from_attributes",
    "convert_analysis_dataset_from_xml",
    "convert_parameter_to_reified_concept",
    "convert_where_clause_to_condition"
]
