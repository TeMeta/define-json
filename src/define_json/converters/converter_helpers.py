"""
Helper functions for Define-XML <-> Define-JSON conversion.
Enables schema-compliant intermediate format with minimal _* fields.

This module provides utilities to:
1. Strip preservation fields for schema validation
2. Infer code context from programming language
3. Convert XML-specific structures to schema-native objects
4. Handle TranslatedText and Standards properly
5. Support ARM (Analysis Results Metadata) structures
"""

from typing import Dict, Any, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


def to_schema_compliant(conversion_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strip all _* preservation fields to get pure schema-compliant JSON.
    
    Use this when you want to validate against the schema or export
    for consumption by tools that don't need XML roundtrip capability.
    
    Args:
        conversion_json: JSON with _* preservation fields
        
    Returns:
        Schema-compliant JSON without any _* fields
        
    Example:
        >>> intermediate = converter.convert_file(xml_path, json_path)
        >>> schema_json = to_schema_compliant(intermediate)
        >>> # schema_json can now be validated against define.yaml
    """
    def strip_underscores(obj):
        if isinstance(obj, dict):
            return {
                k: strip_underscores(v) 
                for k, v in obj.items() 
                if not k.startswith('_')
            }
        elif isinstance(obj, list):
            return [strip_underscores(item) for item in obj]
        return obj
    
    return strip_underscores(conversion_json)


def infer_code_context(code: str) -> str:
    """
    Infer programming language from code content.
    
    Detects common programming languages used in clinical trials:
    - SAS
    - R
    - Python
    - SQL
    
    Args:
        code: The code string to analyze
        
    Returns:
        Detected language name (defaults to 'SAS')
        
    Example:
        >>> infer_code_context("proc freq data=adsl;")
        'SAS'
        >>> infer_code_context("summary(df)")
        'R'
    """
    code_lower = code.lower().strip()
    
    # SAS detection
    if any(keyword in code_lower for keyword in 
           ['proc ', 'data ', 'run;', 'quit;', 'proc freq', 'proc means']):
        return 'SAS'
    
    # R detection
    if any(keyword in code_lower for keyword in 
           ['library(', '<-', 'summary(', 'ggplot', 'dplyr']):
        return 'R'
    
    # Python detection
    if any(keyword in code_lower for keyword in 
           ['import ', 'def ', 'pandas', 'numpy', 'print(']):
        return 'Python'
    
    # SQL detection
    if any(keyword in code_lower for keyword in 
           ['select ', 'from ', 'where ', 'join ', 'group by']):
        return 'SQL'
    
    # Default to SAS for clinical trials
    return 'SAS'


def convert_computation_method_to_formal_expression(
    computation_method_element: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert XML ComputationMethod to FormalExpression format.
    
    XML Structure:
        <def:ComputationMethod OID="CM.001">
            Description or computation text
        </def:ComputationMethod>
    
    JSON Structure:
        {
            "context": "SAS",
            "expression": "Description or computation text"
        }
    
    Args:
        computation_method_element: Raw element with:
            - _attributes: Dict with OID, etc.
            - _text: The computation description/code
            
    Returns:
        FormalExpression dict
        
    Example:
        >>> raw = {
        ...     '_attributes': {'OID': 'CM.001'},
        ...     '_text': 'proc freq data=adsl;'
        ... }
        >>> convert_computation_method_to_formal_expression(raw)
        {'context': 'SAS', 'expression': 'proc freq data=adsl;'}
    """
    code = computation_method_element.get('_text', '').strip()
    context = infer_code_context(code)
    
    return {
        'context': context,
        'expression': code
    }


def convert_programming_code_to_formal_expression(
    programming_code_element: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert ARM ProgrammingCode to FormalExpression format.
    
    XML Structure:
        <arm:ProgrammingCode Context="SAS">
            <arm:Code>proc freq data=adsl; run;</arm:Code>
            <arm:DocumentRef DocumentOID="DOC.001"/>
        </arm:ProgrammingCode>
    
    JSON Structure:
        {
            "context": "SAS",
            "expression": "proc freq data=adsl; run;",
            "documentRefs": ["DOC.001"]
        }
    
    Args:
        programming_code_element: Raw ARM element with:
            - _attributes: Dict with Context
            - _Code_elements: List with code text
            - _DocumentRef_elements: Optional list of doc refs
            
    Returns:
        FormalExpression dict
        
    Example:
        >>> raw = {
        ...     '_attributes': {'Context': 'R'},
        ...     '_Code_elements': [{'_text': 'summary(data)'}]
        ... }
        >>> convert_programming_code_to_formal_expression(raw)
        {'context': 'R', 'expression': 'summary(data)'}
    """
    context = programming_code_element.get('_attributes', {}).get('Context', 'SAS')
    
    # Extract code from _Code_elements
    code_elements = programming_code_element.get('_Code_elements', [])
    code = ''
    if code_elements and len(code_elements) > 0:
        code = code_elements[0].get('_text', '')
    
    formal_expr = {
        'context': context,
        'expression': code.strip()
    }
    
    # Add document references if present
    doc_refs = programming_code_element.get('_DocumentRef_elements', [])
    if doc_refs:
        formal_expr['documentRefs'] = [
            ref.get('_attributes', {}).get('DocumentOID', '')
            for ref in doc_refs
            if ref.get('_attributes', {}).get('DocumentOID')
        ]
    
    return formal_expr


def convert_translated_text_from_xml(
    text: str,
    attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert XML TranslatedText to schema structure.
    
    XML: <Description><TranslatedText xml:lang="en">Study Data</TranslatedText></Description>
    JSON: {"lang": "en", "value": "Study Data"}
    
    Args:
        text: The text content
        attributes: XML attributes dict (e.g., {'xml:lang': 'en'})
        
    Returns:
        TranslatedText dict with lang and value
        
    Example:
        >>> convert_translated_text_from_xml("Study Data", {'xml:lang': 'en'})
        {'lang': 'en', 'value': 'Study Data'}
    """
    # Extract language code (handle both xml:lang and lang)
    lang = attributes.get('xml:lang') or attributes.get('lang', 'en')
    
    return {
        'lang': lang,
        'value': text
    }


def convert_translated_text_to_xml(
    translated_text: Dict[str, Any]
) -> tuple[str, Dict[str, str]]:
    """
    Convert schema TranslatedText back to XML format.
    
    Args:
        translated_text: Dict with 'lang' and 'value' keys
        
    Returns:
        Tuple of (text_value, attributes_dict)
        
    Example:
        >>> convert_translated_text_to_xml({'lang': 'en', 'value': 'Study Data'})
        ('Study Data', {'xml:lang': 'en'})
    """
    text = translated_text.get('value', '')
    lang = translated_text.get('lang', 'en')
    
    return text, {'xml:lang': lang}


def extract_standards_from_attributes(
    attributes: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Extract Standard objects from def:* attributes.
    
    XML: <ItemGroupDef def:StandardOID="STD.SDTM.AE" def:StandardName="SDTM" 
                      def:StandardVersion="1.7">
    JSON: [{
        "standardOID": "STD.SDTM.AE",
        "standardName": "SDTM",
        "standardVersion": "1.7"
    }]
    
    Args:
        attributes: Dict of XML attributes
        
    Returns:
        List of Standard objects
        
    Example:
        >>> attrs = {
        ...     'def:StandardOID': 'STD.SDTM.AE',
        ...     'def:StandardName': 'SDTM',
        ...     'def:StandardVersion': '1.7'
        ... }
        >>> extract_standards_from_attributes(attrs)
        [{'standardOID': 'STD.SDTM.AE', 'standardName': 'SDTM', 'standardVersion': '1.7'}]
    """
    standards = []
    
    # Look for def:StandardOID or similar patterns
    standard_oid = None
    standard_name = None
    standard_version = None
    
    for key, value in attributes.items():
        key_lower = key.lower()
        if 'standardoid' in key_lower:
            standard_oid = value
        elif 'standardname' in key_lower:
            standard_name = value
        elif 'standardversion' in key_lower:
            standard_version = value
    
    if standard_oid or standard_name:
        standard = {}
        if standard_oid:
            standard['standardOID'] = standard_oid
        if standard_name:
            standard['standardName'] = standard_name
        if standard_version:
            standard['standardVersion'] = standard_version
        standards.append(standard)
    
    return standards


def convert_standards_to_attributes(
    standards: List[Dict[str, Any]],
    namespace_prefix: str = 'def'
) -> Dict[str, str]:
    """
    Convert Standard objects back to def:* attributes.
    
    Args:
        standards: List of Standard objects
        namespace_prefix: Namespace prefix to use (default: 'def')
        
    Returns:
        Dict of XML attributes
        
    Example:
        >>> stds = [{'standardOID': 'STD.SDTM.AE', 'standardName': 'SDTM'}]
        >>> convert_standards_to_attributes(stds)
        {'def:StandardOID': 'STD.SDTM.AE', 'def:StandardName': 'SDTM'}
    """
    attributes = {}
    
    if not standards:
        return attributes
    
    # Use first standard if multiple
    standard = standards[0]
    
    if 'standardOID' in standard:
        attributes[f'{namespace_prefix}:StandardOID'] = standard['standardOID']
    if 'standardName' in standard:
        attributes[f'{namespace_prefix}:StandardName'] = standard['standardName']
    if 'standardVersion' in standard:
        attributes[f'{namespace_prefix}:StandardVersion'] = standard['standardVersion']
    
    return attributes


def convert_analysis_dataset_from_xml(
    analysis_dataset_element: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert ARM AnalysisDataset to ItemGroupRef.
    
    XML Structure:
        <arm:AnalysisDataset ItemGroupOID="ADSL">
            <WhereClauseRef WhereClauseOID="WC.ITT"/>
            <arm:AnalysisVariable ItemOID="ADSL.ITTFL"/>
        </arm:AnalysisDataset>
    
    JSON Structure (ItemGroupRef):
        {
            "itemGroupOID": "ADSL",
            "applicableWhen": "WC.ITT",
            "itemRefs": [{"itemOID": "ADSL.ITTFL"}]
        }
    
    Args:
        analysis_dataset_element: Raw ARM element
        
    Returns:
        ItemGroupRef dict
    """
    item_group_oid = analysis_dataset_element.get('_attributes', {}).get('ItemGroupOID', '')
    
    item_group_ref = {
        'itemGroupOID': item_group_oid
    }
    
    # Extract WhereClauseRef
    wc_refs = analysis_dataset_element.get('_WhereClauseRef_elements', [])
    if wc_refs and len(wc_refs) > 0:
        wc_oid = wc_refs[0].get('_attributes', {}).get('WhereClauseOID', '')
        if wc_oid:
            item_group_ref['applicableWhen'] = wc_oid
    
    # Extract AnalysisVariable elements as ItemRefs
    analysis_vars = analysis_dataset_element.get('_AnalysisVariable_elements', [])
    if analysis_vars:
        item_refs = []
        for var in analysis_vars:
            item_oid = var.get('_attributes', {}).get('ItemOID', '')
            if item_oid:
                item_refs.append({'itemOID': item_oid})
        if item_refs:
            item_group_ref['itemRefs'] = item_refs
    
    return item_group_ref


def convert_parameter_to_reified_concept(
    parameter_element: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert ARM Parameter to ReifiedConcept.
    
    XML Structure:
        <arm:Parameter OID="PARAM.001" Name="PARAMCD" 
                      ValueType="text" Value="DIABP"/>
    
    JSON Structure (ReifiedConcept):
        {
            "OID": "RC.PARAMCD.DIABP",
            "subject": "PARAMCD",
            "predicateTerm": "IS_VALUE_OF",
            "object": "DIABP"
        }
    
    Args:
        parameter_element: Raw ARM Parameter element
        
    Returns:
        ReifiedConcept dict
    """
    attrs = parameter_element.get('_attributes', {})
    
    oid = attrs.get('OID', '')
    name = attrs.get('Name', '')
    value = attrs.get('Value', '')
    
    # Generate OID if not present
    if not oid and name and value:
        oid = f'RC.{name}.{value}'
    
    return {
        'OID': oid,
        'subject': name,
        'predicateTerm': 'IS_VALUE_OF',
        'object': value if value else ''
    }


def validate_roundtrip_json(
    json_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate that JSON has necessary preservation fields for roundtrip.
    
    Checks for:
    - _namespace_metadata
    - _root_attributes
    - Element type markers where needed
    
    Args:
        json_data: The conversion JSON to validate
        
    Returns:
        Dict with:
            - valid: bool
            - missing_fields: List[str]
            - warnings: List[str]
    """
    missing_fields = []
    warnings = []
    
    # Check for namespace metadata
    if '_namespace_metadata' not in json_data:
        missing_fields.append('_namespace_metadata')
    else:
        ns_meta = json_data['_namespace_metadata']
        if 'namespaces' not in ns_meta:
            warnings.append('_namespace_metadata missing namespaces')
    
    # Check for root attributes
    if '_root_attributes' not in json_data:
        missing_fields.append('_root_attributes')
    
    # Check methods for element type markers
    methods = json_data.get('methods', [])
    for i, method in enumerate(methods):
        if 'elementType' not in method and '_elementType' not in method:
            warnings.append(f'Method {i} missing elementType marker')
    
    return {
        'valid': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'warnings': warnings
    }


def build_analysis_result_from_xml(
    analysis_results_element: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert ARM AnalysisResults element to AnalysisResult schema object.
    
    This is the main converter for ARM analysis results that extends Method.
    
    XML Structure:
        <arm:AnalysisResults OID="AR.001" ParameterOID="PARAM.DIABP">
            <Description><TranslatedText>...</TranslatedText></Description>
            <arm:AnalysisReason>SPECIFIED IN PROTOCOL</arm:AnalysisReason>
            <arm:AnalysisPurpose>PRIMARY OUTCOME MEASURE</arm:AnalysisPurpose>
            <arm:AnalysisDatasets>...</arm:AnalysisDatasets>
            <arm:ProgrammingCode>...</arm:ProgrammingCode>
        </arm:AnalysisResults>
    
    JSON Structure (extends Method):
        {
            "OID": "AR.001",
            "name": "Analysis of DIABP",
            "type": "Analysis",
            "analysisReason": "SPECIFIED IN PROTOCOL",
            "analysisPurpose": "PRIMARY OUTCOME MEASURE",
            "parameterOID": "PARAM.DIABP",
            "analysisDatasets": [ItemGroupRef, ...],
            "formalExpressions": [FormalExpression, ...]
        }
    
    Args:
        analysis_results_element: Raw ARM AnalysisResults element
        
    Returns:
        AnalysisResult dict (extends Method)
    """
    attrs = analysis_results_element.get('_attributes', {})
    
    analysis_result = {
        'OID': attrs.get('OID', ''),
        'type': 'Analysis'
    }
    
    # Extract name from description
    if 'description' in analysis_results_element:
        desc = analysis_results_element['description']
        if isinstance(desc, dict):
            analysis_result['name'] = desc.get('value', '')
        else:
            analysis_result['name'] = str(desc)
    
    # Extract ARM-specific attributes
    if 'ParameterOID' in attrs:
        analysis_result['parameterOID'] = attrs['ParameterOID']
    
    # Extract AnalysisReason
    reason_elements = analysis_results_element.get('_AnalysisReason_elements', [])
    if reason_elements:
        analysis_result['analysisReason'] = reason_elements[0].get('_text', '')
    
    # Extract AnalysisPurpose
    purpose_elements = analysis_results_element.get('_AnalysisPurpose_elements', [])
    if purpose_elements:
        analysis_result['analysisPurpose'] = purpose_elements[0].get('_text', '')
    
    # Convert AnalysisDatasets to ItemGroupRefs
    dataset_container = analysis_results_element.get('_AnalysisDatasets_elements', [])
    if dataset_container:
        analysis_datasets = []
        for container in dataset_container:
            for dataset_elem in container.get('_AnalysisDataset_elements', []):
                dataset_ref = convert_analysis_dataset_from_xml(dataset_elem)
                analysis_datasets.append(dataset_ref)
        if analysis_datasets:
            analysis_result['analysisDatasets'] = analysis_datasets
    
    # Convert ProgrammingCode to FormalExpressions
    code_elements = analysis_results_element.get('_ProgrammingCode_elements', [])
    if code_elements:
        formal_expressions = []
        for code_elem in code_elements:
            formal_expr = convert_programming_code_to_formal_expression(code_elem)
            formal_expressions.append(formal_expr)
        if formal_expressions:
            analysis_result['formalExpressions'] = formal_expressions
    
    return analysis_result