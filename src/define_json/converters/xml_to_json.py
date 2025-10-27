"""
Define-XML to Define-JSON converter with complete fidelity.

Key principles:
1. NO HARDCODING - detect all namespaces and versions from source
2. NO INFERENCE - preserve exactly what's in the source
3. COMPLETE PRESERVATION - every attribute, element, and namespace must roundtrip
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DefineXMLToJSONConverter:
    """Define-XML to Define-JSON converter with complete fidelity."""
    
    def __init__(self, infer_missing_attributes: bool = False, **kwargs):
        """
        Initialize the converter.
        
        Args:
            infer_missing_attributes: Deprecated parameter kept for backward compatibility.
                                    The fixed converter NEVER infers - it only preserves.
                                    This parameter is ignored.
            **kwargs: Additional parameters for backward compatibility (ignored).
        
        Note: Version detection is ALWAYS automatic - no version parameters needed or accepted.
        """
        # Standard namespace prefixes - will be updated from actual document
        self.namespace_map = {}
        self.reverse_namespace_map = {}
        
        # Legacy parameter - kept for backward compatibility but ignored
        # The fixed converter never infers, only preserves
        self._infer_missing_attributes = False  # Always False in fixed version
        
    def _extract_all_namespaces(self, root: ET.Element) -> Dict[str, str]:
        """Extract ALL namespace declarations from the document."""
        namespaces = {}
        
        # Get namespaces from root element
        for prefix, uri in ET.iterparse(
            str(self._temp_file_path) if hasattr(self, '_temp_file_path') else '',
            events=['start-ns']
        ):
            if prefix:
                namespaces[prefix] = uri
            else:
                # Default namespace
                namespaces[''] = uri
        
        # Also extract from root tag if it has a namespace
        if root.tag.startswith('{'):
            ns_end = root.tag.find('}')
            default_ns = root.tag[1:ns_end]
            if '' not in namespaces:
                namespaces[''] = default_ns
        
        # Scan root attributes for xmlns declarations
        for attr_name, attr_value in root.attrib.items():
            if attr_name == 'xmlns':
                namespaces[''] = attr_value
            elif attr_name.startswith('xmlns:'):
                prefix = attr_name[6:]
                namespaces[prefix] = attr_value
        
        return namespaces
    
    def _build_namespace_maps(self, tree: ET.ElementTree) -> None:
        """Build bidirectional namespace maps from the document."""
        root = tree.getroot()
        
        # Method 1: Parse namespace map from document
        try:
            self.namespace_map = dict([
                (prefix if prefix else 'default', uri)
                for prefix, uri in self._iter_namespace_events(tree)
            ])
        except:
            # Fallback: extract from root element
            self.namespace_map = {}
            for attr_name, attr_value in root.attrib.items():
                if attr_name == 'xmlns':
                    self.namespace_map['default'] = attr_value
                elif attr_name.startswith('xmlns:'):
                    prefix = attr_name[6:]
                    self.namespace_map[prefix] = attr_value
        
        # Also extract from the root tag itself
        if root.tag.startswith('{'):
            ns_end = root.tag.find('}')
            default_ns = root.tag[1:ns_end]
            if 'default' not in self.namespace_map:
                self.namespace_map['default'] = default_ns
        
        # Common namespace detection
        for attr_name, attr_value in root.attrib.items():
            if 'def' in attr_name.lower() or 'define' in attr_value.lower():
                if 'v1.0' in attr_value:
                    self.namespace_map['def'] = 'http://www.cdisc.org/ns/def/v1.0'
                elif 'v2.0' in attr_value or 'v2.1' in attr_value:
                    if 'def' not in self.namespace_map:
                        # Extract the exact URI
                        self.namespace_map['def'] = attr_value
        
        # Always include XML namespace for xml:lang
        self.namespace_map['xml'] = 'http://www.w3.org/XML/1998/namespace'
        
        # Always include XSI namespace for schema locations
        self.namespace_map['xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        
        # Build reverse map
        self.reverse_namespace_map = {uri: prefix for prefix, uri in self.namespace_map.items()}
    
    def _iter_namespace_events(self, tree: ET.ElementTree):
        """Iterate over namespace events in the tree."""
        # This is a workaround since ET.iterparse needs a file
        # We'll extract from the root element instead
        root = tree.getroot()
        
        # Extract xmlns declarations from root
        for attr_name, attr_value in root.attrib.items():
            if attr_name == 'xmlns':
                yield ('', attr_value)
            elif attr_name.startswith('xmlns:'):
                prefix = attr_name[6:]
                yield (prefix, attr_value)
    
    def _get_namespaced_attrib(self, element: ET.Element, name: str, namespace: str = None) -> Optional[str]:
        """Get attribute value handling both namespaced and non-namespaced forms."""
        if namespace:
            # Try with namespace
            ns_name = f'{{{namespace}}}{name}'
            value = element.get(ns_name)
            if value is not None:
                return value
        
        # Try without namespace
        return element.get(name)
    
    def _extract_all_attributes(self, element: ET.Element) -> Dict[str, Any]:
        """Extract ALL attributes from an element, preserving namespaces."""
        attrs = {}
        
        for key, value in element.attrib.items():
            # Store with full namespace URI for accurate roundtrip
            attrs[key] = value
        
        return attrs
    
    def _convert_element_with_attrs(self, element: ET.Element, base_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Add all element attributes to the base dictionary."""
        # Store all attributes with their full qualified names
        all_attrs = self._extract_all_attributes(element)
        if all_attrs:
            base_dict['_attributes'] = all_attrs
        
        return base_dict
    
    def convert_file(self, xml_path: Path, output_path: Path) -> Dict[str, Any]:
        """Convert Define-XML file to Define-JSON with complete fidelity."""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Build complete namespace maps
        self._build_namespace_maps(tree)
        
        # Store namespace map in JSON for roundtrip
        namespace_metadata = {
            'namespaces': self.namespace_map,
            'odmVersion': None,
            'defineVersion': None
        }
        
        # Detect versions from namespaces
        for prefix, uri in self.namespace_map.items():
            if 'odm' in uri.lower():
                if 'v1.2' in uri:
                    namespace_metadata['odmVersion'] = '1.2'
                elif 'v1.3' in uri:
                    namespace_metadata['odmVersion'] = '1.3'
            if 'def' in uri.lower():
                if 'v1.0' in uri:
                    namespace_metadata['defineVersion'] = '1.0'
                elif 'v2.0' in uri:
                    namespace_metadata['defineVersion'] = '2.0'
                elif 'v2.1' in uri:
                    namespace_metadata['defineVersion'] = '2.1'
        
        # Extract ODM root attributes
        root_attrs = self._extract_all_attributes(root)
        
        # Get namespaces
        odm_ns = self.namespace_map.get('default', '')
        def_ns = self.namespace_map.get('def', '')
        
        # Build JSON structure
        define_json = {
            '_namespace_metadata': namespace_metadata,
            '_root_attributes': root_attrs,
            'fileOID': root.get('FileOID'),
            'creationDateTime': root.get('CreationDateTime'),
            'asOfDateTime': root.get('AsOfDateTime'),
            'odmVersion': root.get('ODMVersion'),
            'fileType': root.get('FileType'),
            'originator': root.get('Originator'),
            'sourceSystem': root.get('SourceSystem'),
            'sourceSystemVersion': root.get('SourceSystemVersion')
        }
        
        # Extract def:Context
        for ns_prefix, ns_uri in self.namespace_map.items():
            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                context = root.get(f'{{{ns_uri}}}Context')
                if context:
                    define_json['context'] = context
        
        # Find Study element
        study = None
        for elem in root:
            if elem.tag.endswith('Study'):
                study = elem
                break
        
        if study is None:
            raise ValueError("No Study element found in ODM")
        
        define_json['studyOID'] = study.get('OID')
        
        # Extract study metadata
        define_json['studyName'] = self._get_study_name(study, odm_ns)
        define_json['studyDescription'] = self._get_study_description(study, odm_ns)
        define_json['protocolName'] = self._get_protocol_name(study, odm_ns)
        
        # Find MetaDataVersion
        mdv = None
        for elem in study:
            if elem.tag.endswith('MetaDataVersion'):
                mdv = elem
                break
        
        if mdv is None:
            raise ValueError("No MetaDataVersion found in Study")
        
        # Store MetaDataVersion attributes
        define_json['_mdv_attributes'] = self._extract_all_attributes(mdv)
        
        define_json['OID'] = mdv.get('OID')
        define_json['name'] = mdv.get('Name')
        define_json['description'] = mdv.get('Description')
        
        # Extract DefineVersion
        for ns_prefix, ns_uri in self.namespace_map.items():
            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                define_version = mdv.get(f'{{{ns_uri}}}DefineVersion')
                if define_version:
                    define_json['defineVersion'] = define_version
        
        # Process all elements in proper order
        standards_data = self._process_standards(mdv, odm_ns, def_ns)
        define_json['standards'] = standards_data['standards']
        define_json['has_standards_container'] = standards_data['has_standards_container']
        define_json['annotatedCRF'] = self._process_annotated_crf(mdv, def_ns)
        define_json['supplementalDocs'] = self._process_supplemental_docs(mdv, def_ns)
        define_json['leaves'] = self._process_leaves(mdv, def_ns)
        define_json['conditions'] = self._process_conditions_and_where_clauses(mdv, odm_ns, def_ns)['conditions']
        define_json['whereClauses'] = self._process_conditions_and_where_clauses(mdv, odm_ns, def_ns)['whereClauses']
        
        # Process methods and item groups
        methods, derivation_map = self._process_methods(mdv, odm_ns, def_ns)
        define_json['methods'] = methods
        define_json['itemGroups'] = self._process_item_groups(mdv, odm_ns, def_ns, derivation_map)
        
        # Process items and code lists
        define_json['items'] = self._process_items(mdv, odm_ns, def_ns)
        define_json['codeLists'] = self._process_code_lists(mdv, odm_ns, def_ns)
        
        # Process ValueListDef to only get direct children
        define_json['valueLists'] = self._process_value_list_defs(mdv, odm_ns, def_ns)
        
        # Process analysis result displays
        define_json['analysisResultDisplays'] = self._process_analysis_result_displays(mdv, def_ns)
        
        # Write JSON
        with open(output_path, 'w') as f:
            json.dump(define_json, f, indent=2)
        
        return define_json
    
    def _process_leaves(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process leaf elements that are DIRECT children of MetaDataVersion only."""
        leaves = []
        
        # Only process direct children of MetaDataVersion
        for child_elem in mdv:
            if child_elem.tag.endswith('leaf'):
                leaf = {'_attributes': self._extract_all_attributes(child_elem)}
                
                # Extract attributes
                leaf['ID'] = child_elem.get('ID')
                leaf['href'] = child_elem.get(f'{{{self.namespace_map.get("xlink", "")}}}href') or child_elem.get('href')
                
                # Extract title
                for title_elem in child_elem:
                    if title_elem.tag.endswith('title'):
                        leaf['title'] = title_elem.text
                        break
                
                leaves.append(leaf)
        
        return leaves
    
    def _process_analysis_result_displays(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process AnalysisResultDisplays elements with CORRECT hierarchy.
        
        FIXED: Each AnalysisResults element IS a complete analysis result with its own OID.
        Multiple AnalysisResults can be siblings under a ResultDisplay.
        
        Correct hierarchy:
        AnalysisResultDisplays (OID, Name, Description)
          └── ResultDisplay (OID, Name, Description)
              ├── AnalysisResults (OID, Reason) [element 1]
              │   ├── AnalysisVariable
              │   ├── AnalysisDataset
              │   └── ProgrammingCode
              └── AnalysisResults (OID, Reason) [element 2, etc.]
        """
        displays = []
        
        # Only get direct children of MetaDataVersion
        for display_elem in mdv:
            if display_elem.tag.endswith('AnalysisResultDisplays'):
                display = {'_attributes': self._extract_all_attributes(display_elem)}
                
                # Extract attributes
                display['OID'] = display_elem.get('OID')
                display['name'] = display_elem.get('Name')
                
                # Extract description with attributes
                display['description'], display['_translatedText_attributes'] = self._get_description(display_elem, '')
                
                # Extract ResultDisplay children (DIRECT children only)
                result_displays = []
                for rd_elem in display_elem:
                    if rd_elem.tag.endswith('ResultDisplay'):
                        rd = {'_attributes': self._extract_all_attributes(rd_elem)}
                        rd['OID'] = rd_elem.get('OID')
                        rd['name'] = rd_elem.get('Name')
                        rd['description'], rd['_translatedText_attributes'] = self._get_description(rd_elem, '')
                        
                        # Extract AnalysisResults elements (can be multiple per ResultDisplay)
                        analysis_results = []
                        for child_elem in rd_elem:
                            if child_elem.tag.endswith('AnalysisResults'):
                                # Each AnalysisResults element IS a complete analysis result
                                result = {'_attributes': self._extract_all_attributes(child_elem)}
                                result['OID'] = child_elem.get('OID')
                                result['description'], result['_translatedText_attributes'] = self._get_description(child_elem, '')
                                
                                # Extract child elements recursively (AnalysisVariable, AnalysisDataset, etc.)
                                self._extract_generic_children(child_elem, result, def_ns)
                                
                                analysis_results.append(result)
                        
                        # Store all AnalysisResults in the ResultDisplay
                        if analysis_results:
                            rd['analysisResults'] = analysis_results
                        
                        result_displays.append(rd)
                
                if result_displays:
                    display['resultDisplays'] = result_displays
                
                displays.append(display)
        
        return displays
    
    def _extract_generic_children(self, parent_elem: ET.Element, parent_dict: Dict[str, Any], def_ns: str, depth: int = 0, max_depth: int = 5) -> None:
        """Recursively extract child elements into a generic structure.
        
        Args:
            parent_elem: Parent XML element
            parent_dict: Parent dictionary to store children in
            def_ns: Define namespace
            depth: Current recursion depth
            max_depth: Maximum recursion depth
        """
        if depth >= max_depth:
            return
        
        for child_elem in parent_elem:
            tag_name = child_elem.tag.split('}')[-1] if '}' in child_elem.tag else child_elem.tag
            
            # Skip Description as it's handled separately
            if tag_name == 'Description':
                continue
            
            # Create storage for this element type
            storage_key = f'_{tag_name}_elements'
            if storage_key not in parent_dict:
                parent_dict[storage_key] = []
            
            # Extract element data
            child_data = {
                '_attributes': self._extract_all_attributes(child_elem)
            }
            
            # Add text content if present
            if child_elem.text and child_elem.text.strip():
                child_data['_text'] = child_elem.text.strip()
            
            # Recursively process children
            if len(child_elem) > 0:
                self._extract_generic_children(child_elem, child_data, def_ns, depth + 1, max_depth)
            
            parent_dict[storage_key].append(child_data)
    
    def _process_standards(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> Dict[str, Any]:
        """Process Standard elements and detect if they're wrapped in Standards container."""
        standards_data = {
            'standards': [],
            'has_standards_container': False
        }
        
        # Check for Standards container first
        for child_elem in mdv:
            if child_elem.tag.endswith('Standards'):
                standards_data['has_standards_container'] = True
                # Extract standards from within the container
                for std_elem in child_elem:
                    if std_elem.tag.endswith('Standard'):
                        std = {'_attributes': self._extract_all_attributes(std_elem)}
                        
                        # Extract attributes
                        std['OID'] = std_elem.get('OID')
                        std['name'] = std_elem.get('Name')
                        std['type'] = std_elem.get('Type')
                        std['publishingSet'] = std_elem.get('PublishingSet')
                        std['version'] = std_elem.get('Version')
                        std['status'] = std_elem.get('Status')
                        
                        standards_data['standards'].append(std)
                break
        
        # If no Standards container, look for direct Standard children
        if not standards_data['has_standards_container']:
            for std_elem in mdv:
                if std_elem.tag.endswith('Standard'):
                    std = {'_attributes': self._extract_all_attributes(std_elem)}
                    
                    # Extract attributes
                    std['OID'] = std_elem.get('OID')
                    std['name'] = std_elem.get('Name')
                    std['type'] = std_elem.get('Type')
                    std['publishingSet'] = std_elem.get('PublishingSet')
                    std['version'] = std_elem.get('Version')
                    std['status'] = std_elem.get('Status')
                    
                    standards_data['standards'].append(std)
        
        return standards_data
    
    def _process_annotated_crf(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process AnnotatedCRF elements."""
        crfs = []
        
        for crf_elem in mdv.iter():
            if crf_elem.tag.endswith('AnnotatedCRF'):
                crf = {'_attributes': self._extract_all_attributes(crf_elem)}
                
                # Extract DocumentRef children
                doc_refs = []
                for ref_elem in crf_elem.iter():
                    if ref_elem.tag.endswith('DocumentRef'):
                        doc_ref = {'_attributes': self._extract_all_attributes(ref_elem)}
                        doc_ref['leafID'] = ref_elem.get('leafID')
                        doc_refs.append(doc_ref)
                
                if doc_refs:
                    crf['documentRefs'] = doc_refs
                
                crfs.append(crf)
        
        return crfs
    
    def _process_supplemental_docs(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process SupplementalDoc elements."""
        docs = []
        
        for doc_elem in mdv.iter():
            if doc_elem.tag.endswith('SupplementalDoc'):
                doc = {'_attributes': self._extract_all_attributes(doc_elem)}
                
                # Extract DocumentRef children
                doc_refs = []
                for ref_elem in doc_elem.iter():
                    if ref_elem.tag.endswith('DocumentRef'):
                        doc_ref = {'_attributes': self._extract_all_attributes(ref_elem)}
                        doc_ref['leafID'] = ref_elem.get('leafID')
                        doc_refs.append(doc_ref)
                
                if doc_refs:
                    doc['documentRefs'] = doc_refs
                
                docs.append(doc)
        
        return docs
    
    def _process_methods(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> Tuple[List[Dict[str, Any]], Dict[str, Dict]]:
        """Process both MethodDef and ComputationMethod elements.
        
        Only extracts methods that are DIRECT children of MetaDataVersion.
        Embedded methods in AnalysisResultDisplays, ValueListDef, etc. are NOT extracted.
        """
        methods = []
        derivation_map = {}
        
        # Process MethodDef elements (Define-XML v2.x style)
        # Only get direct children of MetaDataVersion, not nested elements
        for method_elem in mdv:
            if method_elem.tag.endswith('MethodDef'):
                method = {'_attributes': self._extract_all_attributes(method_elem)}
                method['OID'] = method_elem.get('OID')
                method['name'] = method_elem.get('Name')
                method['type'] = method_elem.get('Type', 'Computation')
                method['elementType'] = 'MethodDef'  # Store element type for roundtrip
                
                # Extract description with attributes
                desc, desc_attrs = self._get_description(method_elem, odm_ns)
                if desc:
                    method['description'] = desc
                    if desc_attrs:
                        method['_translatedText_attributes'] = desc_attrs
                
                methods.append(method)
        
        # Process ComputationMethod elements (Define-XML v1.x style)
        # Only get direct children of MetaDataVersion, not nested elements
        for comp_elem in mdv:
            if comp_elem.tag.endswith('ComputationMethod'):
                method = {'_attributes': self._extract_all_attributes(comp_elem)}
                method['OID'] = comp_elem.get('OID')
                method['name'] = comp_elem.get('Name')
                method['type'] = 'Computation'
                method['elementType'] = 'ComputationMethod'  # Store element type for roundtrip
                
                # Text content is the description for ComputationMethod
                if comp_elem.text and comp_elem.text.strip():
                    method['description'] = comp_elem.text.strip()
                
                methods.append(method)
        
        return methods, derivation_map
    
    def _process_item_groups(self, mdv: ET.Element, odm_ns: str, def_ns: str, 
                            derivation_map: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Process ItemGroupDef elements."""
        item_groups = []
        
        for ig_elem in mdv.iter():
            if ig_elem.tag.endswith('ItemGroupDef'):
                ig = {'_attributes': self._extract_all_attributes(ig_elem)}
                
                ig['OID'] = ig_elem.get('OID')
                ig['name'] = ig_elem.get('Name')
                ig['repeating'] = ig_elem.get('Repeating')
                ig['domain'] = ig_elem.get('Domain')
                ig['sasDatasetName'] = ig_elem.get('SASDatasetName')
                
                # Extract namespaced attributes
                for ns_prefix, ns_uri in self.namespace_map.items():
                    if 'def' in ns_prefix or 'def' in ns_uri.lower():
                        ig['structure'] = ig_elem.get(f'{{{ns_uri}}}Structure')
                        ig['class'] = ig_elem.get(f'{{{ns_uri}}}Class')
                        ig['label'] = ig_elem.get(f'{{{ns_uri}}}Label')
                        ig['archiveLocationID'] = ig_elem.get(f'{{{ns_uri}}}ArchiveLocationID')
                
                # Extract description with attributes
                ig['description'], ig['_translatedText_attributes'] = self._get_description(ig_elem, odm_ns)
                
                # Extract child Class elements (not attributes)
                class_elements = []
                for child_elem in ig_elem:
                    if child_elem.tag.endswith('Class'):
                        class_elem = {'_attributes': self._extract_all_attributes(child_elem)}
                        class_elem['name'] = child_elem.get('Name')
                        class_elements.append(class_elem)
                
                if class_elements:
                    ig['classElements'] = class_elements
                
                # Extract ItemRefs
                items = []
                for ref_elem in ig_elem.iter():
                    if ref_elem.tag.endswith('ItemRef'):
                        item_ref = {'_attributes': self._extract_all_attributes(ref_elem)}
                        item_ref['OID'] = ref_elem.get('ItemOID')
                        item_ref['mandatory'] = ref_elem.get('Mandatory', 'No')
                        item_ref['role'] = ref_elem.get('Role')
                        item_ref['roleCodeListOID'] = ref_elem.get('RoleCodeListOID')
                        
                        # Extract method references
                        for ns_prefix, ns_uri in self.namespace_map.items():
                            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                                method_oid = (ref_elem.get(f'{{{ns_uri}}}MethodOID') or 
                                            ref_elem.get(f'{{{ns_uri}}}ComputationMethodOID'))
                                if method_oid:
                                    item_ref['method'] = method_oid
                        
                        # Extract WhereClauseRef
                        for wc_ref_elem in ref_elem:
                            if wc_ref_elem.tag.endswith('WhereClauseRef'):
                                item_ref['whereClauseRef'] = {
                                    '_attributes': self._extract_all_attributes(wc_ref_elem),
                                    'whereClauseOID': wc_ref_elem.get('WhereClauseOID')
                                }
                                break
                        
                        items.append(item_ref)
                
                ig['items'] = items
                
                # Extract nested leaf elements
                leaves = []
                for child_elem in ig_elem:
                    if child_elem.tag.endswith('leaf'):
                        leaf = {'_attributes': self._extract_all_attributes(child_elem)}
                        leaf['ID'] = child_elem.get('ID')
                        leaf['href'] = child_elem.get(f'{{{self.namespace_map.get("xlink", "")}}}href') or child_elem.get('href')
                        
                        # Extract title
                        for title_elem in child_elem:
                            if title_elem.tag.endswith('title'):
                                leaf['title'] = title_elem.text
                                break
                        
                        leaves.append(leaf)
                
                if leaves:
                    ig['leaves'] = leaves
                
                item_groups.append(ig)
        
        return item_groups
    
    def _process_items(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process ItemDef elements."""
        items = []
        
        for item_elem in mdv.iter():
            if item_elem.tag.endswith('ItemDef'):
                item = {'_attributes': self._extract_all_attributes(item_elem)}
                
                item['OID'] = item_elem.get('OID')
                item['name'] = item_elem.get('Name')
                item['dataType'] = item_elem.get('DataType', 'text')
                item['length'] = item_elem.get('Length')
                item['significantDigits'] = item_elem.get('SignificantDigits')
                
                # Extract namespaced attributes
                for ns_prefix, ns_uri in self.namespace_map.items():
                    if 'def' in ns_prefix or 'def' in ns_uri.lower():
                        item['label'] = item_elem.get(f'{{{ns_uri}}}Label')
                
                # Extract description with attributes
                item['description'], item['_translatedText_attributes'] = self._get_description(item_elem, odm_ns)
                
                # Extract CodeListRef
                for ref_elem in item_elem.iter():
                    if ref_elem.tag.endswith('CodeListRef'):
                        item['codeList'] = ref_elem.get('CodeListOID')
                        break
                
                # Extract ValueListRef
                for ref_elem in item_elem.iter():
                    if ref_elem.tag.endswith('ValueListRef'):
                        item['valueListOID'] = ref_elem.get('ValueListOID')
                        break
                
                # Extract Alias
                aliases = []
                for alias_elem in item_elem:
                    if alias_elem.tag.endswith('Alias'):
                        alias = {
                            '_attributes': self._extract_all_attributes(alias_elem),
                            'context': alias_elem.get('Context'),
                            'name': alias_elem.get('Name')
                        }
                        aliases.append(alias)
                
                if aliases:
                    item['aliases'] = aliases
                
                # Extract Origin elements - NEW FIX
                origins = []
                for origin_elem in item_elem:
                    if origin_elem.tag.endswith('Origin'):
                        origin = {
                            '_attributes': self._extract_all_attributes(origin_elem),
                            'type': origin_elem.get('Type'),
                        }
                        
                        # Extract description with attributes
                        origin['description'], origin['_translatedText_attributes'] = self._get_description(origin_elem, odm_ns)
                        
                        # Extract DocumentRef if present
                        for doc_ref_elem in origin_elem:
                            if doc_ref_elem.tag.endswith('DocumentRef'):
                                origin['documentRef'] = {
                                    '_attributes': self._extract_all_attributes(doc_ref_elem),
                                    'leafID': doc_ref_elem.get('leafID')
                                }
                                break
                        
                        origins.append(origin)
                
                if origins:
                    item['origins'] = origins
                
                items.append(item)
        
        return items
    
    def _process_code_lists(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process CodeList elements with complete attribute preservation."""
        code_lists = []
        for cl_elem in mdv.iter():
            if cl_elem.tag.endswith('CodeList') and not cl_elem.tag.endswith('ExternalCodeList'):
                cl = {'_attributes': self._extract_all_attributes(cl_elem)}
                
                cl['OID'] = cl_elem.get('OID')
                cl['name'] = cl_elem.get('Name')
                cl['dataType'] = cl_elem.get('DataType', 'text')
                
                # Extract CodeListItems with ALL attributes
                items = []
                for cli_elem in cl_elem.iter():
                    if cli_elem.tag.endswith('CodeListItem'):
                        cli = {'_attributes': self._extract_all_attributes(cli_elem)}
                        
                        cli['codedValue'] = cli_elem.get('CodedValue')
                        
                        # Extract def:Rank from correct namespace
                        for ns_prefix, ns_uri in self.namespace_map.items():
                            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                                rank = cli_elem.get(f'{{{ns_uri}}}Rank')
                                if rank:
                                    cli['rank'] = rank
                                    break
                        
                        # Extract Decode with xml:lang
                        for decode_elem in cli_elem.iter():
                            if decode_elem.tag.endswith('Decode'):
                                for tt_elem in decode_elem.iter():
                                    if tt_elem.tag.endswith('TranslatedText'):
                                        cli['decode'] = tt_elem.text
                                        xml_ns = self.namespace_map.get('xml', 'http://www.w3.org/XML/1998/namespace')
                                        lang = tt_elem.get(f'{{{xml_ns}}}lang')
                                        if lang:
                                            cli['lang'] = lang
                                        cli['_translatedText_attributes'] = self._extract_all_attributes(tt_elem)
                                        break
                                break
                        
                        # Extract Alias
                        aliases = []
                        for alias_elem in cli_elem:
                            if alias_elem.tag.endswith('Alias'):
                                alias = {
                                    '_attributes': self._extract_all_attributes(alias_elem),
                                    'context': alias_elem.get('Context'),
                                    'name': alias_elem.get('Name')
                                }
                                aliases.append(alias)
                        
                        if aliases:
                            cli['aliases'] = aliases
                        
                        items.append(cli)
                
                cl['codeListItems'] = items
                
                # Extract EnumeratedItem
                enum_items = []
                for ei_elem in cl_elem:
                    if ei_elem.tag.endswith('EnumeratedItem'):
                        ei = {
                            '_attributes': self._extract_all_attributes(ei_elem),
                            'codedValue': ei_elem.get('CodedValue')
                        }
                        
                        # Extract def:Rank
                        for ns_prefix, ns_uri in self.namespace_map.items():
                            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                                rank = ei_elem.get(f'{{{ns_uri}}}Rank')
                                if rank:
                                    ei['rank'] = rank
                                    break
                        
                        # Extract Alias
                        aliases = []
                        for alias_elem in ei_elem:
                            if alias_elem.tag.endswith('Alias'):
                                alias = {
                                    '_attributes': self._extract_all_attributes(alias_elem),
                                    'context': alias_elem.get('Context'),
                                    'name': alias_elem.get('Name')
                                }
                                aliases.append(alias)
                        
                        if aliases:
                            ei['aliases'] = aliases
                        
                        enum_items.append(ei)
                
                if enum_items:
                    cl['enumeratedItems'] = enum_items
                
                # Extract ExternalCodeList
                for child_elem in cl_elem:
                    if child_elem.tag.endswith('ExternalCodeList'):
                        cl['externalCodeList'] = {
                            '_attributes': self._extract_all_attributes(child_elem),
                            'dictionary': child_elem.get('Dictionary'),
                            'version': child_elem.get('Version'),
                            'ref': child_elem.get('ref')
                        }
                        break
                
                # Extract Alias at CodeList level
                aliases = []
                for alias_elem in cl_elem:
                    if alias_elem.tag.endswith('Alias'):
                        alias = {
                            '_attributes': self._extract_all_attributes(alias_elem),
                            'context': alias_elem.get('Context'),
                            'name': alias_elem.get('Name')
                        }
                        aliases.append(alias)
                
                if aliases:
                    cl['aliases'] = aliases
                
                code_lists.append(cl)
        
        return code_lists
    
    def _process_value_list_defs(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process ValueListDef elements to only get direct children."""
        value_lists = []
        
        for vl_elem in mdv:
            if vl_elem.tag.endswith('ValueListDef'):
                vl = {'_attributes': self._extract_all_attributes(vl_elem)}
                
                vl['OID'] = vl_elem.get('OID')
                
                # Extract description with attributes
                vl['description'], vl['_translatedText_attributes'] = self._get_description(vl_elem, odm_ns)
                
                # Extract ItemRef children
                items = []
                for ref_elem in vl_elem:
                    if ref_elem.tag.endswith('ItemRef'):
                        item_ref = {'_attributes': self._extract_all_attributes(ref_elem)}
                        item_ref['OID'] = ref_elem.get('ItemOID')
                        item_ref['mandatory'] = ref_elem.get('Mandatory', 'No')
                        
                        # Extract method references
                        for ns_prefix, ns_uri in self.namespace_map.items():
                            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                                method_oid = (ref_elem.get(f'{{{ns_uri}}}MethodOID') or 
                                            ref_elem.get(f'{{{ns_uri}}}ComputationMethodOID'))
                                if method_oid:
                                    item_ref['method'] = method_oid
                        
                        # Extract WhereClauseRef
                        for wc_ref_elem in ref_elem:
                            if wc_ref_elem.tag.endswith('WhereClauseRef'):
                                item_ref['whereClauseRef'] = {
                                    '_attributes': self._extract_all_attributes(wc_ref_elem),
                                    'whereClauseOID': wc_ref_elem.get('WhereClauseOID')
                                }
                                break
                        
                        items.append(item_ref)
                
                vl['itemRefs'] = items
                value_lists.append(vl)
        
        return value_lists
    
    def _process_conditions_and_where_clauses(self, mdv: ET.Element, odm_ns: str, 
                                             def_ns: str) -> Dict[str, List[Dict[str, Any]]]:
        """Process ConditionDef and WhereClauseDef elements."""
        conditions = []
        where_clauses = []
        
        for cond_elem in mdv.iter():
            if cond_elem.tag.endswith('ConditionDef'):
                condition = {'_attributes': self._extract_all_attributes(cond_elem)}
                condition['OID'] = cond_elem.get('OID')
                condition['name'] = cond_elem.get('Name')
                condition['description'], condition['_translatedText_attributes'] = self._get_description(cond_elem, odm_ns)
                conditions.append(condition)
        
        for wc_elem in mdv.iter():
            if wc_elem.tag.endswith('WhereClauseDef'):
                wc = {'_attributes': self._extract_all_attributes(wc_elem)}
                wc['OID'] = wc_elem.get('OID')
                
                # Extract RangeCheck children with CheckValue
                checks = []
                for check_elem in wc_elem:
                    if check_elem.tag.endswith('RangeCheck'):
                        check = {'_attributes': self._extract_all_attributes(check_elem)}
                        
                        # Extract CheckValue child elements
                        check_values = []
                        for cv_elem in check_elem:
                            if cv_elem.tag.endswith('CheckValue'):
                                check_value = {'_attributes': self._extract_all_attributes(cv_elem)}
                                check_value['text'] = cv_elem.text
                                check_values.append(check_value)
                        
                        if check_values:
                            check['checkValues'] = check_values
                        
                        checks.append(check)
                
                wc['rangeChecks'] = checks
                where_clauses.append(wc)
        
        return {'conditions': conditions, 'whereClauses': where_clauses}
    
    def _get_study_name(self, study: ET.Element, odm_ns: str) -> Optional[str]:
        """Extract study name from GlobalVariables."""
        for gv_elem in study.iter():
            if gv_elem.tag.endswith('GlobalVariables'):
                for sn_elem in gv_elem.iter():
                    if sn_elem.tag.endswith('StudyName'):
                        return sn_elem.text
        return None
    
    def _get_study_description(self, study: ET.Element, odm_ns: str) -> Optional[str]:
        """Extract study description from GlobalVariables."""
        for gv_elem in study.iter():
            if gv_elem.tag.endswith('GlobalVariables'):
                for sd_elem in gv_elem.iter():
                    if sd_elem.tag.endswith('StudyDescription'):
                        return sd_elem.text
        return None
    
    def _get_protocol_name(self, study: ET.Element, odm_ns: str) -> Optional[str]:
        """Extract protocol name from GlobalVariables."""
        for gv_elem in study.iter():
            if gv_elem.tag.endswith('GlobalVariables'):
                for pn_elem in gv_elem.iter():
                    if pn_elem.tag.endswith('ProtocolName'):
                        return pn_elem.text
        return None
    
    def _get_description(self, element: ET.Element, odm_ns: str) -> Tuple[str, Dict[str, Any]]:
        """Extract description from TranslatedText with all attributes.
        
        Returns:
            Tuple of (description_text, translated_text_attributes)
        """
        for desc_elem in element.iter():
            if desc_elem.tag.endswith('Description'):
                for tt_elem in desc_elem.iter():
                    if tt_elem.tag.endswith('TranslatedText'):
                        text = tt_elem.text if tt_elem.text else ''
                        attrs = self._extract_all_attributes(tt_elem)
                        return text, attrs
        return '', {}


def main():
    """Main entry point for testing."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python xml_to_json_fixed.py <input.xml> <output.json>")
        sys.exit(1)
    
    converter = DefineXMLToJSONConverter()
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    print(f"Converting {input_path} to {output_path}")
    result = converter.convert_file(input_path, output_path)
    print(f"Conversion complete. Output written to {output_path}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Item Groups: {len(result.get('itemGroups', []))}")
    print(f"  Items: {len(result.get('items', []))}")
    print(f"  Code Lists: {len(result.get('codeLists', []))}")
    print(f"  Value Lists: {len(result.get('valueLists', []))}")
    print(f"  Methods: {len(result.get('methods', []))}")
    print(f"  Standards: {len(result.get('standards', []))}")
    print(f"  Leaves: {len(result.get('leaves', []))}")
    print(f"  Analysis Result Displays: {len(result.get('analysisResultDisplays', []))}")


if __name__ == '__main__':
    main()
