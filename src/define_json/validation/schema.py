"""
Schema validation for Define-JSON format.

Basic validation of Define-JSON structure and CDISC compliance patterns.
"""

from typing import Dict, List, Any


def validate_define_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic validation of Define-JSON structure.
    
    Args:
        data: Define-JSON data to validate
        
    Returns:
        Dictionary with validation results including valid status, errors, and warnings
    """
    validation = {
        'valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check required fields
    required_top_level = ['metadata', 'Datasets', 'Variables']
    for field in required_top_level:
        if field not in data:
            validation['errors'].append(f"Missing required field: {field}")
            validation['valid'] = False
    
    # Check required metadata fields
    metadata = data.get('metadata', {})
    required_metadata = ['studyOID', 'studyName']
    for field in required_metadata:
        if field not in metadata:
            validation['errors'].append(f"Missing required metadata field: {field}")
            validation['valid'] = False
    
    # Check OID patterns
    datasets = data.get('Datasets', [])
    for ds in datasets:
        if not ds.get('OID', '').startswith('IG.'):
            validation['warnings'].append(f"Dataset OID should start with 'IG.': {ds.get('OID')}")
    
    variables = data.get('Variables', [])
    for var in variables:
        if not var.get('OID', '').startswith('IT.'):
            validation['warnings'].append(f"Variable OID should start with 'IT.': {var.get('OID')}")
    
    # Check data type consistency
    valid_data_types = {'text', 'integer', 'float', 'double', 'boolean', 'date', 'time', 'datetime'}
    for var in variables:
        data_type = var.get('dataType')
        if data_type and data_type not in valid_data_types:
            validation['warnings'].append(f"Unknown data type '{data_type}' for variable {var.get('OID')}")
    
    # Check ItemRef integrity
    all_variable_oids = {var.get('OID') for var in variables}
    for ds in datasets:
        for item_ref in ds.get('items', []):
            item_oid = item_ref.get('itemOID')
            if item_oid and item_oid not in all_variable_oids:
                validation['errors'].append(f"ItemRef references undefined variable: {item_oid}")
                validation['valid'] = False
    
    return validation
