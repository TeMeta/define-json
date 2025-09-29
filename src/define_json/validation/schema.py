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
    
    # Check required fields (now flattened with mixins)
    required_top_level = ['itemGroups', 'items']
    for field in required_top_level:
        if field not in data:
            validation['errors'].append(f"Missing required field: {field}")
            validation['valid'] = False
    
    # Check required fields from StudyMetadata mixin
    required_study_fields = ['studyOID']
    for field in required_study_fields:
        if field not in data:
            validation['errors'].append(f"Missing required field: {field}")
            validation['valid'] = False
    
    # Check required fields from ODMFileMetadata mixin
    required_file_fields = ['fileOID', 'creationDateTime', 'odmVersion', 'fileType']
    for field in required_file_fields:
        if field not in data:
            validation['errors'].append(f"Missing required field: {field}")
            validation['valid'] = False
    
    # Check OID patterns
    item_groups = data.get('itemGroups', [])
    for ig in item_groups:
        if not ig.get('OID', '').startswith(('IG.', 'VL.')):
            validation['warnings'].append(f"ItemGroup OID should start with 'IG.' or 'VL.': {ig.get('OID')}")
    
    items = data.get('items', [])
    for item in items:
        if not item.get('OID', '').startswith('IT.'):
            validation['warnings'].append(f"Item OID should start with 'IT.': {item.get('OID')}")
    
    # Check Condition and WhereClause OID patterns
    conditions = data.get('conditions', [])
    for cond in conditions:
        if not cond.get('OID', '').startswith('COND.'):
            validation['warnings'].append(f"Condition OID should start with 'COND.': {cond.get('OID')}")
    
    where_clauses = data.get('whereClauses', [])
    for wc in where_clauses:
        if not wc.get('OID', '').startswith('WC.'):
            validation['warnings'].append(f"WhereClause OID should start with 'WC.': {wc.get('OID')}")
    
    # Check data type consistency
    valid_data_types = {'text', 'integer', 'float', 'double', 'boolean', 'date', 'time', 'datetime'}
    for item in items:
        data_type = item.get('dataType')
        if data_type and data_type not in valid_data_types:
            validation['warnings'].append(f"Unknown data type '{data_type}' for item {item.get('OID')}")
    
    # Check ItemRef integrity
    all_item_oids = {item.get('OID') for item in items}
    for ig in item_groups:
        for item_ref in ig.get('items', []):
            item_oid = item_ref.get('itemOID')
            if item_oid and item_oid not in all_item_oids:
                validation['errors'].append(f"ItemRef references undefined item: {item_oid}")
                validation['valid'] = False
    
    # Check Condition references in WhereClauses
    all_condition_oids = {cond.get('OID') for cond in conditions}
    for wc in where_clauses:
        for condition_oid in wc.get('conditions', []):
            if condition_oid not in all_condition_oids:
                validation['errors'].append(f"WhereClause references undefined condition: {condition_oid}")
                validation['valid'] = False
    
    return validation
