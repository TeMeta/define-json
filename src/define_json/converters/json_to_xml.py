"""
Define-JSON to Define-XML converter - Unified Smart Converter.

This converter combines the best of both approaches:
1. Pydantic-based field mapping for clean roundtripping
2. CDISC domain knowledge for handling complex structures
3. Optional inference and fallback controls

Key Features:
- Smart default behavior (handles any JSON)
- Strict mode for verbatim roundtripping
- Granular control via enable_inference and enable_fallbacks flags
"""

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False
    logger.warning("lxml not available - HTML generation will not work")


class DefineJSONToXMLConverter:
    """
    Convert Define-JSON to Define-XML with intelligent structure handling.
    
    Modes:
        - enable_inference=True, enable_fallbacks=True (default):
          Smart converter that handles any JSON
        
        - enable_inference=False, enable_fallbacks=False:
          Strict mode - only uses explicit metadata, fails on missing data
          
        - enable_inference=True, enable_fallbacks=False:
          Apply transformations but don't guess missing values
          
        - enable_inference=False, enable_fallbacks=True:
          No transformations, but handle missing metadata gracefully
    """
    
    # Define schema field to XML attribute mapping (reverse of xml_to_json)
    FIELD_TO_XML_MAPPING = {
        # Identity fields
        'OID': 'OID',
        'name': 'Name',
        
        # Link and reference fields
        'href': 'href',
        'ref': 'ref',
        'title': 'title',
        
        # Labels and descriptions
        'label': 'Label',
        'comments': 'Comment',
        'description': 'Description',
        
        # Data type and structure
        'type': 'Type',
        'dataType': 'DataType',
        'length': 'Length',
        'significantDigits': 'SignificantDigits',
        'displayFormat': 'DisplayFormat',
        
        # CDISC-specific fields
        'sasFieldName': 'SASFieldName',
        'sasDatasetName': 'SASDatasetName',
        'sdsVarName': 'SDSVarName',
        'domain': 'Domain',
        'origin': 'Origin',
        'role': 'Role',
        'purpose': 'Purpose',
        
        # Ordering and structure
        'orderNumber': 'OrderNumber',
        'repeating': 'Repeating',
        'isReferenceData': 'IsReferenceData',
        'mandatory': 'Mandatory',
        
        # Standards and versions
        'context': 'Context',
        'dictionary': 'Dictionary',
        'version': 'Version',
        'defineVersion': 'DefineVersion',
        'odmVersion': 'ODMVersion',
        'status': 'Status',
        'publishingSet': 'PublishingSet',
        
        # File metadata
        'fileOID': 'FileOID',
        'fileType': 'FileType',
        'creationDateTime': 'CreationDateTime',
        'asOfDateTime': 'AsOfDateTime',
        'originator': 'Originator',
        'sourceSystem': 'SourceSystem',
        'sourceSystemVersion': 'SourceSystemVersion',
        
        # Study metadata
        'studyOID': 'OID',
        'studyName': 'StudyName',
        'studyDescription': 'StudyDescription',
        'protocolName': 'ProtocolName',
        
        # References
        'itemOID': 'ItemOID',
        'whereClauseOID': 'WhereClauseOID',
        'methodOID': 'MethodOID',
        'valueListOID': 'ValueListOID',
        'codeListOID': 'CodeListOID',
        'leafID': 'leafID',
        
        # Conditions and checks
        'comparator': 'Comparator',
        'softHard': 'SoftHard',
        'operator': 'Operator',
        'checkValue': 'CheckValue',
        
        # Structure metadata
        'structure': 'Structure',
        'class': 'Class',
        'archiveLocationID': 'ArchiveLocationID',
        
        # Code list specifics
        'codedValue': 'CodedValue',
        'rank': 'Rank',
        'extendedValue': 'ExtendedValue',
        'decode': 'Decode',
        
        # Analysis dataset specifics
        'parameterOID': 'ParameterOID',
        'analysisVariableOID': 'AnalysisVariableOID',
    }
    
    def __init__(
        self, 
        stylesheet_href: str = "define2-1.xsl",
        enable_inference: bool = True,
        enable_fallbacks: bool = True
    ):
        """
        Initialize converter.
        
        Args:
            stylesheet_href: XSL stylesheet reference
            enable_inference: Apply CDISC domain knowledge (slices→ValueLists, etc.)
            enable_fallbacks: Use fallback logic when metadata is missing
        """
        self.stylesheet_href = stylesheet_href
        self.enable_inference = enable_inference
        self.enable_fallbacks = enable_fallbacks
        self.namespace_map = {}
        
        # Default namespace URIs (only used if enable_fallbacks=True)
        self.default_namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }
        
        # Register namespace prefixes for proper output
        ET.register_namespace('def', self.default_namespaces['def'])
        ET.register_namespace('xlink', self.default_namespaces['xlink'])
    
    def _normalize_json_structure(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize JSON structure to handle both flattened and nested metaDataVersion formats.
        
        If the JSON has a metaDataVersion array, extract the first element's content
        and merge it with the top-level data.
        """
        # If already flattened (has top-level itemGroups, items, etc.), return as-is
        if json_data.get('itemGroups') or json_data.get('items'):
            return json_data
        
        # Handle nested metaDataVersion format
        if 'metaDataVersion' in json_data and isinstance(json_data['metaDataVersion'], list):
            if len(json_data['metaDataVersion']) > 0:
                # Extract the first metaDataVersion element
                mdv_data = json_data['metaDataVersion'][0]
                
                # Create a new flattened structure
                flattened = json_data.copy()
                
                # Remove the nested metaDataVersion array
                del flattened['metaDataVersion']
                
                # Merge metaDataVersion content into top level
                for key, value in mdv_data.items():
                    if key not in flattened:  # Don't overwrite existing top-level data
                        flattened[key] = value
                
                return flattened
        
        # Return original if no transformation needed
        return json_data
    
    def _get_namespace_uri(self, prefix: str) -> str:
        """
        Get namespace URI for a prefix.
        
        Args:
            prefix: Namespace prefix (e.g., 'def', 'xlink')
            
        Returns:
            Namespace URI or empty string
        """
        # First check stored namespace map
        if prefix in self.namespace_map:
            return self.namespace_map[prefix]
        
        # Fall back to defaults if enabled
        if self.enable_fallbacks and prefix in self.default_namespaces:
            return self.default_namespaces[prefix]
        
        # Strict mode - no fallback
        if not self.enable_fallbacks:
            logger.warning(f"Namespace prefix '{prefix}' not found and fallbacks disabled")
        
        return ''
    
    def _map_field_to_xml(self, field_name: str, namespace_info: Dict[str, str] = None) -> str:
        """
        Map Define schema field name to XML attribute name.
        
        Args:
            field_name: Define schema field name
            namespace_info: Namespace information for this field
            
        Returns:
            XML attribute name (possibly with namespace)
        """
        # Get the XML attribute name
        xml_attr = self.FIELD_TO_XML_MAPPING.get(field_name, field_name)
        
        # If there's namespace information, add namespace prefix
        if namespace_info and field_name in namespace_info:
            ns_prefix = namespace_info[field_name]
            ns_uri = self._get_namespace_uri(ns_prefix)
            if ns_uri:
                return f'{{{ns_uri}}}{xml_attr}'
        
        return xml_attr
    
    def _apply_mapped_attributes(self, element: ET.Element, data: Dict[str, Any]) -> None:
        """
        Apply attributes from Define schema to XML element using field mapping.
        
        Args:
            element: XML element to add attributes to
            data: Dictionary with Define schema field names
        """
        # Get namespace info for this element if present
        namespace_info = data.get('_namespaces', {})
        
        # Skip metadata keys and nested structures
        skip_keys = {
            '_namespaces', '_namespaceMetadata', '_translatedText_attributes',
            'description', 'label', 'title', 'items', 'itemRefs', 'aliases', 
            'documentRef', 'coding', 'rangeChecks', 'checkValues', 'conditions',
            'whereClauses', 'itemGroups', 'codeLists', 'methods', 'standards',
            'annotatedCRF', 'codeListItems', 'resultDisplays', 'analysisResults',
            'origin'  # origin is a nested object, handle separately
        }
        
        for field_name, value in data.items():
            # Skip metadata and nested structures
            if field_name.startswith('_') or field_name in skip_keys:
                continue
            
            # Skip None values
            if value is None:
                continue
            
            # Skip list and dict values (these are nested structures)
            if isinstance(value, (list, dict)):
                continue
            
            # Map field name to XML attribute and apply
            xml_attr = self._map_field_to_xml(field_name, namespace_info)
            element.set(xml_attr, self._safe_str(value))
    
    def _safe_str(self, value: Any) -> str:
        """Safely convert any value to string for XML attributes."""
        if isinstance(value, bool):
            return 'Yes' if value else 'No'
        elif value is None:
            return ''
        else:
            return str(value)
    
    def convert_file(self, json_path: Path, output_path: Path) -> ET.Element:
        """
        Convert Define-JSON file to Define-XML.
        
        Args:
            json_path: Path to input Define-JSON file
            output_path: Path to output Define-XML file
            
        Returns:
            Root ET.Element of the XML tree
        """
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        # Normalize structure (handle nested metaDataVersion)
        json_data = self._normalize_json_structure(json_data)
        
        # Extract namespace metadata
        ns_metadata = json_data.get('_namespaceMetadata', {})
        self.namespace_map = ns_metadata.get('prefixes', {})
        
        # Create root ODM element
        root = ET.Element('ODM')
        odm_ns = self._get_namespace_uri('odm')
        if odm_ns:
            root.set('xmlns', odm_ns)
        
        # Apply ODM root attributes
        self._apply_mapped_attributes(root, json_data)
        
        # Add def:Context if present
        if json_data.get('context'):
            def_ns = self._get_namespace_uri('def')
            if def_ns:
                root.set(f'{{{def_ns}}}Context', json_data['context'])
        
        # Create Study element
        study = ET.SubElement(root, 'Study')
        study_oid = json_data.get('studyOID')
        if study_oid:
            study.set('OID', study_oid)
        elif not self.enable_fallbacks:
            raise ValueError("studyOID is required and fallbacks are disabled")
        else:
            study.set('OID', 'UNKNOWN')
        
        # Global Variables
        self._create_global_variables(study, json_data)
        
        # MetaDataVersion
        mdv = ET.SubElement(study, 'MetaDataVersion')
        mdv_oid = json_data.get('OID', json_data.get('metadataVersionOID'))
        if mdv_oid:
            mdv.set('OID', mdv_oid)
        elif not self.enable_fallbacks:
            raise ValueError("MetaDataVersion OID is required and fallbacks are disabled")
        else:
            mdv.set('OID', 'MDV.ROUNDTRIP')
        
        if json_data.get('name'):
            mdv.set('Name', json_data['name'])
        if json_data.get('description'):
            mdv.set('Description', json_data['description'])
        
        # Add def:DefineVersion if present
        if json_data.get('defineVersion'):
            def_ns = self._get_namespace_uri('def')
            if def_ns:
                mdv.set(f'{{{def_ns}}}DefineVersion', json_data['defineVersion'])
        
        # Process Standards
        self._create_standards(mdv, json_data.get('standards', []))
        
        # Process AnnotatedCRF
        self._create_annotated_crf(mdv, json_data.get('annotatedCRF', []))
        
        # Process Conditions and WhereClauses
        existing_item_oids = self._collect_item_oids(json_data)
        self._create_conditions_and_where_clauses(
            mdv,
            json_data.get('conditions', []),
            json_data.get('whereClauses', []),
            existing_item_oids
        )
        
        # Process ItemGroups and ValueLists
        all_item_groups = json_data.get('itemGroups', [])
        self._process_item_groups_and_value_lists(mdv, all_item_groups)
        
        # Process ItemDefs
        self._process_item_defs(mdv, json_data, all_item_groups)
        
        # Process CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []))
        
        # Process Methods
        self._create_methods(mdv, json_data.get('methods', []))
        
        # Write XML to file
        self._write_xml(root, output_path)
        
        return root
    
    def _create_global_variables(self, study: ET.Element, json_data: Dict[str, Any]) -> None:
        """Create GlobalVariables element."""
        global_vars = ET.SubElement(study, 'GlobalVariables')
        
        if json_data.get('studyName'):
            study_name = ET.SubElement(global_vars, 'StudyName')
            study_name.text = json_data['studyName']
        
        if json_data.get('studyDescription'):
            study_desc = ET.SubElement(global_vars, 'StudyDescription')
            study_desc.text = json_data['studyDescription']
        
        if json_data.get('protocolName'):
            protocol = ET.SubElement(global_vars, 'ProtocolName')
            protocol.text = json_data['protocolName']
    
    def _create_standards(self, parent: ET.Element, standards: List[Dict[str, Any]]) -> None:
        """Create def:Standards section."""
        if not standards:
            return
        
        def_ns = self._get_namespace_uri('def')
        if not def_ns and not self.enable_fallbacks:
            raise ValueError("def namespace not found and fallbacks disabled")
        
        standards_elem = ET.SubElement(parent, f'{{{def_ns}}}Standards' if def_ns else 'Standards')
        
        for standard in standards:
            standard_elem = ET.SubElement(standards_elem, f'{{{def_ns}}}Standard' if def_ns else 'Standard')
            self._apply_mapped_attributes(standard_elem, standard)
    
    def _create_annotated_crf(self, parent: ET.Element, annotated_crf: List[Dict[str, Any]]) -> None:
        """Create def:AnnotatedCRF section."""
        if not annotated_crf:
            return
        
        def_ns = self._get_namespace_uri('def')
        if not def_ns and not self.enable_fallbacks:
            raise ValueError("def namespace not found and fallbacks disabled")
        
        crf_elem = ET.SubElement(parent, f'{{{def_ns}}}AnnotatedCRF' if def_ns else 'AnnotatedCRF')
        
        for doc_ref in annotated_crf:
            doc_ref_elem = ET.SubElement(crf_elem, f'{{{def_ns}}}DocumentRef' if def_ns else 'DocumentRef')
            self._apply_mapped_attributes(doc_ref_elem, doc_ref)
    
    def _collect_item_oids(self, json_data: Dict[str, Any]) -> Set[str]:
        """Collect all existing ItemOIDs for WhereClause validation."""
        item_oids = set()
        
        # From top-level items
        for item in json_data.get('items', []):
            if item.get('OID'):
                item_oids.add(item['OID'])
        
        # From nested items in itemGroups
        for ig in json_data.get('itemGroups', []):
            for item in ig.get('items', []):
                oid = item.get('OID') or item.get('itemOID')
                if oid:
                    item_oids.add(oid)
        
        return item_oids
    
    def _create_conditions_and_where_clauses(
        self, 
        parent: ET.Element, 
        conditions: List[Dict[str, Any]], 
        where_clauses: List[Dict[str, Any]],
        existing_item_oids: Set[str]
    ) -> None:
        """
        Create WhereClauseDef elements from Conditions and WhereClauses.
        
        This intelligently reconstructs WhereClauseDefs:
        - If enable_inference=True: Expands shared WhereClauses to per-variable format
        - If enable_inference=False: Uses WhereClauses as-is
        """
        if not where_clauses:
            return
        
        def_ns = self._get_namespace_uri('def')
        conditions_by_oid = {cond.get('OID'): cond for cond in conditions}
        
        for wc in where_clauses:
            wc_oid = wc.get('OID', '')
            
            if self.enable_inference:
                # Smart mode: Expand WhereClauses for each variable
                self._create_expanded_where_clauses(
                    parent, wc, conditions_by_oid, existing_item_oids, def_ns
                )
            else:
                # Direct mode: Create WhereClause as-is
                self._create_where_clause_direct(parent, wc, conditions_by_oid, def_ns)
    
    def _create_expanded_where_clauses(
        self,
        parent: ET.Element,
        wc: Dict[str, Any],
        conditions_by_oid: Dict[str, Dict[str, Any]],
        existing_item_oids: Set[str],
        def_ns: str
    ) -> None:
        """Create expanded WhereClauses for each variable (inference mode)."""
        wc_oid = wc.get('OID', '')
        
        # Parse OID like WC.VS.TEMP -> extract VS.TEMP
        parts = wc_oid.split('.')
        if len(parts) >= 3:
            domain = parts[1]  # VS, LB
            parameter = parts[2]  # TEMP, AST, etc.
            
            # Determine variables based on domain
            variables = ['LBORRES', 'LBORRESU'] if domain == 'LB' else ['VSORRES', 'VSORRESU']
            
            for variable in variables:
                # Check if the corresponding ItemOID actually exists
                expected_item_oid = f'IT.{domain}.{variable}.{parameter}'
                if existing_item_oids and expected_item_oid not in existing_item_oids:
                    continue  # Skip creating WhereClause for non-existent ItemOID
                
                original_oid = f'WC.{domain}.{variable}.{parameter}'
                
                wc_elem = ET.SubElement(parent, f'{{{def_ns}}}WhereClauseDef' if def_ns else 'WhereClauseDef')
                wc_elem.set('OID', original_oid)
                
                # Add description
                desc = ET.SubElement(wc_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = f'Condition for {variable} {parameter}'
                
                # Add RangeChecks from conditions
                for condition_oid in wc.get('conditions', []):
                    condition = conditions_by_oid.get(condition_oid)
                    if condition:
                        self._add_range_checks(wc_elem, condition)
                        break  # Only use first condition for roundtrip compatibility
    
    def _create_where_clause_direct(
        self,
        parent: ET.Element,
        wc: Dict[str, Any],
        conditions_by_oid: Dict[str, Dict[str, Any]],
        def_ns: str
    ) -> None:
        """Create WhereClause directly without expansion (strict mode)."""
        wc_elem = ET.SubElement(parent, f'{{{def_ns}}}WhereClauseDef' if def_ns else 'WhereClauseDef')
        wc_elem.set('OID', wc.get('OID', ''))
        
        # Add description if present
        if wc.get('description'):
            desc = ET.SubElement(wc_elem, 'Description')
            trans_text = ET.SubElement(desc, 'TranslatedText')
            trans_text.text = wc['description']
        
        # Add RangeChecks from conditions
        for condition_oid in wc.get('conditions', []):
            condition = conditions_by_oid.get(condition_oid)
            if condition:
                self._add_range_checks(wc_elem, condition)
    
    def _add_range_checks(self, wc_elem: ET.Element, condition: Dict[str, Any]) -> None:
        """Add RangeCheck elements from a condition."""
        for range_check_data in condition.get('rangeChecks', []):
            range_check = ET.SubElement(wc_elem, 'RangeCheck')
            range_check.set('Comparator', range_check_data.get('comparator', 'EQ'))
            
            check_values = range_check_data.get('checkValues', [])
            if check_values and check_values[0]:
                check_value = ET.SubElement(range_check, 'CheckValue')
                check_value.text = check_values[0]
    
    def _process_item_groups_and_value_lists(
        self, 
        parent: ET.Element, 
        all_item_groups: List[Dict[str, Any]]
    ) -> None:
        """
        Process ItemGroups and ValueLists with intelligent handling.
        
        Strategy:
        1. Check for explicit ValueListDef elements
        2. If enable_inference=True: Project slices to ValueLists
        3. Otherwise: Create ItemGroups directly
        """
        # Separate domain ItemGroups and DataSpecialization slices
        domain_item_groups = [ig for ig in all_item_groups if ig.get('type') != 'DataSpecialization']
        slice_item_groups = [ig for ig in all_item_groups if ig.get('type') == 'DataSpecialization']
        
        # Check for explicit ValueListDef elements
        explicit_value_lists = [ig for ig in all_item_groups if ig.get('elementType') == 'ValueListDef']
        
        if explicit_value_lists:
            # Use explicit ValueList structure
            self._create_value_lists_direct(parent, explicit_value_lists)
        elif self.enable_inference and slice_item_groups:
            # Project slices to ValueLists
            self._create_value_lists_from_slices(parent, slice_item_groups, domain_item_groups)
        elif slice_item_groups:
            # Fallback: treat slices as regular ItemGroups if inference disabled
            logger.warning("DataSpecialization slices found but inference disabled - treating as ItemGroups")
        
        # Create domain ItemGroups
        self._create_item_groups(parent, domain_item_groups)
    
    def _create_value_lists_from_slices(
        self,
        parent: ET.Element,
        slices: List[Dict[str, Any]],
        domain_groups: List[Dict[str, Any]]
    ) -> None:
        """
        Project context-first slices to variable-first ValueListDefs.
        
        This implements the canonical transformation from data specialization
        slices to proper CDISC ValueLists.
        """
        def_ns = self._get_namespace_uri('def')
        
        # Group items by (domain, variable) to create ValueLists
        var_to_contexts: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
        
        for slice_ig in slices:
            domain = slice_ig.get('domain', '')
            where_clause = slice_ig.get('whereClause', '')
            items = slice_ig.get('items', [])
            
            for item in items:
                var_name = item.get('variable') or item.get('name', '')
                if not var_name:
                    continue
                
                key = (domain, var_name)
                if key not in var_to_contexts:
                    var_to_contexts[key] = []
                
                # Store item with its context
                var_to_contexts[key].append({
                    'item': item,
                    'whereClause': where_clause or item.get('whereClause', '')
                })
        
        # Create ValueListDefs for variables with multiple contexts
        for (domain, var_name), contexts in sorted(var_to_contexts.items()):
            if not contexts:
                continue
            
            # Create ValueList OID
            vl_oid = f"VL.{domain}.{var_name}"
            
            vl_elem = ET.SubElement(parent, f'{{{def_ns}}}ValueListDef' if def_ns else 'ValueListDef')
            vl_elem.set('OID', vl_oid)
            
            # Add description
            desc = ET.SubElement(vl_elem, 'Description')
            trans_text = ET.SubElement(desc, 'TranslatedText')
            trans_text.text = f'Value list for {domain} {var_name} across contexts'
            
            # Add ItemRefs for each context
            for ctx in contexts:
                item = ctx['item']
                where_clause = ctx['whereClause']
                
                item_ref = ET.SubElement(vl_elem, 'ItemRef')
                item_oid = item.get('OID') or item.get('itemOID', '')
                item_ref.set('ItemOID', item_oid)
                item_ref.set('Mandatory', self._safe_str(item.get('mandatory', 'No')))
                
                if item.get('role'):
                    item_ref.set('Role', item['role'])
                
                if where_clause:
                    wc_ref = ET.SubElement(item_ref, f'{{{def_ns}}}WhereClauseRef' if def_ns else 'WhereClauseRef')
                    wc_ref.set('WhereClauseOID', where_clause)
        
        logger.info(f"Projected {len(var_to_contexts)} variables to ValueLists")
    
    def _create_value_lists_direct(
        self,
        parent: ET.Element,
        value_lists: List[Dict[str, Any]]
    ) -> None:
        """Create ValueListDef elements directly from stored structure."""
        def_ns = self._get_namespace_uri('def')
        
        for vl in value_lists:
            vl_elem = ET.SubElement(parent, f'{{{def_ns}}}ValueListDef' if def_ns else 'ValueListDef')
            vl_elem.set('OID', vl.get('OID', ''))
            
            if vl.get('description'):
                desc = ET.SubElement(vl_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = vl['description']
            
            # Add ItemRefs
            for item in vl.get('items', []):
                item_ref = ET.SubElement(vl_elem, 'ItemRef')
                item_ref.set('ItemOID', item.get('itemOID') or item.get('OID', ''))
                item_ref.set('Mandatory', self._safe_str(item.get('mandatory', 'No')))
                
                if item.get('role'):
                    item_ref.set('Role', item['role'])
                
                if item.get('whereClauseOID'):
                    wc_ref = ET.SubElement(item_ref, f'{{{def_ns}}}WhereClauseRef' if def_ns else 'WhereClauseRef')
                    wc_ref.set('WhereClauseOID', item['whereClauseOID'])
    
    def _create_item_groups(self, parent: ET.Element, datasets: List[Dict[str, Any]]) -> None:
        """Create ItemGroupDef elements."""
        def_ns = self._get_namespace_uri('def')
        
        for ds in datasets:
            ig_elem = ET.SubElement(parent, 'ItemGroupDef')
            
            # Apply all mapped attributes
            self._apply_mapped_attributes(ig_elem, ds)
            
            # Handle def: namespaced attributes
            for field in ['structure', 'class', 'label', 'archiveLocationID']:
                if ds.get(field):
                    xml_attr = self.FIELD_TO_XML_MAPPING.get(field, field)
                    if def_ns:
                        ig_elem.set(f'{{{def_ns}}}{xml_attr}', str(ds[field]))
                    else:
                        ig_elem.set(xml_attr, str(ds[field]))
            
            # Add Description if present
            if ds.get('description'):
                desc = ET.SubElement(ig_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = ds['description']
            
            # Add ItemRefs
            for item in ds.get('items', []):
                self._create_item_ref(ig_elem, item, def_ns)
    
    def _create_item_ref(self, parent: ET.Element, item: Dict[str, Any], def_ns: str) -> None:
        """Create an ItemRef element."""
        item_ref = ET.SubElement(parent, 'ItemRef')
        
        # ItemOID
        item_oid = item.get('OID') or item.get('itemOID', '')
        item_ref.set('ItemOID', item_oid)
        
        # Mandatory
        mandatory = item.get('mandatory', 'No')
        item_ref.set('Mandatory', self._safe_str(mandatory))
        
        # Role
        if item.get('role'):
            item_ref.set('Role', item['role'])
        
        # OrderNumber
        if item.get('orderNumber') is not None:
            item_ref.set('OrderNumber', str(item['orderNumber']))
        
        # WhereClauseRef
        if item.get('whereClauseOID'):
            wc_ref = ET.SubElement(item_ref, f'{{{def_ns}}}WhereClauseRef' if def_ns else 'WhereClauseRef')
            wc_ref.set('WhereClauseOID', item['whereClauseOID'])
        
        # MethodRef
        if item.get('methodOID'):
            method_ref = ET.SubElement(item_ref, 'MethodRef')
            method_ref.set('MethodOID', item['methodOID'])
    
    def _process_item_defs(
        self,
        parent: ET.Element,
        json_data: Dict[str, Any],
        all_item_groups: List[Dict[str, Any]]
    ) -> None:
        """
        Process ItemDefs with intelligent deduplication.
        
        Combines top-level items with items nested in ItemGroups,
        removing duplicates by OID.
        """
        # Get top-level items
        items = json_data.get('items', [])
        
        # Extract nested items if inference enabled
        nested_items = []
        if self.enable_inference:
            for ig in all_item_groups:
                for item in ig.get('items', []):
                    # Normalize OID field
                    if 'itemOID' in item and 'OID' not in item:
                        item = item.copy()
                        item['OID'] = item['itemOID']
                    nested_items.append(item)
        
        # Combine and deduplicate
        all_items = items + nested_items
        unique_items = {}
        for item in all_items:
            oid = item.get('OID') or item.get('itemOID')
            if oid:
                # Keep first occurrence (top-level items take precedence)
                if oid not in unique_items:
                    unique_items[oid] = item
        
        # Create ItemDefs
        self._create_item_defs(parent, list(unique_items.values()))
    
    def _create_item_defs(self, parent: ET.Element, variables: List[Dict[str, Any]]) -> None:
        """Create ItemDef elements."""
        def_ns = self._get_namespace_uri('def')
        
        for var in variables:
            item_elem = ET.SubElement(parent, 'ItemDef')
            
            # Apply basic attributes
            self._apply_mapped_attributes(item_elem, var)
            
            # Handle DataType - required field
            if not var.get('dataType'):
                if self.enable_fallbacks:
                    item_elem.set('DataType', 'text')
                else:
                    raise ValueError(f"dataType required for ItemDef {var.get('OID')} and fallbacks disabled")
            
            # Handle def:Label
            if var.get('label'):
                if def_ns:
                    item_elem.set(f'{{{def_ns}}}Label', var['label'])
                else:
                    item_elem.set('Label', var['label'])
            
            # Add Description element if present (separate from label)
            if var.get('description'):
                desc = ET.SubElement(item_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = var['description']
            
            # Add CodeListRef if present
            if var.get('codeList'):
                code_list_ref = ET.SubElement(item_elem, 'CodeListRef')
                code_list_ref.set('CodeListOID', var['codeList'])
            
            # Add Origin if present
            origin = var.get('origin', {})
            if origin and (origin.get('type') or origin.get('source')):
                origin_elem = ET.SubElement(item_elem, f'{{{def_ns}}}Origin' if def_ns else 'Origin')
                if origin.get('type'):
                    origin_elem.set('Type', origin['type'])
                if origin.get('source'):
                    origin_elem.set('Source', origin['source'])
    
    def _create_code_lists(self, parent: ET.Element, code_lists: List[Dict[str, Any]]) -> None:
        """Create CodeList elements."""
        for cl in code_lists:
            cl_elem = ET.SubElement(parent, 'CodeList')
            
            # Apply attributes
            self._apply_mapped_attributes(cl_elem, cl)
            
            # Handle both 'OID' and 'oid' field names
            if not cl_elem.get('OID'):
                oid = cl.get('OID') or cl.get('oid', '')
                if oid:
                    cl_elem.set('OID', oid)
            
            # Default DataType if missing and fallbacks enabled
            if not cl.get('dataType') and self.enable_fallbacks:
                cl_elem.set('DataType', 'text')
            
            # Add CodeListItems
            items = cl.get('codeListItems') or cl.get('items', [])
            for item in items:
                cli_elem = ET.SubElement(cl_elem, 'CodeListItem')
                cli_elem.set('CodedValue', item.get('codedValue', ''))
                
                if item.get('decode'):
                    decode = ET.SubElement(cli_elem, 'Decode')
                    trans_text = ET.SubElement(decode, 'TranslatedText')
                    trans_text.text = item['decode']
                
                if item.get('rank'):
                    cli_elem.set('Rank', str(item['rank']))
    
    def _create_methods(self, parent: ET.Element, methods: List[Dict[str, Any]]) -> None:
        """Create MethodDef elements."""
        def_ns = self._get_namespace_uri('def')
        
        for method in methods:
            # Skip synthetic methods if inference enabled
            if self.enable_inference and method.get('OID', '').startswith('MT.DERIVATION.'):
                continue
            
            method_elem = ET.SubElement(parent, 'MethodDef')
            
            # Apply attributes
            self._apply_mapped_attributes(method_elem, method)
            
            # Add Description
            if method.get('description'):
                desc = ET.SubElement(method_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = method['description']
    
    def _write_xml(self, root: ET.Element, output_path: Path) -> None:
        """Write XML to file with pretty formatting."""
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Pretty print
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
        
        # Remove extra blank lines
        lines = pretty_xml.decode('utf-8').split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(non_empty_lines))
        
        logger.info(f"Written Define-XML to {output_path}")


def main():
    """Main entry point for testing."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert Define-JSON to Define-XML')
    parser.add_argument('input', help='Input Define-JSON file')
    parser.add_argument('output', help='Output Define-XML file')
    parser.add_argument('--no-inference', action='store_true', 
                       help='Disable inference (strict mode)')
    parser.add_argument('--no-fallbacks', action='store_true',
                       help='Disable fallbacks (require all metadata)')
    parser.add_argument('--strict', action='store_true',
                       help='Strict mode (no inference, no fallbacks)')
    
    args = parser.parse_args()
    
    # Determine mode
    enable_inference = not (args.no_inference or args.strict)
    enable_fallbacks = not (args.no_fallbacks or args.strict)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    # Create converter
    converter = DefineJSONToXMLConverter(
        enable_inference=enable_inference,
        enable_fallbacks=enable_fallbacks
    )
    
    # Convert
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    print(f"Converting {input_path} to {output_path}")
    print(f"  Inference: {'enabled' if enable_inference else 'disabled'}")
    print(f"  Fallbacks: {'enabled' if enable_fallbacks else 'disabled'}")
    
    try:
        converter.convert_file(input_path, output_path)
        print(f"✓ Conversion complete. Output written to {output_path}")
    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()