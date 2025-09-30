"""
Define-XML to Define-JSON converter.

Converter with no external dependencies that transforms Define-XML
files into Define-JSON format while preserving all semantic information.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class DefineXMLToJSONConverter:
    """Define-XML to Define-JSON converter with no external dependencies."""
    
    def __init__(self):
        self.namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        # Additional namespaces for backward compatibility
        self.legacy_namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.2',
            'def': 'http://www.cdisc.org/ns/def/v1.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
    
    def _detect_namespaces(self, root: ET.Element) -> Dict[str, str]:
        """Auto-detect which namespace version to use based on the XML root element."""
        # Extract namespace from the root tag
        root_tag = root.tag
        if root_tag.startswith('{'):
            # Extract namespace URI from tag like {http://...}ODM
            namespace_end = root_tag.find('}')
            root_namespace = root_tag[1:namespace_end]
        else:
            root_namespace = None
        
        # Determine which namespace set to use based on detected ODM namespace
        if root_namespace and 'v1.2' in root_namespace:
            return self.legacy_namespaces
        elif root_namespace and 'v1.3' in root_namespace:
            return self.namespaces
        else:
            # Try to find namespace declarations in attributes for prefixed namespaces
            for attr_name, attr_value in root.attrib.items():
                if 'def' in attr_name and 'v1.0' in attr_value:
                    return self.legacy_namespaces
                elif 'def' in attr_name and ('v2.0' in attr_value or 'v2.1' in attr_value):
                    return self.namespaces
            
            # Default to current namespaces
            return self.namespaces
    
    def convert_file(self, xml_path: Path, output_path: Path) -> Dict[str, Any]:
        """Convert Define-XML file to Define-JSON."""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Auto-detect namespace version and use appropriate namespaces
        active_namespaces = self._detect_namespaces(root)
        # Update the instance namespaces to use the detected ones
        self.namespaces = active_namespaces
        
        # Find Study and MetaDataVersion
        study = root.find('.//odm:Study', active_namespaces)
        mdv = root.find('.//odm:MetaDataVersion', active_namespaces)
        
        if not study or not mdv:
            raise ValueError("Could not find Study or MetaDataVersion in Define-XML")
        
        # Build Define-JSON structure with metadata directly in MetaDataVersion
        define_json = {
            # ODM File Metadata (from ODMFileMetadata mixin)
            'fileOID': root.get('FileOID'),
            'asOfDateTime': root.get('AsOfDateTime'),
            'creationDateTime': root.get('CreationDateTime'),
            'odmVersion': root.get('ODMVersion'),
            'fileType': root.get('FileType'),
            'originator': root.get('Originator'),
            'sourceSystem': root.get('SourceSystem'),
            'sourceSystemVersion': root.get('SourceSystemVersion'),
            'context': root.get('{%s}Context' % active_namespaces['def']),
            'defineVersion': mdv.get('{%s}DefineVersion' % active_namespaces['def']),
            
            # Study Metadata (from StudyMetadata mixin)
            'studyOID': study.get('OID'),
            'studyName': self._get_study_name(study),
            'studyDescription': self._get_study_description(study),
            'protocolName': self._get_protocol_name(study),
            
            # MetaDataVersion attributes (from GovernedElement)
            'OID': mdv.get('OID'),
            'name': mdv.get('Name', mdv.get('OID')),
            'description': mdv.get('Description', '')
        }
        
        # Process methods first to get derivation method map for linking
        methods, derivation_method_map = self._process_methods(mdv)
        define_json['methods'] = methods
        
        # Process main elements according to Define-JSON schema
        define_json['itemGroups'] = self._process_item_groups_with_hierarchy(mdv, derivation_method_map)
        define_json['items'] = self._process_items(mdv)  # Top-level items not in any group
        define_json['codeLists'] = self._process_code_lists(mdv)
        
        # Process conditions and where clauses with proper separation
        conditions_and_where_clauses = self._process_conditions_and_where_clauses(mdv)
        define_json['conditions'] = conditions_and_where_clauses['conditions']
        define_json['whereClauses'] = conditions_and_where_clauses['whereClauses']
        define_json['standards'] = self._process_standards(mdv)
        define_json['annotatedCRF'] = self._process_annotated_crf(mdv)
        
        # Process semantic concept elements
        define_json['concepts'] = self._process_reified_concepts(mdv)
        define_json['conceptProperties'] = self._process_concept_properties(mdv)
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(define_json, f, indent=2)
        
        return define_json
    
    def _process_item_groups_with_hierarchy(self, mdv: ET.Element, derivation_method_map: Dict[str, Dict] = None) -> List[Dict[str, Any]]:
        """Process ItemGroupDef elements with proper hierarchical nesting of ValueLists."""
        # First, process domain-level ItemGroups
        domain_item_groups = self._process_domain_item_groups(mdv, derivation_method_map)
        
        # Then, create ValueList ItemGroups as children
        value_list_item_groups = self._process_value_lists_as_item_groups(mdv, derivation_method_map)
        
        # Add ValueList OID references as children of their parent domains
        for domain_ig in domain_item_groups:
            domain = domain_ig.get('domain', '')
            if domain:
                # Find ValueList OIDs that belong to this domain
                domain_value_list_oids = [vl.get('OID') for vl in value_list_item_groups 
                                        if vl.get('OID', '').startswith(f'VL.{domain}.')]
                if domain_value_list_oids:
                    domain_ig['children'] = domain_value_list_oids  # Store OID references, not objects
        
        # Return all ItemGroups (both domain and ValueList) at top level - no redundancy
        return domain_item_groups + value_list_item_groups
    
    def _process_domain_item_groups(self, mdv: ET.Element, derivation_method_map: Dict[str, Dict] = None) -> List[Dict[str, Any]]:
        """Process domain-level ItemGroupDef elements."""
        item_groups = []
        for ig in mdv.findall('.//odm:ItemGroupDef', self.namespaces):
            # Build item group with only non-null values
            item_group = {
                'OID': ig.get('OID'),
                'name': ig.get('Name'),
                'items': []
            }
            
            # Add description (prefer def:Label, fallback to Description, make meaningful)
            description = ig.get('{%s}Label' % self.namespaces['def']) or self._get_description(ig)
            if not description and ig.get('Domain'):
                description = f"{ig.get('Domain')} domain dataset containing clinical data"
            if description:
                item_group['description'] = description
            
            # Add non-null attributes
            if ig.get('Domain'):
                item_group['domain'] = ig.get('Domain')
            if ig.get('{%s}Structure' % self.namespaces['def']):
                item_group['structure'] = ig.get('{%s}Structure' % self.namespaces['def'])
            if ig.get('{%s}Class' % self.namespaces['def']):
                item_group['class'] = ig.get('{%s}Class' % self.namespaces['def'])
            if ig.get('Repeating') == 'Yes':
                item_group['repeating'] = True
            if ig.get('SASDatasetName'):
                item_group['sasDatasetName'] = ig.get('SASDatasetName')
            if ig.get('{%s}ArchiveLocationID' % self.namespaces['def']):
                item_group['archiveLocationID'] = ig.get('{%s}ArchiveLocationID' % self.namespaces['def'])
            
            # Process ItemRefs - embed full Item objects for schema conformance
            for item_ref in ig.findall('odm:ItemRef', self.namespaces):
                item_oid = item_ref.get('ItemOID')
                
                # Find the corresponding ItemDef
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.namespaces)
                if item_def is not None:
                    # Create full Item object according to schema
                    item_data = self._create_full_item_object(item_def, item_ref, derivation_method_map)
                    item_group['items'].append(item_data)
            
            # Note: ValueList references are handled at the ItemDef level via def:ValueListRef
            # ItemGroups do not directly reference ValueLists in Define-XML standard
            
            item_groups.append(item_group)
        
        return item_groups
    
    def _create_full_item_object(self, item_def: ET.Element, item_ref: ET.Element = None, derivation_method_map: Dict[str, Dict] = None) -> Dict[str, Any]:
        """Create a full Item object according to Define-JSON schema."""
        # Build item with all properties from ItemDef
        item_dict = {
            'OID': item_def.get('OID'),
            'name': item_def.get('Name')
        }
        
        # Add description (prefer def:Label, fallback to Description)
        description = item_def.get('{%s}Label' % self.namespaces['def']) or self._get_description(item_def)
        if description:
            item_dict['description'] = description
        
        # Add required dataType
        if item_def.get('DataType'):
            item_dict['dataType'] = item_def.get('DataType')
        
        # Add non-null attributes
        if item_def.get('Length'):
            try:
                item_dict['length'] = int(item_def.get('Length'))
            except (ValueError, TypeError):
                pass
        if item_def.get('SignificantDigits'):
            try:
                item_dict['significantDigits'] = int(item_def.get('SignificantDigits'))
            except (ValueError, TypeError):
                pass
        
        # Add origin if present
        origin = self._get_origin(item_def)
        if origin and any(v for v in origin.values() if v):
            item_dict['origin'] = origin
        
        # Add ItemRef-specific properties if provided
        if item_ref is not None:
            if item_ref.get('Mandatory'):
                item_dict['mandatory'] = item_ref.get('Mandatory', 'No')
            if item_ref.get('Role'):
                item_dict['role'] = item_ref.get('Role')
            
            # Add WhereClause reference
            where_clause_ref = item_ref.find('def:WhereClauseRef', self.namespaces)
            if where_clause_ref is not None:
                item_dict['whereClause'] = where_clause_ref.get('WhereClauseOID')
        
        # Link to auto-generated methods based on derivation descriptions
        if derivation_method_map:
            item_dict = self._link_variables_to_auto_methods(item_dict, derivation_method_map)
        
        return item_dict
    
    def _process_value_lists_as_item_groups(self, mdv: ET.Element, derivation_method_map: Dict[str, Dict] = None) -> List[Dict[str, Any]]:
        """Process ValueListDef elements as ItemGroups with DataSpecialization type."""
        value_list_item_groups = []
        
        # First, collect all items from all ValueLists
        all_items = {}
        for vl in mdv.findall('.//def:ValueListDef', self.namespaces):
            item_refs = vl.findall('odm:ItemRef', self.namespaces)

            for item_ref in item_refs:
                item_oid = item_ref.get('ItemOID')
                
                # Find the corresponding ItemDef
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.namespaces)
                if item_def is not None:
                    # Extract parameter from ItemOID (e.g., IT.VS.VSORRES.TEMP -> VS.TEMP)
                    parts = item_oid.split('.')
                    if len(parts) >= 4:
                        domain = parts[1]  # VS or LB
                        variable = parts[2]  # VSORRES, VSORRESU, LBORRES, LBORRESU
                        parameter = parts[3]  # TEMP, WEIGHT, ALT, etc.

                        param_key = f'{domain}.{parameter}'
                        if param_key not in all_items:
                            all_items[param_key] = []

                        # Create full Item object with ValueList-specific properties
                        item_data = self._create_full_item_object(item_def, item_ref, derivation_method_map)
                        
                        # For Dataset Specialization: Use shared WhereClause for same parameter
                        shared_where_clause = f'WC.{domain}.{parameter}'
                        item_data['whereClause'] = shared_where_clause
                        item_data['variable'] = variable

                        all_items[param_key].append(item_data)

        # Create ValueList ItemGroups grouped by parameter (Dataset Specialization style)
        for param_key, items in sorted(all_items.items()):
            domain, parameter = param_key.split('.')

            # Build ValueList ItemGroup with meaningful description and shared WhereClause
            value_list_item_group = {
                'OID': f'VL.{domain}.{parameter}',
                'name': f'VL.{domain}.{parameter}',
                'description': f'Dataset specialization for {domain} {parameter} parameter containing both result values and units',
                'type': 'DataSpecialization',
                'domain': domain,
                'items': items
            }
            
            # Add reference to the shared WhereClause (using inlined=false approach)
            shared_wc_oid = f'WC.{domain}.{parameter}'
            value_list_item_group['whereClause'] = shared_wc_oid

            value_list_item_groups.append(value_list_item_group)

        return value_list_item_groups
    
    def _process_items(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ItemDef elements that are NOT referenced in any ItemGroup (top-level items only)."""
        # First, collect all ItemOIDs that are referenced in ItemGroups
        referenced_item_oids = set()
        for ig in mdv.findall('.//odm:ItemGroupDef', self.namespaces):
            for item_ref in ig.findall('.//odm:ItemRef', self.namespaces):
                referenced_item_oids.add(item_ref.get('ItemOID'))
        
        # Also collect ItemOIDs referenced in ValueLists
        for vl in mdv.findall('.//def:ValueListDef', self.namespaces):
            for item_ref in vl.findall('.//odm:ItemRef', self.namespaces):
                referenced_item_oids.add(item_ref.get('ItemOID'))
        
        # Only process ItemDefs that are NOT referenced anywhere (true top-level items)
        items = []
        for item in mdv.findall('.//odm:ItemDef', self.namespaces):
            item_oid = item.get('OID')
            if item_oid not in referenced_item_oids:
                # Build item with only non-null values
                item_dict = {
                    'OID': item.get('OID'),
                    'name': item.get('Name')
                }
                
                # Add description (prefer def:Label, fallback to Description)
                description = item.get('{%s}Label' % self.namespaces['def']) or self._get_description(item)
                if description:
                    item_dict['description'] = description
                
                # Add non-null attributes
                if item.get('DataType'):
                    item_dict['dataType'] = item.get('DataType')
                if item.get('Length'):
                    try:
                        item_dict['length'] = int(item.get('Length'))
                    except (ValueError, TypeError):
                        pass
                if item.get('SignificantDigits'):
                    try:
                        item_dict['significantDigits'] = int(item.get('SignificantDigits'))
                    except (ValueError, TypeError):
                        pass
                
                # Add origin if present
                origin = self._get_origin(item)
                if origin and any(v for v in origin.values() if v):  # Only add if origin has content
                    item_dict['origin'] = origin
                
                items.append(item_dict)
        return items
    
    def _process_value_lists(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ValueListDef elements with Dataset Specialization grouping by parameter."""
        # First, collect all items from all ValueLists
        all_items = {}

        for vl in mdv.findall('.//def:ValueListDef', self.namespaces):
            item_refs = vl.findall('odm:ItemRef', self.namespaces)

            for item_ref in item_refs:
                item_oid = item_ref.get('ItemOID')
                where_clause_ref = item_ref.find('def:WhereClauseRef', self.namespaces)
                where_clause_oid = where_clause_ref.get('WhereClauseOID') if where_clause_ref is not None else None

                # Extract parameter from ItemOID (e.g., IT.VS.VSORRES.TEMP -> VS.TEMP)
                parts = item_oid.split('.')
                if len(parts) >= 4:
                    domain = parts[1]  # VS or LB
                    variable = parts[2]  # VSORRES, VSORRESU, LBORRES, LBORRESU
                    parameter = parts[3]  # TEMP, WEIGHT, ALT, etc.

                    param_key = f'{domain}.{parameter}'
                    if param_key not in all_items:
                        all_items[param_key] = []

                    # For Dataset Specialization: Use shared WhereClause for same parameter
                    # Both LBORRES.AST and LBORRESU.AST should use WC.LB.AST
                    shared_where_clause = f'WC.{domain}.{parameter}'

                    all_items[param_key].append({
                        'itemOID': item_oid,
                        'mandatory': item_ref.get('Mandatory', 'No'),
                        'whereClause': shared_where_clause,  # Use shared WhereClause
                        'variable': variable
                    })

        # Create ValueLists grouped by parameter (Dataset Specialization style)
        value_lists = []
        for param_key, items in sorted(all_items.items()):
            domain, parameter = param_key.split('.')

            value_list = {
                'OID': f'VL.{domain}.{parameter}',
                'name': f'VL.{domain}.{parameter}',
                'description': f'Value list for {domain} {parameter} parameter',
                'items': items
            }

            value_lists.append(value_list)

        return value_lists
    
    def _process_code_lists(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process CodeList elements."""
        code_lists = []
        for cl in mdv.findall('.//odm:CodeList', self.namespaces):
            code_list = {
                'oid': cl.get('OID'),
                'name': cl.get('Name'),
                'dataType': cl.get('DataType'),
                'items': []
            }
            
            # Process CodeListItems
            for cli in cl.findall('.//odm:CodeListItem', self.namespaces):
                code_list['items'].append({
                    'codedValue': cli.get('CodedValue'),
                    'decode': self._get_decode(cli)
                })
            
            code_lists.append(code_list)
        
        return code_lists
    
    def _process_conditions_and_where_clauses(self, mdv: ET.Element) -> Dict[str, List[Dict[str, Any]]]:
        """Process WhereClauseDef elements with proper Condition separation."""
        conditions = []
        where_clauses = []
        processed_parameters = set()
        
        # First, collect all original WhereClauses
        original_where_clauses = {}
        for wc in mdv.findall('.//def:WhereClauseDef', self.namespaces):
            range_checks = []
            for rc in wc.findall('.//odm:RangeCheck', self.namespaces):
                check_value = rc.find('.//odm:CheckValue', self.namespaces)
                if check_value is not None:
                    range_checks.append({
                        'comparator': rc.get('Comparator', 'EQ'),
                        'checkValues': [check_value.text or '']
                    })
            
            original_where_clauses[wc.get('OID')] = {
                'range_checks': range_checks,
                'description': self._get_description(wc)
            }
        
        # Create shared Conditions and WhereClauses for Dataset Specialization
        for wc_oid, wc_data in original_where_clauses.items():
            # Parse OID like WC.LB.LBORRES.AST -> extract LB.AST
            parts = wc_oid.split('.')
            if len(parts) >= 4:
                domain = parts[1]  # LB, VS
                parameter = parts[3]  # AST, TEMP, etc.
                param_key = f'{domain}.{parameter}'
                
                if param_key not in processed_parameters:
                    processed_parameters.add(param_key)
                    
                    # Create shared Condition with proper rangeChecks
                    condition_oid = f'COND.{domain}.{parameter}'
                    
                    # Build range checks based ONLY on what exists in original XML
                    range_checks = []
                    for rc in wc_data['range_checks']:
                        if rc['checkValues'][0]:  # Only if there's a value
                            param_value = rc['checkValues'][0]
                            
                            # Primary parameter check (only create what actually exists)
                            range_checks.append({
                                'item': f'IT.{domain}.{domain}TESTCD',  # e.g., IT.VS.VSTESTCD
                                'comparator': 'EQ',
                                'checkValues': [param_value]
                            })
                            
                            # DO NOT add fabricated domain context - only preserve what's in original XML
                    
                    # Create the Condition
                    conditions.append({
                        'OID': condition_oid,
                        'name': f'{parameter}_condition',
                        'description': f'Condition for {domain} {parameter} parameter',
                        'rangeChecks': range_checks
                    })
                    
                    # Create the WhereClause that references this Condition
                    where_clauses.append({
                        'OID': f'WC.{domain}.{parameter}',
                        'name': f'{parameter}Context',
                        'description': f'When {parameter} applies in {domain} domain',
                        'conditions': [condition_oid]  # Reference to the Condition
                    })
        
        return {
            'conditions': conditions,
            'whereClauses': where_clauses
        }
    
    def _process_methods(self, mdv: ET.Element) -> tuple[List[Dict[str, Any]], Dict[str, Dict]]:
        """Process MethodDef elements, ComputationMethod elements, and auto-generate methods from derivations."""
        methods = []
        
        # Process standard MethodDef elements (Define-XML v2.1)
        for method in mdv.findall('.//odm:MethodDef', self.namespaces):
            methods.append({
                'OID': method.get('OID'),
                'name': method.get('Name'),
                'type': method.get('Type'),
                'description': self._get_description(method)
            })
        
        # Process ComputationMethod elements (Define-XML v1.0, common in ADaM)
        computation_methods = self._process_computation_methods(mdv)
        methods.extend(computation_methods)
        
        # Auto-generate methods from derivation descriptions
        auto_methods, derivation_method_map = self._auto_generate_methods_from_derivations(mdv)
        methods.extend(auto_methods)
        
        return methods, derivation_method_map

    def _auto_generate_methods_from_derivations(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Auto-generate Method objects from ItemDef derivation descriptions."""
        # Collect all derivation descriptions
        derivation_descriptions = {}
        method_counter = 1
        
        # Process all ItemDef elements to find derivation patterns
        item_defs = mdv.findall('.//odm:ItemDef', self.namespaces)
        
        for item_def in item_defs:
            comment_attr = item_def.get('Comment', '')
            
            # Skip simple predecessor references - focus on complex derivations
            if comment_attr and len(comment_attr) > 30:  # Complex derivations
                # Normalize the description for matching
                normalized_desc = comment_attr.strip()
                
                # Skip simple dataset references
                simple_patterns = [
                    lambda x: x.count('.') == 1 and len(x) < 20,  # Simple "DM.STUDYID" 
                    lambda x: x.startswith('ADSL.') and len(x) < 30,  # Simple ADSL refs
                    lambda x: x.count(' ') < 3 and '=' not in x  # Short, no logic
                ]
                
                is_simple = any(pattern(normalized_desc) for pattern in simple_patterns)
                
                if not is_simple:
                    if normalized_desc not in derivation_descriptions:
                        # Create new method
                        method_oid = f'MT.DERIVATION.{method_counter:03d}'
                        derivation_descriptions[normalized_desc] = {
                            'OID': method_oid,
                            'name': f'Derivation Method {method_counter}',
                            'type': 'Derivation',
                            'description': normalized_desc,
                            'variables': []
                        }
                        method_counter += 1
                    
                    # Add variable to this method
                    var_name = item_def.get('Name')
                    var_oid = item_def.get('OID')
                    if var_name:
                        derivation_descriptions[normalized_desc]['variables'].append({
                            'name': var_name,
                            'oid': var_oid
                        })
        
        # Convert to method list and add variable count info
        auto_methods = []
        for desc, method_info in derivation_descriptions.items():
            method_dict = {
                'OID': method_info['OID'],
                'name': method_info['name'],
                'type': method_info['type'],
                'description': method_info['description']
            }
            
            # Add metadata about which variables use this method
            var_count = len(method_info['variables'])
            if var_count > 1:
                # Create better naming: "{Var1} derivation ({Domain1}.{Var1}, {Domain2}.{Var2})"
                variables = method_info['variables']
                
                # Get the primary variable name (most common or first)
                var_names = [v['name'] for v in variables]
                primary_var = max(set(var_names), key=var_names.count) if var_names else 'Variable'
                
                # Create domain.variable format for each variable
                domain_vars = []
                for v in variables[:5]:  # Limit to first 5 to avoid overly long names
                    var_oid = v['oid']
                    if '.' in var_oid:
                        domain = var_oid.split('.')[0]
                        domain_vars.append(f'{domain}.{v["name"]}')
                    else:
                        domain_vars.append(v['name'])
                
                if var_count > 5:
                    domain_vars.append(f'... and {var_count - 5} more')
                
                method_dict['name'] = f'{primary_var} derivation ({", ".join(domain_vars)})'
            
            auto_methods.append(method_dict)
        
        return auto_methods, derivation_descriptions

    def _link_variables_to_auto_methods(self, item_dict: Dict[str, Any], derivation_methods: Dict[str, Dict]) -> Dict[str, Any]:
        """Link variables to auto-generated methods based on their derivation descriptions."""
        origin = item_dict.get('origin', {})
        description = origin.get('description', '')
        
        if description and len(description) > 30:
            # Check if this description matches an auto-generated method
            normalized_desc = description.strip()
            if normalized_desc in derivation_methods:
                method_oid = derivation_methods[normalized_desc]['OID']
                item_dict['method'] = method_oid
        
        return item_dict

    def _process_standards(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process def:Standards elements."""
        standards = []
        standards_section = mdv.find('.//def:Standards', self.namespaces)
        if standards_section is not None:
            for standard in standards_section.findall('.//def:Standard', self.namespaces):
                standards.append({
                    'OID': standard.get('OID'),
                    'name': standard.get('Name'),
                    'type': standard.get('Type'),
                    'version': standard.get('Version'),
                    'status': standard.get('Status'),
                    'publishingSet': standard.get('PublishingSet')
                })
        return standards
    
    def _process_annotated_crf(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process def:AnnotatedCRF elements."""
        annotated_crf = []
        crf_section = mdv.find('.//def:AnnotatedCRF', self.namespaces)
        if crf_section is not None:
            for doc_ref in crf_section.findall('.//def:DocumentRef', self.namespaces):
                annotated_crf.append({
                    'leafID': doc_ref.get('leafID'),
                    'title': doc_ref.get('title') or 'Annotated CRF'  # Default title
                })
        return annotated_crf
    
    def _process_reified_concepts(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ReifiedConcept elements (semantic concepts)."""
        concepts = []
        # Note: Define-XML doesn't typically contain ReifiedConcepts directly
        # This would be populated from external concept definitions or extensions
        # For now, return empty list - can be extended when Define-XML includes semantic concepts
        return concepts
    
    def _process_concept_properties(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ConceptProperty elements (concept properties)."""
        concept_properties = []
        # Note: Define-XML doesn't typically contain ConceptProperties directly
        # This would be populated from external concept definitions or extensions
        # For now, return empty list - can be extended when Define-XML includes semantic concepts
        return concept_properties
    
    def _get_study_name(self, study: ET.Element) -> str:
        """Extract study name from GlobalVariables."""
        if study is None:
            return None
        global_vars = study.find('odm:GlobalVariables', self.namespaces)
        if global_vars is not None:
            study_name = global_vars.find('odm:StudyName', self.namespaces)
            if study_name is not None:
                return study_name.text
        return None
    
    def _get_study_description(self, study: ET.Element) -> str:
        """Extract study description from GlobalVariables."""
        if study is None:
            return None
        global_vars = study.find('odm:GlobalVariables', self.namespaces)
        if global_vars is not None:
            study_desc = global_vars.find('odm:StudyDescription', self.namespaces)
            if study_desc is not None:
                return study_desc.text
        return None
    
    def _get_protocol_name(self, study: ET.Element) -> str:
        """Extract protocol name from GlobalVariables."""
        if study is None:
            return None
        global_vars = study.find('odm:GlobalVariables', self.namespaces)
        if global_vars is not None:
            protocol = global_vars.find('odm:ProtocolName', self.namespaces)
            if protocol is not None:
                return protocol.text
        return None
    
    def _get_description(self, element: ET.Element) -> str:
        """Extract description from TranslatedText."""
        desc = element.find('.//odm:Description/odm:TranslatedText', self.namespaces)
        return desc.text if desc is not None else ''
    
    def _get_decode(self, element: ET.Element) -> str:
        """Extract decode from TranslatedText."""
        decode = element.find('.//odm:Decode/odm:TranslatedText', self.namespaces)
        return decode.text if decode is not None else ''
    
    def _get_origin(self, element: ET.Element) -> Dict[str, Any]:
        """Extract origin information from both Origin elements and ItemDef attributes."""
        origin = {}
        
        # First check for def:Origin child element (Define-XML v2.1 style)
        origin_elem = element.find('.//def:Origin', self.namespaces)
        if origin_elem is not None:
            origin['type'] = origin_elem.get('Type')
            origin['source'] = origin_elem.get('Source')
            
            # Get description from Origin element
            desc_elem = origin_elem.find('odm:Description', self.namespaces)
            if desc_elem is not None:
                trans_text = desc_elem.find('odm:TranslatedText', self.namespaces)
                if trans_text is not None and trans_text.text:
                    origin['description'] = trans_text.text
        
        # Also check for Origin attribute on ItemDef (Define-XML v1.0 style, common in ADaM)
        origin_attr = element.get('Origin')
        if origin_attr:
            if not origin.get('type'):  # Don't override if already set from element
                origin['type'] = origin_attr
        
        # Check for Comment attribute (ADaM predecessor information)
        comment_attr = element.get('Comment')
        if comment_attr:
            if origin.get('description'):
                # Combine if we already have description from Origin element
                origin['description'] = f"{origin['description']} | Predecessor: {comment_attr}"
            else:
                # Use comment as predecessor description
                origin['description'] = comment_attr
            
            # If this looks like a predecessor reference, mark it as such
            # Override "Derived" type for clear predecessor references
            if ('.' in comment_attr and not comment_attr.startswith('Derived')) or 'ADSL.' in comment_attr:
                origin['type'] = 'Predecessor'
        
        return origin

    def _process_computation_methods(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ComputationMethod elements (Define-XML v1.0 style)."""
        methods = []
        
        # Look for def:ComputationMethod elements
        comp_methods = mdv.findall('.//def:ComputationMethod', self.namespaces)
        
        for method in comp_methods:
            method_dict = {
                'OID': method.get('OID')
            }
            
            # Add name if present
            if method.get('Name'):
                method_dict['name'] = method.get('Name')
            
            # Add type - for ComputationMethod, typically "Computation"
            method_dict['type'] = 'Computation'
            
            # Add description from the method text content
            if method.text and method.text.strip():
                method_dict['description'] = method.text.strip()
            
            methods.append(method_dict)
        
        return methods
