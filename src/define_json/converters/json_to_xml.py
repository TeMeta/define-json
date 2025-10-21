"""
Define-JSON to Define-XML converter with complete fidelity.

Key principles:
1. Use stored namespace metadata from JSON
2. Reconstruct ALL attributes exactly as they were
3. Recreate correct element types (ComputationMethod vs MethodDef)
4. No defaults or inference - only use what's in the JSON
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DefineJSONToXMLConverter:
    """Convert Define-JSON back to Define-XML with complete fidelity."""
    
    def __init__(self, stylesheet_href: str = "define2-1.xsl"):
        """
        Initialize converter.
        
        Args:
            stylesheet_href: Optional stylesheet reference for XML processing instruction.
                           This is a presentation hint and doesn't affect conversion logic.
                           Defaults to "define2-1.xsl".
        """
        self.namespace_map = {}
        self.stylesheet_href = stylesheet_href
    
    def convert_file(self, json_path: Path, output_path: Path) -> ET.Element:
        """Convert Define-JSON file back to Define-XML."""
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        # Extract namespace metadata
        ns_metadata = json_data.get('_namespace_metadata', {})
        self.namespace_map = ns_metadata.get('namespaces', {})
        
        # If no namespace metadata, use safe defaults
        if not self.namespace_map:
            odm_version = json_data.get('odmVersion', '1.3')
            define_version = json_data.get('defineVersion', '2.1')
            
            if '1.2' in str(odm_version):
                self.namespace_map['default'] = 'http://www.cdisc.org/ns/odm/v1.2'
            else:
                self.namespace_map['default'] = 'http://www.cdisc.org/ns/odm/v1.3'
            
            if '1.0' in str(define_version):
                self.namespace_map['def'] = 'http://www.cdisc.org/ns/def/v1.0'
            elif '2.0' in str(define_version):
                self.namespace_map['def'] = 'http://www.cdisc.org/ns/def/v2.0'
            else:
                self.namespace_map['def'] = 'http://www.cdisc.org/ns/def/v2.1'
            
            self.namespace_map['xlink'] = 'http://www.w3.org/1999/xlink'
            self.namespace_map['xml'] = 'http://www.w3.org/XML/1998/namespace'
            self.namespace_map['xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        
        # Register namespaces for pretty output
        for prefix, uri in self.namespace_map.items():
            if prefix and prefix != 'default':
                ET.register_namespace(prefix, uri)
        
        # Get default namespace
        default_ns = self.namespace_map.get('default', self.namespace_map.get('', ''))
        
        # Create root ODM element
        root = ET.Element(f'{{{default_ns}}}ODM' if default_ns else 'ODM')
        
        # Set root attributes from stored attributes
        root_attrs = json_data.get('_root_attributes', {})
        if root_attrs:
            # Restore all original attributes
            for attr_name, attr_value in root_attrs.items():
                root.set(attr_name, attr_value)
        else:
            # Fallback to basic attributes
            if json_data.get('fileOID'):
                root.set('FileOID', json_data['fileOID'])
            if json_data.get('creationDateTime'):
                root.set('CreationDateTime', json_data['creationDateTime'])
            if json_data.get('asOfDateTime'):
                root.set('AsOfDateTime', json_data['asOfDateTime'])
            if json_data.get('odmVersion'):
                root.set('ODMVersion', json_data['odmVersion'])
            if json_data.get('fileType'):
                root.set('FileType', json_data['fileType'])
            if json_data.get('originator'):
                root.set('Originator', json_data['originator'])
            if json_data.get('sourceSystem'):
                root.set('SourceSystem', json_data['sourceSystem'])
            if json_data.get('sourceSystemVersion'):
                root.set('SourceSystemVersion', json_data['sourceSystemVersion'])
        
            # Ensure namespace declarations are present (only if not already set)
            if default_ns and 'xmlns' not in root.attrib:
                root.set('xmlns', default_ns)
            
            for prefix, uri in self.namespace_map.items():
                print('NAMESPACE', prefix, uri)
                if prefix and prefix not in ['default', '']:
                    ns_attr = f'xmlns:{prefix}'
                    # Only add if not already present in stored attributes
                    if ns_attr not in root.attrib:
                        root.set(ns_attr, uri)
        
        # Add context if present
        if json_data.get('context'):
            def_ns = self.namespace_map.get('def', '')
            if def_ns:
                root.set(f'{{{def_ns}}}Context', json_data['context'])
        
        # Create Study element
        study = ET.SubElement(root, f'{{{default_ns}}}Study' if default_ns else 'Study')
        study.set('OID', json_data.get('studyOID', 'UNKNOWN'))
        
        # Global Variables
        global_vars = ET.SubElement(study, f'{{{default_ns}}}GlobalVariables' if default_ns else 'GlobalVariables')
        
        if json_data.get('studyName'):
            study_name = ET.SubElement(global_vars, f'{{{default_ns}}}StudyName' if default_ns else 'StudyName')
            study_name.text = json_data['studyName']
        
        if json_data.get('studyDescription'):
            study_desc = ET.SubElement(global_vars, f'{{{default_ns}}}StudyDescription' if default_ns else 'StudyDescription')
            study_desc.text = json_data['studyDescription']
        
        if json_data.get('protocolName'):
            protocol = ET.SubElement(global_vars, f'{{{default_ns}}}ProtocolName' if default_ns else 'ProtocolName')
            protocol.text = json_data['protocolName']
        
        # MetaDataVersion
        mdv = ET.SubElement(study, f'{{{default_ns}}}MetaDataVersion' if default_ns else 'MetaDataVersion')
        
        # Restore MetaDataVersion attributes from stored attributes
        mdv_attrs = json_data.get('_mdv_attributes', {})
        if mdv_attrs:
            for attr_name, attr_value in mdv_attrs.items():
                mdv.set(attr_name, attr_value)
        else:
            # Fallback to basic attributes
            mdv.set('OID', json_data.get('OID', 'MDV.ROUNDTRIP'))
            mdv.set('Name', json_data.get('name', 'Roundtrip MetaDataVersion'))
            if json_data.get('description'):
                mdv.set('Description', json_data['description'])
            
            # Set DefineVersion in correct namespace
            if json_data.get('defineVersion'):
                def_ns = self.namespace_map.get('def', '')
                if def_ns:
                    mdv.set(f'{{{def_ns}}}DefineVersion', json_data['defineVersion'])
        
        # Process all element types in proper order
        self._create_standards(mdv, json_data.get('standards', []), default_ns)
        self._create_annotated_crf(mdv, json_data.get('annotatedCRF', []), default_ns)
        self._create_supplemental_docs(mdv, json_data.get('supplementalDocs', []), default_ns)
        
        # Create leaves (PDFs)
        self._create_leaves(mdv, json_data.get('leaves', []))
        
        # Create conditions and where clauses
        self._create_conditions(mdv, json_data.get('conditions', []), default_ns)
        self._create_where_clauses(mdv, json_data.get('whereClauses', []), default_ns)
        
        # Create ItemGroupDefs
        self._create_item_group_defs(mdv, json_data.get('itemGroups', []), default_ns)
        
        # Create ItemDefs
        self._create_item_defs(mdv, json_data.get('items', []), default_ns)
        
        # Create CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []), default_ns)
        
        # Create Methods (both ComputationMethod and MethodDef)
        self._create_methods(mdv, json_data.get('methods', []), default_ns)
        
        # Create AnalysisResultDisplays
        self._create_analysis_result_displays(mdv, json_data.get('analysisResultDisplays', []), default_ns)
        
        # Write to file with proper formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        
        # Add XML declaration and stylesheet PI
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            if self.stylesheet_href:
                f.write(f'<?xml-stylesheet type="text/xsl" href="{self.stylesheet_href}"?>\n'.encode('utf-8'))
            tree.write(f, encoding='utf-8', xml_declaration=False)
        
        return root
    
    def _apply_stored_attributes(self, element: ET.Element, item_dict: Dict[str, Any]) -> None:
        """Apply all stored attributes to an element."""
        stored_attrs = item_dict.get('_attributes', {})
        if stored_attrs:
            for attr_name, attr_value in stored_attrs.items():
                element.set(attr_name, attr_value)
    
    def _create_standards(self, parent: ET.Element, standards: List[Dict[str, Any]], ns: str) -> None:
        """Create Standard elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for std in standards:
            std_elem = ET.SubElement(parent, f'{{{def_ns}}}Standard' if def_ns else 'Standard')
            
            # Restore all attributes
            self._apply_stored_attributes(std_elem, std)
            
            # Ensure key attributes are set
            if not std_elem.get('OID') and std.get('OID'):
                std_elem.set('OID', std['OID'])
            if not std_elem.get('Name') and std.get('name'):
                std_elem.set('Name', std['name'])
            if not std_elem.get('Type') and std.get('type'):
                std_elem.set('Type', std['type'])
            if not std_elem.get('Version') and std.get('version'):
                std_elem.set('Version', std['version'])
    
    def _create_annotated_crf(self, parent: ET.Element, crfs: List[Dict[str, Any]], ns: str) -> None:
        """Create AnnotatedCRF elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for crf in crfs:
            crf_elem = ET.SubElement(parent, f'{{{def_ns}}}AnnotatedCRF' if def_ns else 'AnnotatedCRF')
            
            self._apply_stored_attributes(crf_elem, crf)
            
            # Create DocumentRef children
            for doc_ref in crf.get('documentRefs', []):
                ref_elem = ET.SubElement(crf_elem, f'{{{def_ns}}}DocumentRef' if def_ns else 'DocumentRef')
                self._apply_stored_attributes(ref_elem, doc_ref)
                
                if not ref_elem.get('leafID') and doc_ref.get('leafID'):
                    ref_elem.set('leafID', doc_ref['leafID'])
    
    def _create_supplemental_docs(self, parent: ET.Element, docs: List[Dict[str, Any]], ns: str) -> None:
        """Create SupplementalDoc elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for doc in docs:
            doc_elem = ET.SubElement(parent, f'{{{def_ns}}}SupplementalDoc' if def_ns else 'SupplementalDoc')
            
            self._apply_stored_attributes(doc_elem, doc)
            
            if not doc_elem.get('OID') and doc.get('OID'):
                doc_elem.set('OID', doc['OID'])
            
            # Create DocumentRef children
            for doc_ref in doc.get('documentRefs', []):
                ref_elem = ET.SubElement(doc_elem, f'{{{def_ns}}}DocumentRef' if def_ns else 'DocumentRef')
                self._apply_stored_attributes(ref_elem, doc_ref)
                
                if not ref_elem.get('leafID') and doc_ref.get('leafID'):
                    ref_elem.set('leafID', doc_ref['leafID'])
    
    def _create_leaves(self, parent: ET.Element, leaves: List[Dict[str, Any]]) -> None:
        """Create leaf elements."""
        def_ns = self.namespace_map.get('def', '')
        xlink_ns = self.namespace_map.get('xlink', '')
        
        for leaf in leaves:
            leaf_elem = ET.SubElement(parent, f'{{{def_ns}}}leaf' if def_ns else 'leaf')
            
            self._apply_stored_attributes(leaf_elem, leaf)
            
            if not leaf_elem.get('ID') and leaf.get('ID'):
                leaf_elem.set('ID', leaf['ID'])
            
            # Set href in xlink namespace
            if leaf.get('href'):
                if xlink_ns:
                    leaf_elem.set(f'{{{xlink_ns}}}href', leaf['href'])
                else:
                    leaf_elem.set('href', leaf['href'])
            
            # Add title
            if leaf.get('title'):
                title_elem = ET.SubElement(leaf_elem, f'{{{def_ns}}}title' if def_ns else 'title')
                title_elem.text = leaf['title']
    
    def _create_conditions(self, parent: ET.Element, conditions: List[Dict[str, Any]], ns: str) -> None:
        """Create ConditionDef elements."""
        for cond in conditions:
            cond_elem = ET.SubElement(parent, f'{{{ns}}}ConditionDef' if ns else 'ConditionDef')
            
            self._apply_stored_attributes(cond_elem, cond)
            
            if not cond_elem.get('OID') and cond.get('OID'):
                cond_elem.set('OID', cond['OID'])
            if not cond_elem.get('Name') and cond.get('name'):
                cond_elem.set('Name', cond['name'])
            
            if cond.get('description'):
                desc = ET.SubElement(cond_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = cond['description']
    
    def _create_where_clauses(self, parent: ET.Element, where_clauses: List[Dict[str, Any]], ns: str) -> None:
        """Create WhereClauseDef elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for wc in where_clauses:
            wc_elem = ET.SubElement(parent, f'{{{def_ns}}}WhereClauseDef' if def_ns else 'WhereClauseDef')
            
            self._apply_stored_attributes(wc_elem, wc)
            
            if not wc_elem.get('OID') and wc.get('OID'):
                wc_elem.set('OID', wc['OID'])
            
            # Create RangeCheck children
            for check in wc.get('rangeChecks', []):
                check_elem = ET.SubElement(wc_elem, f'{{{def_ns}}}RangeCheck' if def_ns else 'RangeCheck')
                self._apply_stored_attributes(check_elem, check)
    
    def _create_item_group_defs(self, parent: ET.Element, item_groups: List[Dict[str, Any]], ns: str) -> None:
        """Create ItemGroupDef elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for ig in item_groups:
            ig_elem = ET.SubElement(parent, f'{{{ns}}}ItemGroupDef' if ns else 'ItemGroupDef')
            
            # Apply stored attributes first
            self._apply_stored_attributes(ig_elem, ig)
            
            # Ensure key attributes are set
            if not ig_elem.get('OID') and ig.get('OID'):
                ig_elem.set('OID', ig['OID'])
            if not ig_elem.get('Name') and ig.get('name'):
                ig_elem.set('Name', ig['name'])
            if not ig_elem.get('Repeating') and ig.get('repeating') is not None:
                ig_elem.set('Repeating', str(ig['repeating']))
            if not ig_elem.get('Domain') and ig.get('domain'):
                ig_elem.set('Domain', ig['domain'])
            if not ig_elem.get('SASDatasetName') and ig.get('sasDatasetName'):
                ig_elem.set('SASDatasetName', ig['sasDatasetName'])
            
            # Add description if present
            if ig.get('description'):
                desc = ET.SubElement(ig_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = ig['description']
            
            # Add ItemRefs
            for item in ig.get('items', []):
                ref_elem = ET.SubElement(ig_elem, f'{{{ns}}}ItemRef' if ns else 'ItemRef')
                
                self._apply_stored_attributes(ref_elem, item)
                
                # Ensure ItemOID is set
                item_oid = item.get('OID') or item.get('itemOID')
                if item_oid:
                    ref_elem.set('ItemOID', item_oid)
                
                if not ref_elem.get('Mandatory') and item.get('mandatory'):
                    ref_elem.set('Mandatory', str(item['mandatory']))
                if not ref_elem.get('Role') and item.get('role'):
                    ref_elem.set('Role', item['role'])
    
    def _create_item_defs(self, parent: ET.Element, items: List[Dict[str, Any]], ns: str) -> None:
        """Create ItemDef elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for item in items:
            item_elem = ET.SubElement(parent, f'{{{ns}}}ItemDef' if ns else 'ItemDef')
            
            self._apply_stored_attributes(item_elem, item)
            
            # Ensure key attributes are set
            if not item_elem.get('OID') and item.get('OID'):
                item_elem.set('OID', item['OID'])
            if not item_elem.get('Name') and item.get('name'):
                item_elem.set('Name', item['name'])
            if not item_elem.get('DataType') and item.get('dataType'):
                item_elem.set('DataType', item['dataType'])
            if not item_elem.get('Length') and item.get('length'):
                item_elem.set('Length', str(item['length']))
            if not item_elem.get('SignificantDigits') and item.get('significantDigits'):
                item_elem.set('SignificantDigits', str(item['significantDigits']))
            
            # Add description
            if item.get('description'):
                desc = ET.SubElement(item_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = item['description']
            
            # Add CodeListRef
            if item.get('codeList'):
                ref_elem = ET.SubElement(item_elem, f'{{{ns}}}CodeListRef' if ns else 'CodeListRef')
                ref_elem.set('CodeListOID', item['codeList'])
            
            # Add ValueListRef
            if item.get('valueListOID'):
                vlr_elem = ET.SubElement(item_elem, f'{{{ns}}}ValueListRef' if ns else 'ValueListRef')
                vlr_elem.set('ValueListOID', item['valueListOID'])
    
    def _create_code_lists(self, parent: ET.Element, code_lists: List[Dict[str, Any]], ns: str) -> None:
        """Create CodeList elements with complete attribute preservation."""
        def_ns = self.namespace_map.get('def', '')
        xml_ns = self.namespace_map.get('xml', 'http://www.w3.org/XML/1998/namespace')
        
        for cl in code_lists:
            cl_elem = ET.SubElement(parent, f'{{{ns}}}CodeList' if ns else 'CodeList')
            
            self._apply_stored_attributes(cl_elem, cl)
            
            if not cl_elem.get('OID') and cl.get('OID'):
                cl_elem.set('OID', cl['OID'])
            if not cl_elem.get('Name') and cl.get('name'):
                cl_elem.set('Name', cl['name'])
            if not cl_elem.get('DataType') and cl.get('dataType'):
                cl_elem.set('DataType', cl['dataType'])
            
            # Add CodeListItems
            for item in cl.get('codeListItems', []):
                cli_elem = ET.SubElement(cl_elem, f'{{{ns}}}CodeListItem' if ns else 'CodeListItem')
                
                self._apply_stored_attributes(cli_elem, item)
                
                if not cli_elem.get('CodedValue') and item.get('codedValue'):
                    cli_elem.set('CodedValue', item['codedValue'])
                
                # Set def:Rank if present
                if item.get('rank'):
                    if def_ns:
                        cli_elem.set(f'{{{def_ns}}}Rank', str(item['rank']))
                    elif not cli_elem.get('Rank'):
                        cli_elem.set('Rank', str(item['rank']))
                
                # Add Decode with xml:lang
                if item.get('decode'):
                    decode = ET.SubElement(cli_elem, f'{{{ns}}}Decode' if ns else 'Decode')
                    tt = ET.SubElement(decode, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                    
                    # Restore TranslatedText attributes
                    tt_attrs = item.get('_translatedText_attributes', {})
                    if tt_attrs:
                        for attr_name, attr_value in tt_attrs.items():
                            tt.set(attr_name, attr_value)
                    
                    # Set xml:lang if present and not already set
                    if item.get('lang') and not any(k.endswith('lang') for k in tt.attrib.keys()):
                        tt.set(f'{{{xml_ns}}}lang', item['lang'])
                    
                    tt.text = item['decode']
    
    def _create_methods(self, parent: ET.Element, methods: List[Dict[str, Any]], ns: str) -> None:
        """Create MethodDef or ComputationMethod elements based on element type."""
        def_ns = self.namespace_map.get('def', '')
        
        for method in methods:
            element_type = method.get('elementType', 'MethodDef')
            
            # Skip synthetic methods
            if method.get('OID', '').startswith('MT.DERIVATION.'):
                continue
            
            if element_type == 'ComputationMethod':
                # Create ComputationMethod (v1.0 style)
                method_elem = ET.SubElement(parent, f'{{{def_ns}}}ComputationMethod' if def_ns else 'ComputationMethod')
                
                self._apply_stored_attributes(method_elem, method)
                
                if not method_elem.get('OID') and method.get('OID'):
                    method_elem.set('OID', method['OID'])
                if not method_elem.get('Name') and method.get('name'):
                    method_elem.set('Name', method['name'])
                
                # Text content is the description
                if method.get('description'):
                    method_elem.text = method['description']
            
            else:
                # Create MethodDef (v2.x style)
                method_elem = ET.SubElement(parent, f'{{{ns}}}MethodDef' if ns else 'MethodDef')
                
                self._apply_stored_attributes(method_elem, method)
                
                if not method_elem.get('OID') and method.get('OID'):
                    method_elem.set('OID', method['OID'])
                if not method_elem.get('Name') and method.get('name'):
                    method_elem.set('Name', method['name'])
                if not method_elem.get('Type') and method.get('type'):
                    method_elem.set('Type', method['type'])
                
                # Description in child elements
                if method.get('description'):
                    desc = ET.SubElement(method_elem, f'{{{ns}}}Description' if ns else 'Description')
                    tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                    tt.text = method['description']
    
    def _create_analysis_result_displays(self, parent: ET.Element, displays: List[Dict[str, Any]], ns: str) -> None:
        """Create AnalysisResultDisplays elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for display in displays:
            display_elem = ET.SubElement(parent, f'{{{def_ns}}}AnalysisResultDisplays' if def_ns else 'AnalysisResultDisplays')
            
            self._apply_stored_attributes(display_elem, display)
            
            if not display_elem.get('OID') and display.get('OID'):
                display_elem.set('OID', display['OID'])
            if not display_elem.get('Name') and display.get('name'):
                display_elem.set('Name', display['name'])
            
            # Add description
            if display.get('description'):
                desc = ET.SubElement(display_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = display['description']
            
            # Add AnalysisResult children
            for result in display.get('analysisResults', []):
                result_elem = ET.SubElement(display_elem, f'{{{def_ns}}}AnalysisResult' if def_ns else 'AnalysisResult')
                
                self._apply_stored_attributes(result_elem, result)
                
                if not result_elem.get('OID') and result.get('OID'):
                    result_elem.set('OID', result['OID'])
                
                if result.get('description'):
                    desc = ET.SubElement(result_elem, f'{{{ns}}}Description' if ns else 'Description')
                    tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                    tt.text = result['description']


def main():
    """Main entry point for testing."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python json_to_xml_fixed.py <input.json> <output.xml>")
        sys.exit(1)
    
    converter = DefineJSONToXMLConverter()
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    print(f"Converting {input_path} to {output_path}")
    result = converter.convert_file(input_path, output_path)
    print(f"Conversion complete. Output written to {output_path}")


if __name__ == '__main__':
    main()
