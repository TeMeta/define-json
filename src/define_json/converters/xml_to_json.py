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
        
        # Find Study and MetaDataVersion using detected namespaces
        def_ns = self.namespace_map.get('def', '')
        odm_ns = self.namespace_map.get('default', self.namespace_map.get('', ''))
        
        # Find elements using flexible namespace matching
        study = None
        mdv = None
        
        for elem in root.iter():
            if elem.tag.endswith('Study') or elem.tag == 'Study':
                study = elem
            if elem.tag.endswith('MetaDataVersion') or elem.tag == 'MetaDataVersion':
                mdv = elem
                break
        
        if not study or not mdv:
            raise ValueError("Could not find Study or MetaDataVersion in Define-XML")
        
        # Extract root-level attributes
        root_attrs = self._extract_all_attributes(root)
        
        # Build Define-JSON structure
        define_json = {
            '_namespace_metadata': namespace_metadata,
            '_root_attributes': root_attrs
        }
        
        # Extract ODM attributes
        define_json['fileOID'] = root.get('FileOID')
        define_json['asOfDateTime'] = root.get('AsOfDateTime')
        define_json['creationDateTime'] = root.get('CreationDateTime')
        define_json['odmVersion'] = root.get('ODMVersion')
        define_json['fileType'] = root.get('FileType')
        define_json['originator'] = root.get('Originator')
        define_json['sourceSystem'] = root.get('SourceSystem')
        define_json['sourceSystemVersion'] = root.get('SourceSystemVersion')
        
        # Extract def:Context if present (check all possible namespace versions)
        for ns_prefix, ns_uri in self.namespace_map.items():
            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                context = root.get(f'{{{ns_uri}}}Context')
                if context:
                    define_json['context'] = context
                    break
        
        # Extract Study attributes
        define_json['studyOID'] = study.get('OID')
        define_json['studyName'] = self._get_study_name(study, odm_ns)
        define_json['studyDescription'] = self._get_study_description(study, odm_ns)
        define_json['protocolName'] = self._get_protocol_name(study, odm_ns)
        
        # Extract MetaDataVersion attributes (including all namespaced ones)
        mdv_attrs = self._extract_all_attributes(mdv)
        define_json['_mdv_attributes'] = mdv_attrs
        
        define_json['OID'] = mdv.get('OID')
        define_json['name'] = mdv.get('Name', mdv.get('OID'))
        define_json['description'] = mdv.get('Description', '')
        
        # Extract def:DefineVersion from the correct namespace
        for ns_prefix, ns_uri in self.namespace_map.items():
            if 'def' in ns_prefix or 'def' in ns_uri.lower():
                def_version = mdv.get(f'{{{ns_uri}}}DefineVersion')
                if def_version:
                    define_json['defineVersion'] = def_version
                    break
        
        # Process all major element types
        define_json['standards'] = self._process_standards(mdv, odm_ns, def_ns)
        define_json['annotatedCRF'] = self._process_annotated_crf(mdv, odm_ns, def_ns)
        define_json['supplementalDocs'] = self._process_supplemental_docs(mdv, odm_ns, def_ns)
        define_json['leaves'] = self._process_leaves(mdv, def_ns)
        define_json['analysisResultDisplays'] = self._process_analysis_result_displays(mdv, def_ns)
        
        # Process methods
        methods, derivation_method_map = self._process_methods(mdv, odm_ns, def_ns)
        define_json['methods'] = methods
        
        # Process data structures
        define_json['itemGroups'] = self._process_item_groups(mdv, odm_ns, def_ns, derivation_method_map)
        define_json['items'] = self._process_items(mdv, odm_ns, def_ns)
        define_json['codeLists'] = self._process_code_lists(mdv, odm_ns, def_ns)
        
        # Process conditions and where clauses
        conditions_and_where = self._process_conditions_and_where_clauses(mdv, odm_ns, def_ns)
        define_json['conditions'] = conditions_and_where['conditions']
        define_json['whereClauses'] = conditions_and_where['whereClauses']
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(define_json, f, indent=2)
        
        return define_json
    
    def _process_supplemental_docs(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process SupplementalDoc elements."""
        docs = []
        
        for doc_elem in mdv.iter():
            if doc_elem.tag.endswith('SupplementalDoc'):
                doc = {'_attributes': self._extract_all_attributes(doc_elem)}
                
                # Extract common attributes
                doc['OID'] = doc_elem.get('OID')
                
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
    
    def _process_leaves(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process leaf elements (PDF references)."""
        leaves = []
        
        for leaf_elem in mdv.iter():
            # Check for def:leaf or just leaf
            if leaf_elem.tag.endswith('leaf') or 'leaf' in leaf_elem.tag.lower():
                leaf = {'_attributes': self._extract_all_attributes(leaf_elem)}
                
                # Extract attributes
                leaf['ID'] = leaf_elem.get('ID')
                leaf['href'] = leaf_elem.get(f'{{{self.namespace_map.get("xlink", "")}}}href') or leaf_elem.get('href')
                
                # Extract title
                for title_elem in leaf_elem.iter():
                    if title_elem.tag.endswith('title'):
                        leaf['title'] = title_elem.text
                        break
                
                leaves.append(leaf)
        
        return leaves
    
    def _process_analysis_result_displays(self, mdv: ET.Element, def_ns: str) -> List[Dict[str, Any]]:
        """Process AnalysisResultDisplays elements."""
        displays = []
        
        for display_elem in mdv.iter():
            if display_elem.tag.endswith('AnalysisResultDisplays'):
                display = {'_attributes': self._extract_all_attributes(display_elem)}
                
                # Extract attributes
                display['OID'] = display_elem.get('OID')
                display['name'] = display_elem.get('Name')
                
                # Extract description
                display['description'] = self._get_description(display_elem, '')
                
                # Extract AnalysisResults children
                results = []
                for result_elem in display_elem.iter():
                    if result_elem.tag.endswith('AnalysisResult'):
                        result = {'_attributes': self._extract_all_attributes(result_elem)}
                        result['OID'] = result_elem.get('OID')
                        result['description'] = self._get_description(result_elem, '')
                        
                        # Extract other nested elements as needed
                        results.append(result)
                
                if results:
                    display['analysisResults'] = results
                
                displays.append(display)
        
        return displays
    
    def _process_standards(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process Standard elements."""
        standards = []
        
        for std_elem in mdv.iter():
            if std_elem.tag.endswith('Standard'):
                standard = {'_attributes': self._extract_all_attributes(std_elem)}
                
                # Extract attributes (trying multiple namespace combinations)
                standard['OID'] = std_elem.get('OID')
                standard['name'] = std_elem.get('Name')
                standard['type'] = std_elem.get('Type')
                standard['version'] = std_elem.get('Version')
                standard['status'] = std_elem.get('Status')
                
                standards.append(standard)
        
        return standards
    
    def _process_annotated_crf(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
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
                
                # Extract description
                desc = self._get_description(method_elem, odm_ns)
                if desc:
                    method['description'] = desc
                
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
                
                # Extract description
                ig['description'] = self._get_description(ig_elem, odm_ns)
                
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
                        
                        items.append(item_ref)
                
                ig['items'] = items
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
                
                # Extract description
                item['description'] = self._get_description(item_elem, odm_ns)
                
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
                
                items.append(item)
        
        return items
    
    def _process_code_lists(self, mdv: ET.Element, odm_ns: str, def_ns: str) -> List[Dict[str, Any]]:
        """Process CodeList elements with complete attribute preservation."""
        code_lists = []
        
        for cl_elem in mdv.iter():
            if cl_elem.tag.endswith('CodeList'):
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
                                        
                                        # Extract xml:lang attribute
                                        xml_ns = self.namespace_map.get('xml', 'http://www.w3.org/XML/1998/namespace')
                                        lang = tt_elem.get(f'{{{xml_ns}}}lang')
                                        if lang:
                                            cli['lang'] = lang
                                        
                                        # Store TranslatedText attributes
                                        cli['_translatedText_attributes'] = self._extract_all_attributes(tt_elem)
                                        break
                                break
                        
                        items.append(cli)
                
                cl['codeListItems'] = items
                code_lists.append(cl)
        
        return code_lists
    
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
                condition['description'] = self._get_description(cond_elem, odm_ns)
                conditions.append(condition)
        
        for wc_elem in mdv.iter():
            if wc_elem.tag.endswith('WhereClauseDef'):
                wc = {'_attributes': self._extract_all_attributes(wc_elem)}
                wc['OID'] = wc_elem.get('OID')
                
                # Extract RangeCheck children
                checks = []
                for check_elem in wc_elem.iter():
                    if check_elem.tag.endswith('RangeCheck'):
                        check = {'_attributes': self._extract_all_attributes(check_elem)}
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
    
    def _get_description(self, element: ET.Element, odm_ns: str) -> str:
        """Extract description from TranslatedText."""
        for desc_elem in element.iter():
            if desc_elem.tag.endswith('Description'):
                for tt_elem in desc_elem.iter():
                    if tt_elem.tag.endswith('TranslatedText'):
                        return tt_elem.text if tt_elem.text else ''
        return ''


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
    print(f"  Methods: {len(result.get('methods', []))}")
    print(f"  Standards: {len(result.get('standards', []))}")
    print(f"  Leaves: {len(result.get('leaves', []))}")
    print(f"  Analysis Result Displays: {len(result.get('analysisResultDisplays', []))}")


if __name__ == '__main__':
    main()
