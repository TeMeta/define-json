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
            enable_inference: Apply CDISC domain knowledge (slices -> ValueLists, etc.)
            enable_fallbacks: Use fallback logic when metadata is missing
        """
        self.stylesheet_href = stylesheet_href
        self.enable_inference = enable_inference
        self.enable_fallbacks = enable_fallbacks
        self.namespace_map = {}
        self.supplemental_data = {}
        
        # Default namespace URIs (only used if enable_fallbacks=True)
        self.default_namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }
        
        # Don't register namespaces here - they'll be registered in convert_file
        # with the actual namespace URIs from the JSON metadata
    
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
    
    def _apply_mapped_attributes(self, element: ET.Element, data: Dict[str, Any], element_type: str = None) -> None:
        """
        Apply attributes from Define schema to XML element using field mapping.
        
        Args:
            element: XML element to add attributes to
            data: Dictionary with Define schema field names
            element_type: Type of element ('ODM', 'Study', 'MetaDataVersion', etc.) for context-specific handling
        """
        # Get namespace info for this element if present
        namespace_info = data.get('_namespaces', {})
        
        # Get def namespace for special handling
        def_ns = self._get_namespace_uri('def')
        
        # Fields that should have def: namespace in CDISC standards
        # These apply to ItemGroupDef elements
        def_namespaced_fields = {
            'structure', 'class', 'label', 'archiveLocationID'
            # Note: standardOID and commentOID are handled explicitly in _create_item_groups and _create_code_lists
            # to ensure correct casing (StandardOID, CommentOID with capital letters)
        }
        
        # Skip metadata keys and nested structures
        skip_keys = {
            '_namespaces', '_xmlMetadata', '_translatedText_attributes',
            'description', 'label', 'title', 'items', 'itemRefs', 'aliases', 
            'documentRef', 'coding', 'rangeChecks', 'checkValues', 'conditions',
            'whereClauses', 'itemGroups', 'codeLists', 'methods', 'standards',
            'annotatedCRF', 'codeListItems', 'resultDisplays', 'analysisResults',
            'origin',  # origin is a nested object, handle separately
            'codeList',  # codeList is handled as CodeListRef child element
            'mandatory',  # mandatory is handled explicitly in ItemRef creation, skip in ItemDef
            'role',  # role is ItemRef attribute, not ItemDef - handled explicitly in ItemRef creation
            'method',  # method is handled as MethodOID on ItemRef, not ItemDef attribute
            'wasDerivedFrom',  # wasDerivedFrom is provenance, handled as ExternalCodeList, not XML attribute
            # Skip def: namespaced fields that are handled explicitly with correct casing
            'defClass', 'defDomainKeys', 'comment',
            'standardOID', 'commentOID', 'isNonStandard', 'hasNoData',  # Handled explicitly to ensure correct namespace (def:StandardOID, def:CommentOID, def:IsNonStandard, def:HasNoData)
            'leaf', 'externalCodeList', 'sourceResourceOID', 'leafID',
            'displayFormat',  # displayFormat (def:DisplayFormat) is handled explicitly for ItemDefs
            'classIsAttribute',  # classIsAttribute is metadata to track attribute vs element form
            'sasFieldName',  # sasFieldName is handled explicitly based on hasSASFieldName flag
        }
        
        # Context-specific field exclusions
        # For ODM element, skip 'OID' field as it represents MetaDataVersion OID, not FileOID
        # Also skip study metadata that belongs in GlobalVariables, not ODM
        if element_type == 'ODM':
            skip_keys = skip_keys | {
                'OID', 'studyOID', 'metadataVersionOID',
                'name', 'studyName', 'studyDescription', 'protocolName', 'defineVersion'
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
            
            # Map field name to XML attribute
            xml_attr = self.FIELD_TO_XML_MAPPING.get(field_name, field_name)
            
            # Apply namespace prefix if this is a def: namespaced field and we're not at ODM root
            if field_name in def_namespaced_fields and def_ns and element.tag != 'ODM':
                element.set(f'{{{def_ns}}}{xml_attr}', self._safe_str(value))
            else:
                # Check if there's specific namespace info for this field
                if namespace_info and field_name in namespace_info:
                    ns_prefix = namespace_info[field_name]
                    ns_uri = self._get_namespace_uri(ns_prefix)
                    if ns_uri:
                        element.set(f'{{{ns_uri}}}{xml_attr}', self._safe_str(value))
                    else:
                        element.set(xml_attr, self._safe_str(value))
                else:
                    element.set(xml_attr, self._safe_str(value))
    
    def _safe_str(self, value: Any) -> str:
        """Safely convert any value to string for XML attributes."""
        if isinstance(value, bool):
            return 'Yes' if value else 'No'
        elif value is None:
            return ''
        else:
            return str(value)
    
    def _merge_supplemental_data(self, item: Dict[str, Any], category: str) -> Dict[str, Any]:
        """
        Merge supplemental data from _xmlMetadata into an item.
        
        Args:
            item: The item dictionary (e.g., itemGroup, codeList)
            category: The category of supplemental data ('itemGroup', 'codeList', etc.)
            
        Returns:
            A new dictionary with supplemental data merged in
        """
        merged = item.copy()
        item_oid = item.get('OID')
        
        if item_oid and category in self.supplemental_data:
            supp = self.supplemental_data[category].get(item_oid, {})
            # Merge supplemental data, but don't overwrite existing data
            for key, value in supp.items():
                if key not in merged or merged[key] is None:
                    merged[key] = value
        
        return merged
    
    def _create_translated_text(self, parent: ET.Element, text: str, lang: str = 'en') -> ET.Element:
        """
        Create a TranslatedText element with xml:lang attribute.
        
        Args:
            parent: Parent element to attach TranslatedText to
            text: Text content
            lang: Language code (default: 'en')
            
        Returns:
            The created TranslatedText element
        """
        trans_text = ET.SubElement(parent, 'TranslatedText')
        trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
        trans_text.text = text
        return trans_text
    
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
        xml_metadata = json_data.get('_xmlMetadata', {})
        self.namespace_map = xml_metadata.get('namespaces', {})
        self._current_xml_metadata = xml_metadata  # Store for access in methods
        self._current_json_data = json_data  # Store JSON data for Dictionary lookup
        self.supplemental_data = {
            'itemGroup': xml_metadata.get('itemGroupSupplemental', {}),
            'codeList': xml_metadata.get('codeListSupplemental', {}),
            'method': xml_metadata.get('methodSupplemental', {}),
            'condition': xml_metadata.get('conditionSupplemental', {})
        }
        
        # Register all namespaces from metadata with ElementTree
        # This will automatically add xmlns declarations when the namespace is used
        for prefix, uri in self.namespace_map.items():
            if uri:
                ET.register_namespace(prefix, uri)
        
        # Create root ODM element
        root = ET.Element('ODM')
        
        # Set default namespace (xmlns without prefix)
        odm_ns = self._get_namespace_uri('odm')
        if odm_ns:
            root.set('xmlns', odm_ns)
        
        # ElementTree will automatically add all xmlns declarations when namespaces are first used
        # We don't need to set them explicitly to avoid duplicates
        
        # Add xsi namespace and schemaLocation if present in metadata
        xsi_schema_location = xml_metadata.get('xsiSchemaLocation')
        if xsi_schema_location:
            root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation', xsi_schema_location)
        
        # Note: We don't manually add xmlns: declarations here because:
        # - xmlns:xsi is added automatically when we use xsi:schemaLocation above
        # - xmlns:def is added automatically when we use def: prefixed attributes
        # - xmlns:xlink is added automatically when we use xlink: prefixed attributes  
        # - xmlns:adamref (or arm) is added automatically when creating AnalysisResultDisplays
        # - Any other namespaces are added automatically when first used
        
        # Apply ODM root attributes (skip 'OID' which belongs to MetaDataVersion)
        self._apply_mapped_attributes(root, json_data, element_type='ODM')
        
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
        
        # Fix #1: Apply _odmMetadata to MetaDataVersion if available
        xml_metadata = json_data.get('_xmlMetadata', {})
        odm_metadata = xml_metadata.get('_odmMetadata', {})
        
        if odm_metadata.get('Name'):
            mdv.set('Name', odm_metadata['Name'])
        elif json_data.get('name'):
            mdv.set('Name', json_data['name'])
        
        if json_data.get('description'):
            mdv.set('Description', json_data['description'])
        
        # Add def:DefineVersion from _odmMetadata or top-level
        define_version = odm_metadata.get('DefineVersion') or json_data.get('defineVersion')
        if define_version:
            def_ns = self._get_namespace_uri('def')
            if def_ns:
                mdv.set(f'{{{def_ns}}}DefineVersion', define_version)
        
        # Add def:StandardName and def:StandardVersion from standards array
        # BUT only if Standards was NOT an element (i.e., it was represented as attributes)
        standards = json_data.get('standards', [])
        has_standards_element = xml_metadata.get('hasStandardsElement', False)
        
        if standards and len(standards) > 0 and not has_standards_element:
            standard = standards[0]
            def_ns = self._get_namespace_uri('def')
            if def_ns:
                # Map StandardName enum back to XML format
                standard_name = standard.get('name')
                if standard_name:
                    # Map enum values back to XML format
                    name_map = {
                        'ADaMIG': 'CDISC ADaM',
                        'SDTMIG': 'CDISC SDTM', 
                        'SENDIG': 'CDISC SEND',
                    }
                    xml_standard_name = name_map.get(standard_name, standard_name)
                    mdv.set(f'{{{def_ns}}}StandardName', xml_standard_name)
                
                if standard.get('version'):
                    mdv.set(f'{{{def_ns}}}StandardVersion', standard['version'])
        
        # Process Standards element (only if it was an element in the original)
        self._create_standards(mdv, json_data.get('standards', []))
        
        # Get xml_metadata early for AnnotatedCRF and other supplemental elements
        xml_metadata = json_data.get('_xmlMetadata', {})
        
        # Process AnnotatedCRF (from xml_metadata)
        annotated_crf_data = xml_metadata.get('annotatedCRF', {})
        if annotated_crf_data:
            self._create_annotated_crf(mdv, annotated_crf_data.get('documentRefs', []))
        
        # Process SupplementalDoc from DocumentReference objects in resources
        self._create_supplemental_doc(mdv, json_data)
        
        # Process AnalysisResultDisplays from native Display and Analysis objects
        self._create_analysis_result_displays_from_objects(mdv, json_data)
        
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
        # Process ItemGroups/ValueLists and get flattened list (includes nested slices)
        flattened_item_groups = self._process_item_groups_and_value_lists(mdv, all_item_groups, json_data)
        
        # Store flattened list for method reference collection
        self._flattened_item_groups = flattened_item_groups
        
        # Process ItemDefs using flattened list (includes items from nested ValueLists)
        self._process_item_defs(mdv, json_data, flattened_item_groups)
        
        # Process CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []))
        
        # Process Comments (def:CommentDef elements)
        # First, collect all CommentOID references from supplemental metadata
        xml_metadata = getattr(self, '_current_xml_metadata', {})
        referenced_comment_oids = set()
        
        # Collect from itemGroupSupplemental
        item_group_supp = xml_metadata.get('itemGroupSupplemental', {})
        item_origin_metadata = item_group_supp.get('_itemOriginMetadata', {})
        for item_metadata in item_origin_metadata.values():
            comment_oid = item_metadata.get('commentOID')
            if comment_oid:
                referenced_comment_oids.add(comment_oid)
        
        # Collect from conditionSupplemental
        condition_supplemental = xml_metadata.get('conditionSupplemental', {})
        for wc_supp in condition_supplemental.values():
            comment_oid = wc_supp.get('commentOID')
            if comment_oid:
                referenced_comment_oids.add(comment_oid)
        
        # Collect from codeListSupplemental
        code_list_supplemental = xml_metadata.get('codeListSupplemental', {})
        for cl_supp in code_list_supplemental.values():
            comment_oid = cl_supp.get('commentOID')
            if comment_oid:
                referenced_comment_oids.add(comment_oid)
        
        # Collect from standardSupplemental
        standard_supplemental = xml_metadata.get('standardSupplemental', {})
        for std_supp in standard_supplemental.values():
            comment_oid = std_supp.get('commentOID')
            if comment_oid:
                referenced_comment_oids.add(comment_oid)
        
        # Collect from itemGroupSupplemental (ItemGroupDef level)
        for ig_supp in item_group_supp.values():
            if isinstance(ig_supp, dict):
                comment_oid = ig_supp.get('commentOID')
                if comment_oid:
                    referenced_comment_oids.add(comment_oid)
        
        # Get explicit CommentDef data from supplemental
        comment_supplemental = xml_metadata.get('commentSupplemental', {})
        
        # Create CommentDef elements for all referenced CommentOIDs
        comments_to_create = {}
        
        # First, add explicit CommentDef data
        for comment_oid, comment_data in comment_supplemental.items():
            if isinstance(comment_data, dict) and 'OID' in comment_data:
                comments_to_create[comment_oid] = comment_data
        
        # Then, infer CommentDef for any referenced CommentOIDs that don't have explicit data
        for comment_oid in referenced_comment_oids:
            if comment_oid not in comments_to_create:
                # Create minimal CommentDef from the reference
                comments_to_create[comment_oid] = {
                    'OID': comment_oid,
                    'text': f'Comment referenced by CommentOID={comment_oid}'
                }
        
        if comments_to_create:
            self._create_comments(mdv, list(comments_to_create.values()))
        
        # Write MetaDataVersion Comment attribute if present
        mdv_comments = json_data.get('comments', [])
        if mdv_comments and len(mdv_comments) > 0:
            mdv.set('Comment', str(mdv_comments[0]))
        
        # Process Methods
        self._create_methods(mdv, json_data.get('methods', []))
        
        # Add MetaDataVersion-level leaf elements from resources (for display references)
        # Convert resources back to leaf elements
        resources = json_data.get('resources', [])
        if resources:
            # Collect all sourceResourceOIDs from ItemGroups to exclude them from mdv leaves
            item_groups = json_data.get('itemGroups', [])
            item_group_resource_oids = set()
            for ig in item_groups:
                ig_supp = xml_metadata.get('itemGroupSupplemental', {}).get(ig.get('OID', ''), {})
                if ig_supp.get('sourceResourceOID'):
                    item_group_resource_oids.add(ig_supp['sourceResourceOID'])
            
            # Filter resources that are from MetaDataVersion-level leaves only
            # (exclude those referenced by ItemGroups via sourceResourceOID)
            mdv_resources = [
                r for r in resources 
                if r.get('OID', '').startswith('RES.') 
                and r.get('OID') not in item_group_resource_oids
            ]
            mdv_leaves = []
            if mdv_resources:
                for resource in mdv_resources:
                    leaf_data = {
                        'ID': resource.get('OID', '').replace('RES.', ''),
                        'href': resource.get('href'),
                        'title': resource.get('label') or resource.get('name')
                    }
                    mdv_leaves.append(leaf_data)
            if mdv_leaves:
                self._create_mdv_leaves(mdv, mdv_leaves)
        
        # Also handle legacy mdvLeaves from _xmlMetadata
        mdv_leaves_legacy = xml_metadata.get('mdvLeaves', [])
        if mdv_leaves_legacy:
            self._create_mdv_leaves(mdv, mdv_leaves_legacy)
        
        # Write XML to file
        self._write_xml(root, output_path)
        
        return root
    
    def _create_global_variables(self, study: ET.Element, json_data: Dict[str, Any]) -> None:
        """Create GlobalVariables element."""
        global_vars = ET.SubElement(study, 'GlobalVariables')
        
        # Get values from _odmMetadata if present (these came from GlobalVariables in original)
        xml_metadata = json_data.get('_xmlMetadata', {})
        odm_metadata = xml_metadata.get('_odmMetadata', {})
        
        # Prefer _odmMetadata values (from original XML) over top-level values
        study_name = odm_metadata.get('StudyName') or json_data.get('studyName')
        if study_name:
            study_name_elem = ET.SubElement(global_vars, 'StudyName')
            study_name_elem.text = study_name
        
        study_desc = odm_metadata.get('StudyDescription') or json_data.get('studyDescription')
        if study_desc:
            study_desc_elem = ET.SubElement(global_vars, 'StudyDescription')
            study_desc_elem.text = study_desc
        
        protocol = odm_metadata.get('ProtocolName') or json_data.get('protocolName')
        if protocol:
            protocol_elem = ET.SubElement(global_vars, 'ProtocolName')
            protocol_elem.text = protocol
    
    def _create_standards(self, parent: ET.Element, standards: List[Dict[str, Any]]) -> None:
        """
        Create def:Standards section only if it existed as an element in the original XML.
        
        Standards can be represented as:
        1. Attributes on MetaDataVersion (def:StandardName, def:StandardVersion) - most common
        2. Child <Standards> element - less common
        
        We check _xmlMetadata to see if Standards was an element.
        """
        if not standards:
            return
        
        # Check if Standards element existed in original XML
        xml_metadata = getattr(self, '_current_xml_metadata', {})
        has_standards_element = xml_metadata.get('hasStandardsElement', False)
        
        # Only create Standards element if it was originally an element (not just attributes)
        if not has_standards_element:
            return
        
        def_ns = self._get_namespace_uri('def')
        if not def_ns and not self.enable_fallbacks:
            raise ValueError("def namespace not found and fallbacks disabled")
        
        standards_elem = ET.SubElement(parent, f'{{{def_ns}}}Standards' if def_ns else 'Standards')
        
        for standard in standards:
            standard_elem = ET.SubElement(standards_elem, f'{{{def_ns}}}Standard' if def_ns else 'Standard')
            
            # Handle Status and Type with proper case mapping
            standard_copy = dict(standard)
            
            # Map Status enum back to original case
            if 'status' in standard_copy:
                status_value = str(standard_copy['status'])
                # Reverse mapping: FINAL → Final, DRAFT → Draft
                if status_value == 'FINAL':
                    standard_copy['status'] = 'Final'
                elif status_value == 'DRAFT':
                    standard_copy['status'] = 'Draft'
            
            # Type is already in correct format (IG, CT, etc.) - just ensure it's uppercase if needed
            # Actually Type values like "IG", "CT" should remain as-is
            
            self._apply_mapped_attributes(standard_elem, standard_copy)
            
            # Add def:CommentOID from supplemental
            std_oid = standard.get('OID')
            if std_oid and def_ns:
                xml_metadata = getattr(self, '_current_xml_metadata', {})
                std_supp = xml_metadata.get('standardSupplemental', {}).get(std_oid, {})
                comment_oid = std_supp.get('commentOID')
                if comment_oid:
                    standard_elem.set(f'{{{def_ns}}}CommentOID', comment_oid)
    
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
            # Add leafID attribute (no namespace prefix needed)
            if doc_ref.get('leafID'):
                doc_ref_elem.set('leafID', doc_ref['leafID'])
            # Apply any other attributes
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
                self._create_translated_text(desc, f'Condition for {variable} {parameter}')
                
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
        
        # Add def:CommentOID from supplemental if present
        wc_oid = wc.get('OID')
        if wc_oid and def_ns:
            xml_metadata = getattr(self, '_current_xml_metadata', {})
            cond_supp = xml_metadata.get('conditionSupplemental', {}).get(wc_oid, {})
            comment_oid = cond_supp.get('commentOID')
            if comment_oid:
                wc_elem.set(f'{{{def_ns}}}CommentOID', comment_oid)
        
        # Add description if present
        if wc.get('description'):
            desc = ET.SubElement(wc_elem, 'Description')
            self._create_translated_text(desc, wc['description'])
        
        # Add RangeChecks from conditions
        for condition_oid in wc.get('conditions', []):
            condition = conditions_by_oid.get(condition_oid)
            if condition:
                self._add_range_checks(wc_elem, condition)
    
    def _add_range_checks(self, wc_elem: ET.Element, condition: Dict[str, Any]) -> None:
        """Add RangeCheck elements from a condition."""
        for range_check_data in condition.get('rangeChecks', []):
            range_check = ET.SubElement(wc_elem, 'RangeCheck')
            
            # SoftHard attribute (optional, written first for proper attribute order)
            if range_check_data.get('softHard'):
                range_check.set('SoftHard', range_check_data['softHard'])
            
            # RangeCheck uses 'def:ItemOID' attribute in Define-XML 2.x
            item_ref = range_check_data.get('item')
            if item_ref:
                # Use def:ItemOID for Define-XML 2.x
                def_ns = self._get_namespace_uri('def')
                if def_ns:
                    range_check.set(f'{{{def_ns}}}ItemOID', item_ref)
                else:
                    range_check.set('ItemOID', item_ref)
            
            # Comparator attribute
            range_check.set('Comparator', range_check_data.get('comparator', 'EQ'))
            
            # Add CheckValue child elements (Define-JSON stores as checkValues list)
            # Multiple CheckValue elements can exist per RangeCheck
            check_values = range_check_data.get('checkValues', [])
            for check_value in check_values:
                check_value_elem = ET.SubElement(range_check, 'CheckValue')
                check_value_elem.text = str(check_value)
            
    def _create_supplemental_doc(self, parent: ET.Element, json_data: Dict[str, Any]) -> None:
        """
        Create SupplementalDoc element from DocumentReference objects in resources.
        
        Args:
            parent: Parent MetaDataVersion element
            json_data: Full JSON data dict with resources array
        """
        # Extract DocumentReference objects from resources that came from SupplementalDoc
        # (identified by OID pattern DOC.SUPP.*)
        resources = json_data.get('resources', [])
        supp_doc_refs = [r for r in resources if isinstance(r, dict) and r.get('OID', '').startswith('DOC.SUPP.')]
        
        if not supp_doc_refs:
            return
        
        def_ns = self._get_namespace_uri('def')
        if not def_ns:
            logger.warning("def namespace not found, skipping SupplementalDoc")
            return
        
        supp_doc_elem = ET.SubElement(parent, f'{{{def_ns}}}SupplementalDoc')
        
        for doc_ref in supp_doc_refs:
            leaf_id = doc_ref.get('leafID')
            if leaf_id:
                doc_ref_elem = ET.SubElement(supp_doc_elem, f'{{{def_ns}}}DocumentRef')
                doc_ref_elem.set('leafID', leaf_id)
    
    def _create_analysis_result_displays_from_objects(self, parent: ET.Element, json_data: Dict[str, Any]) -> None:
        """
        Create AnalysisResultDisplays from native Display and Analysis objects.
        
        ARM Structure:
          AnalysisResultDisplays (container per ResultDisplay)
            └─ ResultDisplay (from Display object)
                └─ AnalysisResults (from Analysis objects) *
        
        Args:
            parent: Parent MetaDataVersion element
            json_data: Full JSON data with displays and analyses arrays
        """
        displays = json_data.get('displays', [])
        analyses = json_data.get('analyses', [])
        
        if not displays:
            return
        
        # Create analysis lookup for quick access
        analysis_lookup = {a.get('OID'): a for a in analyses}
        
        # Get display→analyses mapping from supplemental data (for Displays with multiple Analyses)
        xml_metadata = json_data.get('_xmlMetadata', {})
        display_supplemental = xml_metadata.get('displaySupplemental', {})
        display_to_analyses = display_supplemental.get('multipleAnalyses', {})
        
        # Get analysis supplemental data for perfect roundtrip
        analysis_supplemental = xml_metadata.get('analysisSupplemental', {})
        analysis_dataset_criteria = analysis_supplemental.get('datasetCriteria', {})
        analysis_parameters = analysis_supplemental.get('parameters', {})
        analysis_doc_leafids = analysis_supplemental.get('docLeafIDs', {})
        analysis_progcode_leafids = analysis_supplemental.get('progcodeLeafIDs', {})
        
        # Get ARM namespace (try adamref first, fallback to arm)
        arm_ns = self._get_namespace_uri('adamref') or self._get_namespace_uri('arm')
        if not arm_ns:
            logger.warning("No ARM namespace found, skipping AnalysisResultDisplays")
            return
        
        # Check if we need separate containers (LZZT format) or one container (defineV21 format)
        # Check first display's supplemental data to determine format
        use_separate_containers = False
        if displays:
            first_display_oid = displays[0].get('OID')
            first_display_supp = display_supplemental.get(first_display_oid, {})
            use_separate_containers = first_display_supp.get('_separateContainer', False)
        
        # Create container(s) based on format
        if use_separate_containers:
            # LZZT format: one AnalysisResultDisplays container per Display
            ard_container = None  # Will be created per display
        else:
            # defineV21 format: one AnalysisResultDisplays container for all Displays
            if displays:
                ard_container = ET.SubElement(parent, f'{{{arm_ns}}}AnalysisResultDisplays')
        
        for display in displays:
            # Create separate container if needed (LZZT format)
            if use_separate_containers:
                ard_container = ET.SubElement(parent, f'{{{arm_ns}}}AnalysisResultDisplays')
            
            # Create ResultDisplay element
            rd_elem = ET.SubElement(ard_container, f'{{{arm_ns}}}ResultDisplay')
            rd_elem.set('OID', display.get('OID', ''))
            
            # Get display supplemental data for attributes and documents
            display_oid = display.get('OID')
            display_supp = display_supplemental.get(display_oid, {})
            
            # Set attributes based on format
            if display_supp.get('displayIdentifier'):
                # LZZT format: DisplayIdentifier and DisplayLabel
                rd_elem.set('DisplayIdentifier', display_supp['displayIdentifier'])
                if display_supp.get('displayLabel'):
                    rd_elem.set('DisplayLabel', display_supp['displayLabel'])
            else:
                # defineV21 format: Name attribute
                name_attr = display_supp.get('name') or display.get('name')
                if name_attr:
                    rd_elem.set('Name', name_attr)
            
            # Add Description child if present
            if display.get('description'):
                desc_elem = ET.SubElement(rd_elem, 'Description')
                self._create_translated_text(desc_elem, display['description'])
            
            # Add DocumentRef children if Display.location exists (presence indicates original had DocumentRef children)
            locations = display.get('location', [])
            if locations:
                def_ns = self._get_namespace_uri('def')
                for loc_ref in locations:
                    # Handle both dict (from JSON) and DocumentReference object
                    if isinstance(loc_ref, dict):
                        leaf_id = loc_ref.get('leafID')
                    else:
                        leaf_id = loc_ref.leafID if hasattr(loc_ref, 'leafID') else None
                    
                    if leaf_id:
                        # DocumentRef is in def namespace, not arm namespace
                        if def_ns:
                            doc_ref = ET.SubElement(rd_elem, f'{{{def_ns}}}DocumentRef')
                        else:
                            doc_ref = ET.SubElement(rd_elem, f'{{{arm_ns}}}DocumentRef')
                        doc_ref.set('leafID', leaf_id)
                        # Add PDFPageRef children if present in supplemental
                        pdf_page_refs_dict = display_supp.get('pdfPageRefs', {})
                        pdf_page_refs = pdf_page_refs_dict.get(leaf_id, [])
                        for pdf_page_ref_data in pdf_page_refs:
                            pdf_ref_elem = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                            if pdf_page_ref_data.get('pageRefs'):
                                pdf_ref_elem.set('PageRefs', pdf_page_ref_data['pageRefs'])
                            if pdf_page_ref_data.get('type'):
                                pdf_ref_elem.set('Type', pdf_page_ref_data['type'])
                            if pdf_page_ref_data.get('title'):
                                pdf_ref_elem.set('Title', pdf_page_ref_data['title'])
            
            # Set leafID attribute on ResultDisplay (only if original had it as an attribute, not from DocumentRef children)
            # If Display.location exists, DocumentRef children were present, so don't set leafID attribute
            # If Display.location doesn't exist but leafID is in supplemental, set it as attribute
            if not locations:
                leaf_id = display_supp.get('leafID')
                if leaf_id:
                    rd_elem.set('leafID', leaf_id)
            
            # Get linked Analysis object(s)
            # Check supplemental data first for multiple analyses, fallback to display.analysis field
            display_oid = display.get('OID')
            if display_oid in display_to_analyses:
                # Use full list from supplemental data
                analysis_oids = display_to_analyses[display_oid]
            else:
                # Use single analysis from display.analysis field
                analysis_ref = display.get('analysis')
                if not analysis_ref:
                    continue
                analysis_oids = [analysis_ref] if isinstance(analysis_ref, str) else [analysis_ref]
            
            for analysis_oid in analysis_oids:
                analysis = analysis_lookup.get(analysis_oid)
                if not analysis:
                    logger.warning(f"Analysis {analysis_oid} not found for Display {display.get('OID')}")
                    continue
                
                # Create AnalysisResult element (default to singular, correct format)
                # Permissively handle AnalysisResults (plural) if explicitly detected, but default to singular
                uses_plural = display_supp.get('_usesAnalysisResults', False)
                if uses_plural:
                    # Only use plural if explicitly detected in original XML (permissive handling)
                    ar_elem = ET.SubElement(rd_elem, f'{{{arm_ns}}}AnalysisResults')
                else:
                    # Default to singular (correct format per Define-XML standard)
                    ar_elem = ET.SubElement(rd_elem, f'{{{arm_ns}}}AnalysisResult')
                ar_elem.set('OID', analysis.get('OID', ''))
                
                # Get AnalysisResult supplemental data
                analysis_oid = analysis.get('OID')
                result_supplemental = analysis_supplemental.get('resultSupplemental', {})
                ar_supp = result_supplemental.get(analysis_oid, {})
                
                # Set attributes
                if analysis.get('analysisReason'):
                    ar_elem.set('Reason', analysis.get('analysisReason'))
                if ar_supp.get('analysisReason'):
                    ar_elem.set('AnalysisReason', ar_supp['analysisReason'])
                if analysis.get('name'):
                    ar_elem.set('ResultIdentifier', analysis.get('name'))
                if ar_supp.get('parameterOID'):
                    ar_elem.set('ParameterOID', ar_supp['parameterOID'])
                if ar_supp.get('analysisPurpose'):
                    ar_elem.set('AnalysisPurpose', ar_supp['analysisPurpose'])
                
                # Add Description child if present in supplemental
                # Description is in ODM namespace, not ARM namespace
                if ar_supp.get('description'):
                    odm_ns = self._get_namespace_uri('odm')
                    if odm_ns:
                        desc_elem = ET.SubElement(ar_elem, f'{{{odm_ns}}}Description')
                    else:
                        desc_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}Description')
                    trans_text = ET.SubElement(desc_elem, 'TranslatedText')
                    trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    trans_text.text = ar_supp['description']
                
                # Add ParameterList if parameters exist (extract from expressions)
                parameters = []
                expressions = analysis.get('expressions', [])
                for expr in expressions:
                    if 'parameters' in expr:
                        parameters.extend(expr['parameters'])
                
                if parameters:
                    param_list_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}ParameterList')
                    # Get original parameter metadata from supplemental
                    analysis_oid = analysis.get('OID')
                    param_metadata = analysis_parameters.get(analysis_oid, [])
                    param_lookup = {pm['paramCD']: pm for pm in param_metadata}
                    
                    for param in parameters:
                        param_elem = ET.SubElement(param_list_elem, f'{{{arm_ns}}}Parameter')
                        # Extract ParamCD from OID or use stored metadata
                        param_oid = param.get('OID', '')
                        param_cd = param_oid.replace('PARAM.', '') if 'PARAM.' in param_oid else param.get('name', '')
                        
                        # Use original metadata if available
                        if param_cd in param_lookup:
                            param_elem.set('ParamCD', param_cd)
                            param_elem.set('Param', param_lookup[param_cd]['param'])
                        else:
                            # Fallback
                            param_elem.set('ParamCD', param_cd)
                            param_elem.set('Param', param.get('name', param_cd))
                
                # Get dataset→criteria mapping for THIS analysis from supplemental
                analysis_oid = analysis.get('OID')
                dataset_criteria_map = analysis_dataset_criteria.get(analysis_oid, {})
                
                input_data = analysis.get('inputData', [])
                
                # Handle both formats permissively, but default to correct format (singular with AnalysisDatasets container)
                # If plural format detected, use LZZT-style structure (direct children, ItemGroupRef)
                # Otherwise, use correct defineV21 format (AnalysisDatasets container, ItemGroupOID attribute)
                if uses_plural:
                    # LZZT format: AnalysisVariable and AnalysisDataset as direct children
                    # AnalysisVariable: all Item OIDs (not just those starting with 'IT.')
                    # AnalysisDataset: ItemGroup OIDs with ItemGroupRef child (not ItemGroupOID attribute)
                    
                    # Get dataset supplemental data to identify which OIDs are datasets
                    dataset_supplemental = analysis_supplemental.get('datasetSupplemental', {})
                    analysis_dataset_supp = dataset_supplemental.get(analysis_oid, {})
                    
                    # Collect ItemGroup OIDs (datasets) - check supplemental data first, then 'IG.' prefix
                    dataset_oids = []
                    item_oids = []
                    for item_oid in input_data:
                        # Check if this OID is marked as a dataset in supplemental data
                        is_dataset = False
                        for ds_oid, ds_supp in analysis_dataset_supp.items():
                            if ds_oid == item_oid and ds_supp.get('_isDataset', False):
                                is_dataset = True
                                break
                        if is_dataset or item_oid.startswith('IG.'):
                            dataset_oids.append(item_oid)
                        else:
                            # Assume non-dataset OIDs are Item OIDs
                            item_oids.append(item_oid)
                    
                    # Create AnalysisVariable elements (all Item OIDs)
                    for item_oid in item_oids:
                        av_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}AnalysisVariable')
                        av_elem.set('ItemOID', item_oid)
                    
                    # Create AnalysisDataset elements directly (no AnalysisDatasets container)
                    dataset_supplemental = analysis_supplemental.get('datasetSupplemental', {})
                    analysis_dataset_supp = dataset_supplemental.get(analysis_oid, {})
                    
                    for item_oid in dataset_oids:
                        ad_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}AnalysisDataset')
                        # LZZT format: ItemGroupRef child (not ItemGroupOID attribute)
                        # ItemGroupRef is in ODM namespace, not ARM namespace
                        ad_supp = analysis_dataset_supp.get(item_oid, {})
                        odm_ns_uri = ad_supp.get('_itemGroupRefNamespace') or self._get_namespace_uri('odm') or 'http://www.cdisc.org/ns/odm/v1.3'
                        ig_ref_elem = ET.SubElement(ad_elem, f'{{{odm_ns_uri}}}ItemGroupRef')
                        ig_ref_elem.set('ItemGroupOID', item_oid)
                        # Add Mandatory attribute if present
                        if ad_supp.get('mandatory'):
                            ig_ref_elem.set('Mandatory', ad_supp['mandatory'])
                        
                        # Add WhereClauseRef children if present in supplemental (in def namespace, not arm)
                        ad_supp = analysis_dataset_supp.get(item_oid, {})
                        def_ns = self._get_namespace_uri('def')
                        for wc_ref_data in ad_supp.get('whereClauseRefs', []):
                            wc_oid = wc_ref_data.get('whereClauseOID')
                            if wc_oid:
                                if def_ns:
                                    wc_ref_elem = ET.SubElement(ad_elem, f'{{{def_ns}}}WhereClauseRef')
                                else:
                                    wc_ref_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}WhereClauseRef')
                                wc_ref_elem.set('WhereClauseOID', wc_oid)
                        
                        # Add AnalysisVariable children if present in supplemental
                        for av_data in ad_supp.get('analysisVariables', []):
                            av_item_oid = av_data.get('itemOID')
                            if av_item_oid:
                                av_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}AnalysisVariable')
                                av_elem.set('ItemOID', av_item_oid)
                        
                        # Add SelectionCriteria if present in supplemental
                        sc_data = ad_supp.get('selectionCriteria', {})
                        if sc_data.get('computationMethods'):
                            sc_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}SelectionCriteria')
                            def_ns = self._get_namespace_uri('def')
                            for cm_data in sc_data['computationMethods']:
                                if def_ns:
                                    cm_elem = ET.SubElement(sc_elem, f'{{{def_ns}}}ComputationMethod')
                                else:
                                    cm_elem = ET.SubElement(sc_elem, f'{{{arm_ns}}}ComputationMethod')
                                if cm_data.get('OID'):
                                    cm_elem.set('OID', cm_data['OID'])
                                if cm_data.get('Name'):
                                    cm_elem.set('Name', cm_data['Name'])
                                if cm_data.get('text'):
                                    cm_elem.text = cm_data['text']
                else:
                    # defineV21 format: AnalysisDatasets container with AnalysisDataset children
                    # Add AnalysisVariable elements (from inputData)
                    for item_oid in input_data:
                        # Check if it's an Item OID (starts with 'IT.') - these become AnalysisVariable
                        if item_oid.startswith('IT.'):
                            av_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}AnalysisVariable')
                            av_elem.set('ItemOID', item_oid)
                    
                    # Collect ItemGroup OIDs (datasets)
                    # ItemGroup OIDs start with 'IG.', Item OIDs start with 'IT.'
                    dataset_oids = [item_oid for item_oid in input_data if item_oid.startswith('IG.')]
                    
                    if dataset_oids:
                        # Create AnalysisDatasets container
                        ads_container = ET.SubElement(ar_elem, f'{{{arm_ns}}}AnalysisDatasets')
                        
                        # Add AnalysisDatasets attributes (e.g., CommentOID) from supplemental
                        datasets_supplemental = analysis_supplemental.get('datasetsSupplemental', {})
                        ads_container_supp = datasets_supplemental.get(analysis_oid, {})
                        def_ns = self._get_namespace_uri('def')
                        if def_ns and ads_container_supp.get('commentOID'):
                            ads_container.set(f'{{{def_ns}}}CommentOID', ads_container_supp['commentOID'])
                        
                        # Get AnalysisDataset supplemental data
                        dataset_supplemental = analysis_supplemental.get('datasetSupplemental', {})
                        analysis_dataset_supp = dataset_supplemental.get(analysis_oid, {})
                        
                        for item_oid in dataset_oids:
                            ad_elem = ET.SubElement(ads_container, f'{{{arm_ns}}}AnalysisDataset')
                            # Set ItemGroupOID as attribute on AnalysisDataset (not ItemGroupRef child)
                            ad_elem.set('ItemGroupOID', item_oid)
                            
                            # Add WhereClauseRef children if present in supplemental (in def namespace, not arm)
                            ad_supp = analysis_dataset_supp.get(item_oid, {})
                            def_ns = self._get_namespace_uri('def')
                            for wc_ref_data in ad_supp.get('whereClauseRefs', []):
                                wc_oid = wc_ref_data.get('whereClauseOID')
                                if wc_oid:
                                    if def_ns:
                                        wc_ref_elem = ET.SubElement(ad_elem, f'{{{def_ns}}}WhereClauseRef')
                                    else:
                                        wc_ref_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}WhereClauseRef')
                                    wc_ref_elem.set('WhereClauseOID', wc_oid)
                            
                            # Add AnalysisVariable children if present in supplemental
                            for av_data in ad_supp.get('analysisVariables', []):
                                item_oid_av = av_data.get('itemOID')
                                if item_oid_av:
                                    av_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}AnalysisVariable')
                                    av_elem.set('ItemOID', item_oid_av)
                        
                        # Add SelectionCriteria ONLY for THIS dataset (from supplemental mapping)
                        dataset_criteria = dataset_criteria_map.get(item_oid, [])
                        if dataset_criteria:
                            sc_elem = ET.SubElement(ad_elem, f'{{{arm_ns}}}SelectionCriteria')
                            def_ns = self._get_namespace_uri('def')
                            
                            # Get method details from methods array
                            methods_array = json_data.get('methods', [])
                            method_lookup = {m.get('OID'): m for m in methods_array}
                            
                            for method_oid in dataset_criteria:
                                if def_ns:
                                    method = method_lookup.get(method_oid)
                                    cm_elem = ET.SubElement(sc_elem, f'{{{def_ns}}}ComputationMethod')
                                    cm_elem.set('OID', method_oid)
                                    # Get Name from method if available
                                    if method and method.get('name'):
                                        cm_elem.set('Name', method['name'])
                                    else:
                                        cm_elem.set('Name', 'Selection Criteria')
                                    # Get text from method description
                                    if method and method.get('description'):
                                        cm_elem.text = method['description']
                
                # Add Documentation if present in supplemental or description exists
                doc_data = ar_supp.get('documentation')
                description = analysis.get('description', '')
                if doc_data or description:
                    doc_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}Documentation')
                    
                    # Add leafID attribute if present in supplemental data
                    if doc_data and doc_data.get('leafID'):
                        doc_elem.set('leafID', doc_data['leafID'])
                    
                    # Use supplemental data if available
                    if doc_data:
                        if doc_data.get('description'):
                            # Check if TranslatedText should be directly under Documentation (LZZT format) or under Description (defineV21 format)
                            if doc_data.get('_translatedTextDirect', False):
                                # LZZT format: TranslatedText directly under Documentation
                                odm_ns = self._get_namespace_uri('odm')
                                if odm_ns:
                                    trans_text = ET.SubElement(doc_elem, f'{{{odm_ns}}}TranslatedText')
                                else:
                                    trans_text = ET.SubElement(doc_elem, 'TranslatedText')
                                trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                                trans_text.text = doc_data['description']
                            else:
                                # defineV21 format: TranslatedText under Description
                                odm_ns = self._get_namespace_uri('odm')
                                if odm_ns:
                                    doc_desc_elem = ET.SubElement(doc_elem, f'{{{odm_ns}}}Description')
                                else:
                                    doc_desc_elem = ET.SubElement(doc_elem, f'{{{arm_ns}}}Description')
                                trans_text = ET.SubElement(doc_desc_elem, 'TranslatedText')
                                trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                                trans_text.text = doc_data['description']
                        
                        for doc_ref_data in doc_data.get('documents', []):
                            leaf_id = doc_ref_data.get('leafID')
                            if leaf_id:
                                # DocumentRef is in def namespace, not arm namespace
                                def_ns = self._get_namespace_uri('def')
                                if def_ns:
                                    doc_ref = ET.SubElement(doc_elem, f'{{{def_ns}}}DocumentRef')
                                else:
                                    doc_ref = ET.SubElement(doc_elem, f'{{{arm_ns}}}DocumentRef')
                                doc_ref.set('leafID', leaf_id)
                                # Add PDFPageRef children if present
                                for pdf_page_ref_data in doc_ref_data.get('pdfPageRefs', []):
                                    pdf_ref_elem = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                                    if pdf_page_ref_data.get('pageRefs'):
                                        pdf_ref_elem.set('PageRefs', pdf_page_ref_data['pageRefs'])
                                    if pdf_page_ref_data.get('type'):
                                        pdf_ref_elem.set('Type', pdf_page_ref_data['type'])
                                    if pdf_page_ref_data.get('title'):
                                        pdf_ref_elem.set('Title', pdf_page_ref_data['title'])
                    elif description:
                        # Fallback to old logic
                        # Check if description is a leafID-only marker
                        if description.startswith('[leafID: ') and description.endswith(']'):
                            # Extract leafID and set as attribute (empty Documentation)
                            leaf_id = description[9:-1]  # Remove '[leafID: ' and ']'
                            doc_elem.set('leafID', leaf_id)
                        else:
                            # Regular description with TranslatedText
                            # Check if leafID exists in supplemental (Documentation with BOTH leafID and text)
                            doc_leaf_id = analysis_doc_leafids.get(analysis_oid)
                            if doc_leaf_id:
                                doc_elem.set('leafID', doc_leaf_id)
                            
                            # Create Description/TranslatedText structure (not TranslatedText directly)
                            # Description is in ODM namespace, not ARM namespace
                            odm_ns = self._get_namespace_uri('odm')
                            if odm_ns:
                                doc_desc_elem = ET.SubElement(doc_elem, f'{{{odm_ns}}}Description')
                            else:
                                doc_desc_elem = ET.SubElement(doc_elem, f'{{{arm_ns}}}Description')
                            trans_text = ET.SubElement(doc_desc_elem, 'TranslatedText')
                            trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                            trans_text.text = description
                
                # Add ProgrammingCode (from supplemental or link to analysisMethod OR empty with leafID)
                prog_code_data = ar_supp.get('programmingCode')
                analysis_method_oid = analysis.get('analysisMethod')
                progcode_leaf_id = analysis_progcode_leafids.get(analysis_oid)
                
                if prog_code_data is not None:
                    # Use supplemental data (always create if present, even if empty)
                    pc_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}ProgrammingCode')
                    if prog_code_data.get('leafID'):
                        pc_elem.set('leafID', prog_code_data['leafID'])
                    if prog_code_data.get('context'):
                        pc_elem.set('Context', prog_code_data['context'])
                    if prog_code_data.get('methodOID'):
                        def_ns = self._get_namespace_uri('def')
                        if def_ns:
                            cm_elem = ET.SubElement(pc_elem, f'{{{def_ns}}}ComputationMethod')
                            cm_elem.set('OID', prog_code_data['methodOID'])
                            # Add Name attribute if present
                            if prog_code_data.get('computationMethodName'):
                                cm_elem.set('Name', prog_code_data['computationMethodName'])
                            # Add text content if present
                            if prog_code_data.get('computationMethodText'):
                                cm_elem.text = prog_code_data['computationMethodText']
                    if prog_code_data.get('code'):
                        code_elem = ET.SubElement(pc_elem, f'{{{arm_ns}}}Code')
                        code_elem.text = prog_code_data['code']
                    # Add DocumentRef children if present (in def namespace)
                    def_ns = self._get_namespace_uri('def')
                    for doc_ref_data in prog_code_data.get('documents', []):
                        leaf_id = doc_ref_data.get('leafID')
                        if leaf_id:
                            if def_ns:
                                doc_ref = ET.SubElement(pc_elem, f'{{{def_ns}}}DocumentRef')
                            else:
                                doc_ref = ET.SubElement(pc_elem, f'{{{arm_ns}}}DocumentRef')
                            doc_ref.set('leafID', leaf_id)
                            # Add PDFPageRef children if present
                            for pdf_page_ref_data in doc_ref_data.get('pdfPageRefs', []):
                                pdf_ref_elem = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                                if pdf_page_ref_data.get('pageRefs'):
                                    pdf_ref_elem.set('PageRefs', pdf_page_ref_data['pageRefs'])
                                if pdf_page_ref_data.get('type'):
                                    pdf_ref_elem.set('Type', pdf_page_ref_data['type'])
                                if pdf_page_ref_data.get('title'):
                                    pdf_ref_elem.set('Title', pdf_page_ref_data['title'])
                elif analysis_method_oid:
                    # ProgrammingCode with ComputationMethod
                    # Look up the method to get its code text
                    method = None
                    methods_array = json_data.get('methods', [])
                    for m in methods_array:
                        if m.get('OID') == analysis_method_oid:
                            method = m
                            break
                    
                    # Write ProgrammingCode with method text
                    pc_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}ProgrammingCode')
                    def_ns = self._get_namespace_uri('def')
                    if def_ns:
                        cm_elem = ET.SubElement(pc_elem, f'{{{def_ns}}}ComputationMethod')
                        cm_elem.set('OID', analysis_method_oid)
                        # Add method code text if available
                        if method and method.get('description'):
                            cm_elem.text = method['description']
                elif progcode_leaf_id:
                    # Empty ProgrammingCode with only leafID
                    pc_elem = ET.SubElement(ar_elem, f'{{{arm_ns}}}ProgrammingCode')
                    pc_elem.set('leafID', progcode_leaf_id)
    
    def _create_analysis_result_displays(self, parent: ET.Element, analysis_displays: Optional[List[Dict[str, Any]]]) -> None:
        """
        DEPRECATED: Old XML blob-based creator. Keep for backward compatibility.
        
        Fix #3: Create AnalysisResultDisplays (ARM/AdamRef Extensions).
        
        Recreates the complete structure from serialized XML containers.
        Each container is a separate AnalysisResultDisplays element.
        
        Args:
            parent: Parent MetaDataVersion element
            analysis_displays: List of analysis result container objects
        """
        if not analysis_displays:
            return
        
        # Each entry in analysis_displays is a complete container
        for container_data in analysis_displays:
            if container_data.get('_containerType') == 'AnalysisResultDisplays':
                # We have serialized XML content - parse and recreate
                xml_content = container_data.get('_xmlContent')
                namespace_prefix = container_data.get('_namespace', 'adamref')
                
                if xml_content:
                    try:
                        # Parse the XML content
                        container_elem = ET.fromstring(xml_content)
                        # Append directly to parent
                        parent.append(container_elem)
                    except Exception as e:
                        logger.error(f"Failed to parse AnalysisResultDisplays XML content: {e}")
                        # Fallback to empty container if parse fails
                        self._create_empty_analysis_container(parent, namespace_prefix)
            else:
                # Fallback for old format - shouldn't happen with updated xml_to_json
                logger.warning("Found old-format analysis display data, creating minimal structure")
                self._create_legacy_analysis_display(parent, container_data)
    
    def _create_empty_analysis_container(self, parent: ET.Element, namespace_prefix: str) -> None:
        """Create an empty AnalysisResultDisplays container."""
        analysis_ns = self._get_namespace_uri(namespace_prefix)
        if analysis_ns:
            ET.SubElement(parent, f'{{{analysis_ns}}}AnalysisResultDisplays')
    
    def _create_legacy_analysis_display(self, parent: ET.Element, ar: Dict[str, Any]) -> None:
        """Fallback for old format analysis displays."""
        # Get namespace
        analysis_ns = self._get_namespace_uri('adamref')
        if not analysis_ns:
            return
        
        # Create container
        ard_container = ET.SubElement(parent, f'{{{analysis_ns}}}AnalysisResultDisplays')
        
        # Create ResultDisplay
        element_type = ar.get('_elementType', 'ResultDisplay')
        if element_type == 'ResultDisplay':
            ar_elem = ET.SubElement(ard_container, f'{{{analysis_ns}}}ResultDisplay')
            ar_elem.set('OID', ar.get('OID', ''))
            for attr in ['DisplayIdentifier', 'DisplayLabel', 'leafID']:
                if ar.get(attr):
                    ar_elem.set(attr, ar[attr])
    
    def _flatten_nested_itemgroups(self, item_groups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract nested ItemGroups from slices and flatten to top level.
        
        Recursively traverses slices arrays to find nested ValueLists and other ItemGroups.
        Modifies parent slices arrays to contain only OID references (for roundtrip).
        
        Args:
            item_groups: List of top-level ItemGroups (may contain nested slices)
            
        Returns:
            Flat list of all ItemGroups (domains + nested ValueLists)
        """
        flattened = []
        
        for ig in item_groups:
            # Add this ItemGroup to flat list
            flattened.append(ig)
            
            # Check for nested slices (could be ItemGroup objects or OID strings)
            slices = ig.get('slices', [])
            if not slices:
                continue
            
            # Separate nested ItemGroups from OID references
            nested_igs = []
            oid_refs = []
            
            for slice_item in slices:
                if isinstance(slice_item, dict):
                    # It's a nested ItemGroup object - extract it
                    nested_igs.append(slice_item)
                    # Replace with OID reference for parent's slices array
                    oid_refs.append(slice_item.get('OID', ''))
                elif isinstance(slice_item, str):
                    # It's already an OID reference - keep it
                    oid_refs.append(slice_item)
            
            # Update parent's slices to only contain OID references (for XML writing)
            if nested_igs:
                ig['slices'] = oid_refs
                logger.info(f"    - Extracted {len(nested_igs)} nested ItemGroups from {ig.get('OID')}")
            
            # Recursively flatten any nested ItemGroups
            if nested_igs:
                flattened.extend(self._flatten_nested_itemgroups(nested_igs))
        
        return flattened
    
    def _process_item_groups_and_value_lists(
        self, 
        parent: ET.Element, 
        all_item_groups: List[Dict[str, Any]],
        json_data: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        json_data = json_data or {}
        """
        Process ItemGroups and ValueLists with intelligent handling.
        
        Strategy:
        1. Flatten nested ValueLists from slices to top level
        2. Separate by type field ('ValueList', 'DatasetSpecialization', or regular)
        3. Create ValueListDef elements for type='ValueList'
        4. Create ItemGroupDef elements for regular ItemGroups
        5. Handle DatasetSpecialization slices if inference enabled
        
        Returns:
            Flattened list of all ItemGroups (for ItemDef processing)
        """
        # Flatten any nested ItemGroups (ValueLists nested under parents) to top level
        logger.info(f"Flattening {len(all_item_groups)} top-level ItemGroups (may contain nested ValueLists)...")
        flattened_item_groups = self._flatten_nested_itemgroups(all_item_groups)
        logger.info(f"  - Flattened to {len(flattened_item_groups)} total ItemGroups")
        
        # Separate ItemGroups by type field
        value_list_groups = [ig for ig in flattened_item_groups if ig.get('type') == 'ValueList']
        slice_item_groups = [ig for ig in flattened_item_groups if ig.get('type') == 'DatasetSpecialization']
        domain_item_groups = [ig for ig in flattened_item_groups 
                              if ig.get('type') not in ('ValueList', 'DatasetSpecialization')]
        
        # Build map of ValueList OIDs for reference in ItemDef creation
        # This allows us to add <def:ValueListRef> elements to ItemDefs
        # Pattern: ItemDef OID "ADLBC.AVAL" -> ValueList OID "ValueList.ADLBC.AVAL"
        self._value_list_oids = set()
        for ig in value_list_groups:
            oid = ig.get('OID')
            if oid:
                self._value_list_oids.add(oid)
        
        logger.info(f"Collected {len(self._value_list_oids)} ValueList OIDs for ItemDef reference")
        
        # Create ValueLists
        if value_list_groups:
            self._create_value_lists_direct(parent, value_list_groups)
            logger.info(f"Created {len(value_list_groups)} ValueListDef elements")
        
        # Handle DatasetSpecialization slices
        if self.enable_inference and slice_item_groups:
            # Project slices to ValueLists
            self._create_value_lists_from_slices(parent, slice_item_groups, domain_item_groups)
        elif slice_item_groups:
            # Fallback: treat slices as regular ItemGroups if inference disabled
            logger.warning("DatasetSpecialization slices found but inference disabled - treating as ItemGroups")
            domain_item_groups.extend(slice_item_groups)
        
        # Create domain ItemGroups
        self._create_item_groups(parent, domain_item_groups, json_data)
        logger.info(f"Created {len(domain_item_groups)} ItemGroupDef elements")
        
        # Return flattened list for ItemDef processing
        return flattened_item_groups
    
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
            # Get WhereClause from slice's applicableWhen (canonical slices have one WhereClause)
            applicable_when = slice_ig.get('applicableWhen', [])
            where_clause = applicable_when[0] if applicable_when else ''
            items = slice_ig.get('items', [])
            
            for item in items:
                var_name = item.get('variable') or item.get('name', '')
                if not var_name:
                    continue
                
                key = (domain, var_name)
                if key not in var_to_contexts:
                    var_to_contexts[key] = []
                
                # Store item with its context
                # Use slice's applicableWhen, or fall back to item's applicableWhen
                item_applicable_when = item.get('applicableWhen', [])
                item_where_clause = item_applicable_when[0] if item_applicable_when else where_clause
                var_to_contexts[key].append({
                    'item': item,
                    'whereClause': item_where_clause or where_clause
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
            
            # Add ItemRefs for each context - order inferred from array position
            for idx, ctx in enumerate(contexts, start=1):
                item = ctx['item']
                where_clause = ctx['whereClause']
                
                item_ref = ET.SubElement(vl_elem, 'ItemRef')
                item_oid = item.get('OID') or item.get('itemOID', '')
                item_ref.set('ItemOID', item_oid)
                item_ref.set('OrderNumber', str(idx))
                
                # Only set Mandatory if explicitly present
                if 'mandatory' in item:
                    item_ref.set('Mandatory', self._safe_str(item['mandatory']))
                
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
        """Create ValueListDef elements directly from stored structure, preserving original order."""
        def_ns = self._get_namespace_uri('def')
        
        # Sort value_lists by original order if available in metadata
        xml_metadata = getattr(self, '_current_xml_metadata', {})
        # Note: valueListDefOrder removed - order is preserved by array ordering
        # Process ValueLists in the order they appear in the JSON array
        
        for vl in value_lists:
            vl_elem = ET.SubElement(parent, f'{{{def_ns}}}ValueListDef' if def_ns else 'ValueListDef')
            vl_elem.set('OID', vl.get('OID', ''))
            
            if vl.get('description'):
                desc = ET.SubElement(vl_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = vl['description']
            
            # Merge supplemental data
            merged_vl = self._merge_supplemental_data(vl, 'itemGroup')
            
            # Add ItemRefs - order is inferred from array position
            for idx, item in enumerate(merged_vl.get('items', []), start=1):
                item_ref = ET.SubElement(vl_elem, 'ItemRef')
                item_oid = item.get('itemOID') or item.get('OID', '')
                item_ref.set('ItemOID', item_oid)
                item_ref.set('OrderNumber', str(idx))
                
                # Only set Mandatory if explicitly present
                if 'mandatory' in item:
                    item_ref.set('Mandatory', self._safe_str(item['mandatory']))
                
                if item.get('role'):
                    item_ref.set('Role', item['role'])
                
                # MethodOID
                if item.get('method'):
                    item_ref.set('MethodOID', item['method'])
                
                # def:HasNoData - from item metadata
                xml_metadata = getattr(self, '_current_xml_metadata', {})
                item_group_supp = xml_metadata.get('itemGroupSupplemental', {})
                item_origin_metadata = item_group_supp.get('_itemOriginMetadata', {})
                item_metadata = item_origin_metadata.get(item_oid, {})
                has_no_data = item_metadata.get('hasNoData')
                if has_no_data and def_ns:
                    item_ref.set(f'{{{def_ns}}}HasNoData', has_no_data)
                
                # WhereClauseRef (from whereClauseOID or applicableWhen)
                where_clause_oid = item.get('whereClauseOID')
                if not where_clause_oid and item.get('applicableWhen'):
                    # applicableWhen is a list of WhereClause OIDs
                    applicable_when = item.get('applicableWhen', [])
                    if applicable_when:
                        where_clause_oid = applicable_when[0]  # Use first one
                
                if where_clause_oid:
                    wc_ref = ET.SubElement(item_ref, f'{{{def_ns}}}WhereClauseRef' if def_ns else 'WhereClauseRef')
                    wc_ref.set('WhereClauseOID', where_clause_oid)
    
    def _create_item_groups(self, parent: ET.Element, datasets: List[Dict[str, Any]], json_data: Dict[str, Any] = None) -> None:
        """Create ItemGroupDef elements."""
        def_ns = self._get_namespace_uri('def')
        json_data = json_data or {}
        
        for ds in datasets:
            ig_elem = ET.SubElement(parent, 'ItemGroupDef')
            
            # Merge supplemental data from _xmlMetadata
            merged_ds = self._merge_supplemental_data(ds, 'itemGroup')
            
            # Apply all mapped attributes (including def: namespaced ones)
            self._apply_mapped_attributes(ig_elem, merged_ds)
            
            # Write def: namespaced attributes from supplemental data
            if def_ns:
                # Use native label if available, otherwise fall back to supplemental
                if merged_ds.get('label'):
                    ig_elem.set(f'{{{def_ns}}}Label', str(merged_ds['label']))
                elif merged_ds.get('defLabel'):
                    ig_elem.set(f'{{{def_ns}}}Label', merged_ds['defLabel'])
                # def:Class - write as attribute if it was an attribute in original
                if merged_ds.get('defClass') and merged_ds.get('classIsAttribute'):
                    ig_elem.set(f'{{{def_ns}}}Class', merged_ds['defClass'])
                if merged_ds.get('defDomainKeys'):
                    ig_elem.set(f'{{{def_ns}}}DomainKeys', merged_ds['defDomainKeys'])
                if merged_ds.get('structure'):
                    ig_elem.set(f'{{{def_ns}}}Structure', str(merged_ds['structure']))
                if merged_ds.get('archiveLocationID'):
                    ig_elem.set(f'{{{def_ns}}}ArchiveLocationID', merged_ds['archiveLocationID'])
                # def:CommentOID - from supplemental
                if merged_ds.get('commentOID'):
                    ig_elem.set(f'{{{def_ns}}}CommentOID', merged_ds['commentOID'])
                # def:StandardOID - from supplemental
                if merged_ds.get('standardOID'):
                    ig_elem.set(f'{{{def_ns}}}StandardOID', merged_ds['standardOID'])
                # def:IsNonStandard - from supplemental
                if merged_ds.get('isNonStandard'):
                    ig_elem.set(f'{{{def_ns}}}IsNonStandard', merged_ds['isNonStandard'])
                # def:HasNoData - from supplemental
                if merged_ds.get('hasNoData'):
                    ig_elem.set(f'{{{def_ns}}}HasNoData', merged_ds['hasNoData'])
            
            # Write Comment attribute - prefer native comments array, fall back to supplemental
            if merged_ds.get('comments') and len(merged_ds['comments']) > 0:
                # Use first comment as Comment attribute
                ig_elem.set('Comment', str(merged_ds['comments'][0]))
            elif 'comment' in merged_ds:
                ig_elem.set('Comment', merged_ds['comment'])
            
            # Write Repeating attribute from supplemental
            if merged_ds.get('repeating'):
                ig_elem.set('Repeating', merged_ds['repeating'])
            
            # Add Description if present
            if merged_ds.get('description'):
                desc = ET.SubElement(ig_elem, 'Description')
                self._create_translated_text(desc, merged_ds['description'])
            
            # Add Alias elements from coding field
            # Coding objects map to Alias (codeSystem → Context, code → Name)
            coding_list = merged_ds.get('coding', [])
            for coding in coding_list:
                if isinstance(coding, dict):
                    code_system = coding.get('codeSystem')
                    code = coding.get('code')
                    if code_system and code:
                        alias_elem = ET.SubElement(ig_elem, 'Alias')
                        alias_elem.set('Context', code_system)
                        alias_elem.set('Name', code)
            
            # Add ItemRefs - order is preserved by array ordering
            items = merged_ds.get('items', [])
            # Set current ItemGroup context for KeySequence resolution
            self._current_itemgroup = merged_ds
            for idx, item in enumerate(items, start=1):
                self._create_item_ref(ig_elem, item, def_ns, order_number=idx)
            self._current_itemgroup = None  # Clear context
            
            # Add def:leaf element - check for Resource reference or legacy leaf data
            if merged_ds.get('sourceResourceOID'):
                # Look up Resource from resources array
                resources = json_data.get('resources', [])
                resource = next((r for r in resources if r.get('OID') == merged_ds['sourceResourceOID']), None)
                if resource:
                    # Convert Resource back to leaf
                    leaf_data = {
                        'ID': merged_ds.get('leafID', resource.get('OID', '').replace('RES.', '')),
                        'href': resource.get('href'),
                        'title': resource.get('label') or resource.get('name')
                    }
                    self._create_leaf_element(ig_elem, leaf_data, def_ns)
            elif merged_ds.get('leaf'):
                # Legacy leaf data
                self._create_leaf_element(ig_elem, merged_ds['leaf'], def_ns)
            
            # Add def:Class child element (only if it was a child element in original)
            if def_ns and merged_ds.get('defClass') and not merged_ds.get('classIsAttribute'):
                class_elem = ET.SubElement(ig_elem, f'{{{def_ns}}}Class')
                class_elem.set('Name', merged_ds['defClass'])
                
                # Add SubClass children if present
                sub_classes = merged_ds.get('subClasses', [])
                for sub_class_data in sub_classes:
                    sub_class_elem = ET.SubElement(class_elem, f'{{{def_ns}}}SubClass')
                    sub_class_elem.set('Name', sub_class_data.get('name', ''))
    
    def _create_item_ref(self, parent: ET.Element, item: Dict[str, Any], def_ns: str, order_number: int = None) -> None:
        """Create an ItemRef element. Order is inferred from array position."""
        item_ref = ET.SubElement(parent, 'ItemRef')
        
        # ItemOID
        item_oid = item.get('OID') or item.get('itemOID', '')
        item_ref.set('ItemOID', item_oid)
        
        # OrderNumber - inferred from array position
        if order_number is not None:
            item_ref.set('OrderNumber', str(order_number))
        
        # Mandatory - only set if explicitly present
        if 'mandatory' in item:
            item_ref.set('Mandatory', self._safe_str(item['mandatory']))
        
        # Role
        if item.get('role'):
            item_ref.set('Role', item['role'])
        
        # KeySequence - derived from parent ItemGroup's native keySequence array
        key_seq = None
        current_ig = getattr(self, '_current_itemgroup', None)
        if current_ig and current_ig.get('keySequence'):
            key_sequence_list = current_ig['keySequence']
            if item_oid in key_sequence_list:
                # KeySequence is 1-based position in the list
                key_seq = key_sequence_list.index(item_oid) + 1
        
        if key_seq:
            item_ref.set('KeySequence', str(key_seq))
        
        # MethodOID - attribute on ItemRef in Define-XML 2.1
        method_oid = item.get('methodOID') or item.get('method')
        if method_oid:
            item_ref.set('MethodOID', method_oid)
        
        # def:HasNoData - from item metadata
        xml_metadata = getattr(self, '_current_xml_metadata', {})
        item_group_supp = xml_metadata.get('itemGroupSupplemental', {})
        item_origin_metadata = item_group_supp.get('_itemOriginMetadata', {})
        item_metadata = item_origin_metadata.get(item_oid, {})
        has_no_data = item_metadata.get('hasNoData')
        if has_no_data and def_ns:
            item_ref.set(f'{{{def_ns}}}HasNoData', has_no_data)
        
        # WhereClauseRef (from whereClauseOID or applicableWhen)
        where_clause_oid = item.get('whereClauseOID')
        if not where_clause_oid and item.get('applicableWhen'):
            # applicableWhen is a list of WhereClause OIDs
            applicable_when = item.get('applicableWhen', [])
            if applicable_when:
                where_clause_oid = applicable_when[0]  # Use first one
        
        if where_clause_oid:
            wc_ref = ET.SubElement(item_ref, f'{{{def_ns}}}WhereClauseRef' if def_ns else 'WhereClauseRef')
            wc_ref.set('WhereClauseOID', where_clause_oid)
    
    def _create_leaf_element(self, parent: ET.Element, leaf_data: Dict[str, Any], def_ns: str) -> None:
        """Create a def:leaf element for dataset location."""
        if not def_ns:
            return
        
        xlink_ns = self._get_namespace_uri('xlink')
        
        # Create leaf element with def namespace
        leaf_elem = ET.SubElement(parent, f'{{{def_ns}}}leaf')
        
        # Add ID attribute
        if leaf_data.get('ID'):
            leaf_elem.set('ID', leaf_data['ID'])
        
        # Add xlink:href attribute
        if leaf_data.get('href') and xlink_ns:
            leaf_elem.set(f'{{{xlink_ns}}}href', leaf_data['href'])
        
        # Add def:title child element
        if leaf_data.get('title'):
            title_elem = ET.SubElement(leaf_elem, f'{{{def_ns}}}title')
            title_elem.text = leaf_data['title']
    
    def _extract_items_recursively(self, item_group: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Recursively extract items from an ItemGroup and its nested slices.
        
        Args:
            item_group: ItemGroup dictionary (may contain nested slices)
            
        Returns:
            List of all items from this ItemGroup and its nested slices
        """
        items = []
        
        # Extract items from this ItemGroup
        for item in item_group.get('items', []):
            # Normalize OID field
            if 'itemOID' in item and 'OID' not in item:
                item = item.copy()
                item['OID'] = item['itemOID']
            items.append(item)
        
        # Recursively extract from nested slices
        slices = item_group.get('slices', [])
        for slice_item in slices:
            if isinstance(slice_item, dict):
                # It's a nested ItemGroup - recurse into it
                items.extend(self._extract_items_recursively(slice_item))
            # Skip OID string references - they've already been processed
        
        return items
    
    def _process_item_defs(
        self,
        parent: ET.Element,
        json_data: Dict[str, Any],
        all_item_groups: List[Dict[str, Any]]
    ) -> None:
        """
        Process ItemDefs with intelligent deduplication.
        
        Combines top-level items with items nested in ItemGroups,
        removing duplicates by OID. Recursively extracts items from
        nested slices (e.g., ValueLists nested under parent domains).
        """
        # Get top-level items
        items = json_data.get('items', [])
        
        # ALWAYS extract nested items to create ItemDef elements (required by Define-XML spec)
        # Recursively extract from all ItemGroups including nested slices
        nested_items = []
        for ig in all_item_groups:
            nested_items.extend(self._extract_items_recursively(ig))
        
        # Combine and deduplicate
        all_items = items + nested_items
        unique_items = {}
        for item in all_items:
            oid = item.get('OID') or item.get('itemOID')
            if oid:
                # Keep first occurrence (top-level items take precedence)
                if oid not in unique_items:
                    unique_items[oid] = item
        
        # Fix #5: Sort by original order if available
        xml_metadata = json_data.get('_xmlMetadata', {})
        # Note: itemDefOrder removed - order is preserved by array ordering
        # Process items in the order they appear in the JSON (from ItemGroups.items arrays)
        # ItemDef order doesn't matter for Define-XML spec compliance
        self._create_item_defs(parent, list(unique_items.values()))
    
    def _create_item_defs(self, parent: ET.Element, variables: List[Dict[str, Any]]) -> None:
        """Create ItemDef elements."""
        def_ns = self._get_namespace_uri('def')
        
        for var in variables:
            item_elem = ET.SubElement(parent, 'ItemDef')
            
            # Apply basic attributes
            self._apply_mapped_attributes(item_elem, var)
            
            # SASFieldName - write if explicitly present in supplemental
            # Note: We only store SASFieldName in supplemental if it differs from Name
            # If hasSASFieldName flag is set but no explicit value in supplemental, 
            # the original XML didn't have SASFieldName for this specific item
            xml_metadata = getattr(self, '_current_xml_metadata', {})
            has_sas_field_name = xml_metadata.get('hasSASFieldName', False)
            
            if has_sas_field_name and not item_elem.get('SASFieldName'):
                # Get item supplemental metadata
                var_oid = var.get('OID', '')
                item_origin_metadata = xml_metadata.get('itemGroupSupplemental', {}).get('_itemOriginMetadata', {})
                item_metadata = item_origin_metadata.get(var_oid, {})
                
                # Only write if explicitly stored in supplemental (means original had it and it differed from Name)
                sas_field_name = item_metadata.get('SASFieldName')
                if sas_field_name:
                    item_elem.set('SASFieldName', sas_field_name)
            
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
            
            # Handle def:DisplayFormat  
            if var.get('displayFormat'):
                if def_ns:
                    item_elem.set(f'{{{def_ns}}}DisplayFormat', var['displayFormat'])
                else:
                    item_elem.set('DisplayFormat', var['displayFormat'])
            
            # Add Description element if present (separate from label)
            if var.get('description'):
                desc = ET.SubElement(item_elem, 'Description')
                self._create_translated_text(desc, var['description'])
            
            # Add CodeListRef if present
            if var.get('codeList'):
                code_list_ref = ET.SubElement(item_elem, 'CodeListRef')
                code_list_ref.set('CodeListOID', var['codeList'])
            
            # Add ValueListRef from supplemental data
            var_oid = var.get('OID', '')
            if var_oid and def_ns:
                # Check supplemental data for valueListOID
                xml_metadata = getattr(self, '_current_xml_metadata', {})
                item_origin_metadata = xml_metadata.get('itemGroupSupplemental', {}).get('_itemOriginMetadata', {})
                item_metadata = item_origin_metadata.get(var_oid, {})
                value_list_oid = item_metadata.get('valueListOID')
                
                if value_list_oid:
                    vl_ref_elem = ET.SubElement(item_elem, f'{{{def_ns}}}ValueListRef')
                    vl_ref_elem.set('ValueListOID', value_list_oid)
                
                # Add def:CommentOID attribute if present in supplemental data
                comment_oid = item_metadata.get('commentOID')
                if comment_oid:
                    item_elem.set(f'{{{def_ns}}}CommentOID', comment_oid)
            
            # Add Origin if present
            origin = var.get('origin', {})
            
            # Get origin metadata from supplemental data
            xml_metadata = getattr(self, '_current_xml_metadata', {})
            item_group_supp = xml_metadata.get('itemGroupSupplemental', {})
            item_origin_metadata = item_group_supp.get('_itemOriginMetadata', {})
            origin_metadata = item_origin_metadata.get(var.get('OID'), {})
            
            # Extract comment from Comment objects (prefer over supplemental)
            comment_text = None
            comments = var.get('comments', [])
            if comments:
                # Look for origin-related comments (OID contains "ORIGIN")
                for comment in comments:
                    if isinstance(comment, dict):
                        comment_oid = comment.get('OID', '')
                        if 'ORIGIN' in comment_oid:
                            comment_text = comment.get('text', '')
                            break
                    elif hasattr(comment, 'OID') and 'ORIGIN' in getattr(comment, 'OID', ''):
                        comment_text = getattr(comment, 'text', '')
                        break
            
            # Fallback to supplemental if not found in comments
            if not comment_text:
                comment_text = origin_metadata.get('comment')
            
            # Check if we have origin data or metadata
            if origin or origin_metadata or comment_text:
                # Check if original was element-based or attribute-based
                was_element = origin_metadata.get('wasElement', False)
                
                if origin and (origin.get('type') or origin.get('source')):
                    if was_element:
                        # v2.x style: Create Origin child element
                        origin_elem = ET.SubElement(item_elem, f'{{{def_ns}}}Origin' if def_ns else 'Origin')
                        if origin.get('type'):
                            origin_elem.set('Type', origin['type'])
                        if origin.get('source'):
                            origin_elem.set('Source', origin['source'])
                        
                        # Add Description within Origin if present (stored in metadata)
                        origin_desc_text = origin_metadata.get('originDescription')
                        if origin_desc_text:
                            origin_desc = ET.SubElement(origin_elem, 'Description')
                            self._create_translated_text(origin_desc, origin_desc_text)
                        
                        # Add DocumentRef elements if present
                        documents = origin.get('documents', [])
                        for doc in documents:
                            leaf_id = doc.get('leafID')
                            if leaf_id and def_ns:
                                doc_ref = ET.SubElement(origin_elem, f'{{{def_ns}}}DocumentRef')
                                doc_ref.set('leafID', leaf_id)
                                
                                # Add PDFPageRef elements if present in metadata
                                pdf_page_refs = origin_metadata.get(f'pdfPageRefs_{leaf_id}', [])
                                for pdf_data in pdf_page_refs:
                                    pdf_ref = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                                    if pdf_data.get('type'):
                                        pdf_ref.set('Type', pdf_data['type'])
                                    if pdf_data.get('pageRefs'):
                                        pdf_ref.set('PageRefs', pdf_data['pageRefs'])
                                    if pdf_data.get('firstPage'):
                                        pdf_ref.set('FirstPage', str(pdf_data['firstPage']))
                                    if pdf_data.get('lastPage'):
                                        pdf_ref.set('LastPage', str(pdf_data['lastPage']))
                    else:
                        # v1.x style: Use Origin as attribute
                        if origin.get('type'):
                            item_elem.set('Origin', origin['type'])
                        # Note: In v1.x, Source would be handled differently if present
                
                # ALWAYS write Comment attribute if present (works for both v1.x and v2.x)
                if not comment_text:
                    # Fallback to top-level comments field
                    comment_text = var.get('comments')
                if comment_text:
                    item_elem.set('Comment', comment_text)
    
    def _create_code_lists(self, parent: ET.Element, code_lists: List[Dict[str, Any]]) -> None:
        """Create CodeList elements."""
        def_ns = self._get_namespace_uri('def')
        
        for cl in code_lists:
            cl_elem = ET.SubElement(parent, 'CodeList')
            
            # Apply attributes
            self._apply_mapped_attributes(cl_elem, cl)
            
            # Handle both 'OID' and 'oid' field names
            if not cl_elem.get('OID'):
                oid = cl.get('OID') or cl.get('oid', '')
                if oid:
                    cl_elem.set('OID', oid)
            
            # Get supplemental data for this CodeList
            xml_metadata = getattr(self, '_current_xml_metadata', {})
            cl_supplemental = xml_metadata.get('codeListSupplemental', {})
            cl_oid = cl.get('OID') or cl.get('oid', '')
            cl_supp = cl_supplemental.get(cl_oid, {})
            
            # Add def: namespaced attributes from supplemental
            if def_ns:
                # def:StandardOID
                if cl_supp.get('standardOID'):
                    cl_elem.set(f'{{{def_ns}}}StandardOID', cl_supp['standardOID'])
                # def:CommentOID
                if cl_supp.get('commentOID'):
                    cl_elem.set(f'{{{def_ns}}}CommentOID', cl_supp['commentOID'])
                # def:IsNonStandard
                if cl_supp.get('isNonStandard'):
                    cl_elem.set(f'{{{def_ns}}}IsNonStandard', cl_supp['isNonStandard'])
            
            # SASFormatName attribute
            if cl_supp.get('sasFormatName'):
                cl_elem.set('SASFormatName', cl_supp['sasFormatName'])
            
            # Default DataType if missing and fallbacks enabled
            if not cl.get('dataType') and self.enable_fallbacks:
                cl_elem.set('DataType', 'text')
            
            # Check for wasDerivedFrom reference (provenance -> external dictionary)
            derived_from_oid = cl.get('wasDerivedFrom')
            if derived_from_oid:
                # Get dictionaries array from JSON
                json_data = getattr(self, '_current_json_data', {})
                dictionaries = json_data.get('dictionaries', [])
                
                # Find the Dictionary object
                dict_obj = None
                for d in dictionaries:
                    if d.get('OID') == derived_from_oid:
                        dict_obj = d
                        break
                
                if dict_obj:
                    # Create ExternalCodeList element
                    ext_cl_elem = ET.SubElement(cl_elem, 'ExternalCodeList')
                    
                    # Set Dictionary attribute from Dictionary.name
                    if dict_obj.get('name'):
                        ext_cl_elem.set('Dictionary', dict_obj['name'])
                    
                    # Set Version attribute from Dictionary.version
                    if dict_obj.get('version'):
                        ext_cl_elem.set('Version', dict_obj['version'])
                    
                    # Add href/ref from supplemental if present (xlink attrs)
                    xml_metadata = getattr(self, '_current_xml_metadata', {})
                    cl_supplemental = xml_metadata.get('codeListSupplemental', {})
                    cl_oid = cl.get('OID') or cl.get('oid', '')
                    cl_supp = cl_supplemental.get(cl_oid, {})
                    
                    if cl_supp.get('externalCodeListLinks'):
                        links = cl_supp['externalCodeListLinks']
                        if links.get('href'):
                            ext_cl_elem.set('href', links['href'])
                        if links.get('ref'):
                            ext_cl_elem.set('ref', links['ref'])
                    
                    logger.info(f"  - Created ExternalCodeList for {cl_oid} from wasDerivedFrom {derived_from_oid}: {dict_obj['name']} {dict_obj.get('version', '')}")
                else:
                    logger.warning(f"Dictionary {derived_from_oid} referenced by CodeList {cl.get('OID')} not found")
            
            # Fallback: Check for old supplemental data approach
            else:
                xml_metadata = getattr(self, '_current_xml_metadata', {})
                cl_supplemental = xml_metadata.get('codeListSupplemental', {})
                cl_oid = cl.get('OID') or cl.get('oid', '')
                cl_supp = cl_supplemental.get(cl_oid, {})
                
                if cl_supp.get('externalCodeList'):
                    logger.info(f"Creating ExternalCodeList for {cl_oid} from supplemental: {cl_supp['externalCodeList']}")
                    self._create_external_code_list(cl_elem, cl_supp['externalCodeList'])
            
            # Add Alias elements for CodeList from coding array (terminology references)
            codings = cl.get('coding', [])
            for coding_obj in codings:
                alias_elem = ET.SubElement(cl_elem, 'Alias')
                if isinstance(coding_obj, dict):
                    alias_elem.set('Context', coding_obj.get('codeSystem', ''))
                    alias_elem.set('Name', coding_obj.get('code', ''))
                else:
                    # Pydantic Coding object
                    alias_elem.set('Context', coding_obj.codeSystem)
                    alias_elem.set('Name', coding_obj.code)
            
            # Add Alias elements for CodeList (from string aliases)
            aliases = cl.get('aliases', [])
            for alias_str in aliases:
                alias_elem = ET.SubElement(cl_elem, 'Alias')
                # Parse "context|||name" format (using ||| as delimiter)
                if '|||' in alias_str:
                    context, name = alias_str.split('|||', 1)
                    alias_elem.set('Context', context)
                    alias_elem.set('Name', name)
                else:
                    alias_elem.set('Name', alias_str)
            
            # Add CodeListItems or EnumeratedItems based on original element type
            items = cl.get('codeListItems') or cl.get('items', [])
            # Get element types from supplemental data
            xml_metadata = getattr(self, '_current_xml_metadata', {})
            cl_supplemental = xml_metadata.get('codeListSupplemental', {})
            cl_supp = cl_supplemental.get(cl_oid, {})
            # Determine element types based on optimized storage
            item_element_types = cl_supp.get('itemElementTypes', {})
            is_enumerated_list = cl_supp.get('isEnumeratedList', False)
            
            for item in items:
                coded_value = item.get('codedValue')
                # Determine element type using optimized logic:
                # 1. If mixed list (has itemElementTypes) - use mapping
                # 2. If isEnumeratedList flag - all are EnumeratedItem
                # 3. Default - all are CodeListItem
                if item_element_types:
                    element_type = item_element_types.get(coded_value, 'CodeListItem')
                elif is_enumerated_list:
                    element_type = 'EnumeratedItem'
                else:
                    element_type = 'CodeListItem'
                cli_elem = ET.SubElement(cl_elem, element_type)
                cli_elem.set('CodedValue', item.get('codedValue', ''))
                
                # Add Rank from weight field
                # Rank is always non-namespaced in Define-XML (even in 2.1)
                weight = item.get('weight') or item.get('rank')
                if weight is not None:
                    cli_elem.set('Rank', str(weight))
                
                # Add def:ExtendedValue (from supplemental - can be on both CodeListItem and EnumeratedItem)
                if def_ns:
                    if element_type == 'EnumeratedItem':
                        enumerated_supp = cl_supp.get('enumeratedItemSupplemental', {})
                        item_supp = enumerated_supp.get(coded_value, {})
                    else:  # CodeListItem
                        codelist_item_supp = cl_supp.get('codeListItemSupplemental', {})
                        item_supp = codelist_item_supp.get(coded_value, {})
                    
                    if item_supp and item_supp.get('extendedValue'):
                        cli_elem.set(f'{{{def_ns}}}ExtendedValue', item_supp['extendedValue'])
                
                # Add Decode element (only for CodeListItem, not EnumeratedItem)
                if item.get('decode') and element_type == 'CodeListItem':
                    decode = ET.SubElement(cli_elem, 'Decode')
                    trans_text = ET.SubElement(decode, 'TranslatedText')
                    trans_text.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                    trans_text.text = item['decode']
                
                # Add Alias element from coding field (semantic reference)
                coding = item.get('coding', {})
                if coding and (coding.get('codeSystem') or coding.get('code')):
                    alias_elem = ET.SubElement(cli_elem, 'Alias')
                    if coding.get('codeSystem'):
                        alias_elem.set('Context', coding['codeSystem'])
                    if coding.get('code'):
                        alias_elem.set('Name', coding['code'])
    
    def _create_external_code_list(self, parent: ET.Element, ext_cl_data: Dict[str, Any]) -> None:
        """Create an ExternalCodeList element."""
        ext_cl_elem = ET.SubElement(parent, 'ExternalCodeList')
        
        # Add attributes
        if ext_cl_data.get('dictionary'):
            ext_cl_elem.set('Dictionary', ext_cl_data['dictionary'])
        if ext_cl_data.get('version'):
            ext_cl_elem.set('Version', ext_cl_data['version'])
        if ext_cl_data.get('href'):
            ext_cl_elem.set('href', ext_cl_data['href'])
        if ext_cl_data.get('ref'):
            ext_cl_elem.set('ref', ext_cl_data['ref'])
    
    def _create_mdv_leaves(self, parent: ET.Element, leaves: List[Dict[str, Any]]) -> None:
        """Create MetaDataVersion-level def:leaf elements (for display references)."""
        def_ns = self._get_namespace_uri('def')
        if not def_ns:
            return
        
        xlink_ns = self._get_namespace_uri('xlink')
        
        for leaf_data in leaves:
            # Create leaf element
            leaf_elem = ET.SubElement(parent, f'{{{def_ns}}}leaf')
            
            # Add ID attribute
            if leaf_data.get('ID'):
                leaf_elem.set('ID', leaf_data['ID'])
            
            # Add xlink:href attribute
            if leaf_data.get('href') and xlink_ns:
                leaf_elem.set(f'{{{xlink_ns}}}href', leaf_data['href'])
            
            # Add def:title child element
            if leaf_data.get('title'):
                title_elem = ET.SubElement(leaf_elem, f'{{{def_ns}}}title')
                title_elem.text = leaf_data['title']
    
    def _collect_referenced_method_oids(self) -> set:
        """
        Collect all method OIDs referenced by ItemDefs.
        
        ComputationMethods (ARM-specific) are NOT referenced by ItemDefs.
        Only true MethodDef elements are referenced.
        
        Returns:
            Set of method OIDs that should be created as top-level MethodDef elements
        """
        referenced = set()
        json_data = getattr(self, '_current_json_data', {})
        
        # Check top-level items
        for item in json_data.get('items', []):
            # Check both methodOID (Define-XML attribute) and method (inferred field)
            method_oid = item.get('methodOID') or item.get('method')
            if method_oid:
                referenced.add(method_oid)
        
        # Use flattened ItemGroups if available (after _process_item_groups_and_value_lists)
        # This ensures we check ValueLists that were nested in JSON
        item_groups_to_check = getattr(self, '_flattened_item_groups', json_data.get('itemGroups', []))
        
        # Check items within ItemGroups (now using flattened list which includes ValueLists)
        for ig in item_groups_to_check:
            for item in ig.get('items', []):
                # Check both methodOID (Define-XML attribute) and method (inferred field)
                method_oid = item.get('methodOID') or item.get('method')
                if method_oid:
                    referenced.add(method_oid)
        
        logger.info(f"Collected {len(referenced)} referenced method OIDs from {len(item_groups_to_check)} ItemGroups")
        
        return referenced
    
    def _create_comments(self, parent: ET.Element, comments: List[Dict[str, Any]]) -> None:
        """
        Create def:CommentDef elements.
        
        Args:
            parent: Parent MetaDataVersion element
            comments: List of Comment dictionaries
        """
        if not comments:
            return
        
        def_ns = self._get_namespace_uri('def')
        if not def_ns:
            logger.warning("def namespace not found, skipping CommentDef elements")
            return
        
        for comment in comments:
            comment_elem = ET.SubElement(parent, f'{{{def_ns}}}CommentDef')
            
            # Add OID attribute
            comment_oid = comment.get('OID')
            if comment_oid:
                comment_elem.set('OID', comment_oid)
            
            # Add Description (from 'text' field)
            text = comment.get('text')
            if text:
                desc = ET.SubElement(comment_elem, 'Description')
                self._create_translated_text(desc, text)
            
            # Add DocumentRef elements
            documents = comment.get('documents', [])
            for doc in documents:
                leaf_id = doc.get('leafID')
                if leaf_id:
                    doc_ref = ET.SubElement(comment_elem, f'{{{def_ns}}}DocumentRef')
                    doc_ref.set('leafID', leaf_id)
                    
                    # Add PDFPageRef elements if present (stored directly in documents)
                    pdf_page_refs = doc.get('pdfPageRefs', [])
                    for pdf_data in pdf_page_refs:
                        pdf_ref = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                        if pdf_data.get('type'):
                            pdf_ref.set('Type', pdf_data['type'])
                        if pdf_data.get('pageRefs'):
                            pdf_ref.set('PageRefs', pdf_data['pageRefs'])
                        if pdf_data.get('firstPage'):
                            pdf_ref.set('FirstPage', str(pdf_data['firstPage']))
                        if pdf_data.get('lastPage'):
                            pdf_ref.set('LastPage', str(pdf_data['lastPage']))
    
    def _create_methods(self, parent: ET.Element, methods: List[Dict[str, Any]]) -> None:
        """Create MethodDef elements, skipping synthetic methods and ComputationMethods."""
        def_ns = self._get_namespace_uri('def')
        
        # Get supplemental method data for checking markers
        xml_metadata = getattr(self, '_current_xml_metadata', {})
        method_supplemental = xml_metadata.get('methodSupplemental', {})
        
        # INFER ComputationMethods: Collect all method OIDs referenced by ItemDefs
        # ComputationMethods (ARM-specific) have NO ItemDef references
        referenced_method_oids = self._collect_referenced_method_oids()
        
        for method in methods:
            method_oid = method.get('OID', '')
            
            # Get supplemental data for this method
            method_supp = method_supplemental.get(method_oid, {})
            
            # Skip synthetic methods
            if method_supp.get('_isSynthetic', False):
                continue
            
            # INFER: Skip ComputationMethod elements (ARM-specific, not referenced by ItemDefs)
            # BUT: If method is from original XML (_isFromXML), include it even if not referenced
            # This preserves methods that exist in original but aren't referenced by ItemDefs
            if method_oid not in referenced_method_oids:
                # Only skip if it's NOT from original XML
                if not method_supp.get('_isFromXML', False):
                    continue
            
            # Skip auto-generated method OIDs
            if method_oid.startswith('MT.DERIVATION.') or method_oid.startswith('MT.SYNTHETIC.'):
                continue
            
            # In strict mode (no inference), only create methods explicitly from XML as MethodDef
            # Default to False to prevent creating methods that weren't in original
            if not self.enable_inference:
                if not method_supp.get('_isFromXML', False):
                    continue
            
            method_elem = ET.SubElement(parent, 'MethodDef')
            
            # Apply attributes
            self._apply_mapped_attributes(method_elem, method)
            
            # Add Description
            if method.get('description'):
                desc = ET.SubElement(method_elem, 'Description')
                self._create_translated_text(desc, method['description'])
            
            # Add DocumentRef elements
            documents = method.get('documents', [])
            for doc in documents:
                leaf_id = doc.get('leafID')
                if leaf_id and def_ns:
                    doc_ref = ET.SubElement(method_elem, f'{{{def_ns}}}DocumentRef')
                    doc_ref.set('leafID', leaf_id)
                    
                    # Add PDFPageRef elements if present in supplemental metadata
                    pdf_page_refs = method_supp.get(f'pdfPageRefs_{leaf_id}', [])
                    for pdf_data in pdf_page_refs:
                        pdf_ref = ET.SubElement(doc_ref, f'{{{def_ns}}}PDFPageRef')
                        if pdf_data.get('type'):
                            pdf_ref.set('Type', pdf_data['type'])
                        if pdf_data.get('pageRefs'):
                            pdf_ref.set('PageRefs', pdf_data['pageRefs'])
                        if pdf_data.get('firstPage'):
                            pdf_ref.set('FirstPage', str(pdf_data['firstPage']))
                        if pdf_data.get('lastPage'):
                            pdf_ref.set('LastPage', str(pdf_data['lastPage']))
            
            # Add FormalExpression if present in expressions (odm namespace, not def)
            expressions = method.get('expressions', [])
            odm_ns = self._get_namespace_uri('odm')
            for expr in expressions:
                if isinstance(expr, dict):
                    formal_expr = ET.SubElement(method_elem, f'{{{odm_ns}}}FormalExpression' if odm_ns else 'FormalExpression')
                    if expr.get('context'):
                        formal_expr.set('Context', expr['context'])
                    if expr.get('expression'):
                        formal_expr.text = expr['expression']
    
    def _write_xml(self, root: ET.Element, output_path: Path) -> None:
        """
        Write XML to file with pretty formatting.
        
        Uses minidom for pretty printing but preserves significant whitespace
        in text nodes by avoiding toprettyxml's text reformatting.
        """
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Write directly without minidom pretty printing to preserve text whitespace
        # The original XML formatting is already preserved from the serialized containers
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(xml_str)
        
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
        print(f"Conversion complete. Output written to {output_path}")
    except Exception as e:
        print(f"Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()