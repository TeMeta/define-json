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
    
    def _apply_stored_attributes(self, element: ET.Element, data: Dict[str, Any]) -> None:
        """Apply stored attributes to an element."""
        if '_attributes' in data:
            for attr_name, attr_value in data['_attributes'].items():
                element.set(attr_name, attr_value)
    
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
        self._create_standards(mdv, json_data.get('standards', []), default_ns, 
                             json_data.get('has_standards_container', False))
        self._create_annotated_crf(mdv, json_data.get('annotatedCRF', []), default_ns)
        self._create_supplemental_docs(mdv, json_data.get('supplementalDocs', []), default_ns)
        self._create_value_list_defs(mdv, json_data.get('valueLists', []), default_ns)
        self._create_where_clauses(mdv, json_data.get('whereClauses', []), default_ns)
        self._create_item_group_defs(mdv, json_data.get('itemGroups', []), default_ns)
        self._create_item_defs(mdv, json_data.get('items', []), default_ns)
        self._create_code_lists(mdv, json_data.get('codeLists', []), default_ns)
        self._create_methods(mdv, json_data.get('methods', []), default_ns)
        self._create_condition_defs(mdv, json_data.get('conditions', []), default_ns)
        self._create_leaves(mdv, json_data.get('leaves', []), default_ns)
        self._create_analysis_result_displays(mdv, json_data.get('analysisResultDisplays', []), default_ns)
        
        # Write to file with pretty formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        
        # Add XML declaration and stylesheet
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            if self.stylesheet_href:
                f.write(f'<?xml-stylesheet type="text/xsl" href="{self.stylesheet_href}"?>\n'.encode())
            tree.write(f, encoding='utf-8', xml_declaration=False)
        
        return root
    
    def _create_standards(self, parent: ET.Element, standards: List[Dict[str, Any]], ns: str, has_container: bool) -> None:
        """Create Standard elements, with optional Standards container."""
        def_ns = self.namespace_map.get('def', '')
        
        if has_container:
            # Create Standards container
            standards_elem = ET.SubElement(parent, f'{{{def_ns}}}Standards' if def_ns else 'Standards')
            for std in standards:
                std_elem = ET.SubElement(standards_elem, f'{{{def_ns}}}Standard' if def_ns else 'Standard')
                self._apply_stored_attributes(std_elem, std)
                
                if not std_elem.get('OID') and std.get('OID'):
                    std_elem.set('OID', std['OID'])
                if not std_elem.get('Name') and std.get('name'):
                    std_elem.set('Name', std['name'])
                if not std_elem.get('Type') and std.get('type'):
                    std_elem.set('Type', std['type'])
                if not std_elem.get('PublishingSet') and std.get('publishingSet'):
                    std_elem.set('PublishingSet', std['publishingSet'])
                if not std_elem.get('Version') and std.get('version'):
                    std_elem.set('Version', std['version'])
                if not std_elem.get('Status') and std.get('status'):
                    std_elem.set('Status', std['status'])
        else:
            # Create Standard elements directly
            for std in standards:
                std_elem = ET.SubElement(parent, f'{{{def_ns}}}Standard' if def_ns else 'Standard')
                self._apply_stored_attributes(std_elem, std)
                
                if not std_elem.get('OID') and std.get('OID'):
                    std_elem.set('OID', std['OID'])
                if not std_elem.get('Name') and std.get('name'):
                    std_elem.set('Name', std['name'])
                if not std_elem.get('Type') and std.get('type'):
                    std_elem.set('Type', std['type'])
                if not std_elem.get('PublishingSet') and std.get('publishingSet'):
                    std_elem.set('PublishingSet', std['publishingSet'])
                if not std_elem.get('Version') and std.get('version'):
                    std_elem.set('Version', std['version'])
                if not std_elem.get('Status') and std.get('status'):
                    std_elem.set('Status', std['status'])
    
    def _create_annotated_crf(self, parent: ET.Element, crfs: List[Dict[str, Any]], ns: str) -> None:
        """Create AnnotatedCRF elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for crf in crfs:
            crf_elem = ET.SubElement(parent, f'{{{def_ns}}}AnnotatedCRF' if def_ns else 'AnnotatedCRF')
            
            self._apply_stored_attributes(crf_elem, crf)
            
            # Add DocumentRef children
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
            
            # Add DocumentRef children
            for doc_ref in doc.get('documentRefs', []):
                ref_elem = ET.SubElement(doc_elem, f'{{{def_ns}}}DocumentRef' if def_ns else 'DocumentRef')
                
                self._apply_stored_attributes(ref_elem, doc_ref)
                
                if not ref_elem.get('leafID') and doc_ref.get('leafID'):
                    ref_elem.set('leafID', doc_ref['leafID'])
    
    def _create_leaves(self, parent: ET.Element, leaves: List[Dict[str, Any]], ns: str) -> None:
        """Create global leaf elements (direct children of MetaDataVersion)."""
        def_ns = self.namespace_map.get('def', '')
        xlink_ns = self.namespace_map.get('xlink', '')
        
        for leaf in leaves:
            leaf_elem = ET.SubElement(parent, f'{{{def_ns}}}leaf' if def_ns else 'leaf')
            
            self._apply_stored_attributes(leaf_elem, leaf)
            
            if not leaf_elem.get('ID') and leaf.get('ID'):
                leaf_elem.set('ID', leaf['ID'])
            
            # Set href
            if leaf.get('href'):
                if xlink_ns:
                    leaf_elem.set(f'{{{xlink_ns}}}href', leaf['href'])
                else:
                    leaf_elem.set('href', leaf['href'])
            
            # Add title
            if leaf.get('title'):
                title_elem = ET.SubElement(leaf_elem, f'{{{def_ns}}}title' if def_ns else 'title')
                title_elem.text = leaf['title']
    
    def _create_condition_defs(self, parent: ET.Element, conditions: List[Dict[str, Any]], ns: str) -> None:
        """Create ConditionDef elements."""
        for condition in conditions:
            cond_elem = ET.SubElement(parent, f'{{{ns}}}ConditionDef' if ns else 'ConditionDef')
            
            self._apply_stored_attributes(cond_elem, condition)
            
            if not cond_elem.get('OID') and condition.get('OID'):
                cond_elem.set('OID', condition['OID'])
            if not cond_elem.get('Name') and condition.get('name'):
                cond_elem.set('Name', condition['name'])
            
            # Add description
            if condition.get('description'):
                desc = ET.SubElement(cond_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = condition['description']
                
                # Restore TranslatedText attributes (xml:lang, etc.)
                if condition.get('_translatedText_attributes'):
                    for attr_name, attr_value in condition['_translatedText_attributes'].items():
                        tt.set(attr_name, attr_value)
    
    def _create_where_clauses(self, parent: ET.Element, where_clauses: List[Dict[str, Any]], ns: str) -> None:
        """Create WhereClauseDef elements with CheckValue children."""
        for wc in where_clauses:
            wc_elem = ET.SubElement(parent, f'{{{ns}}}WhereClauseDef' if ns else 'WhereClauseDef')
            
            self._apply_stored_attributes(wc_elem, wc)
            
            if not wc_elem.get('OID') and wc.get('OID'):
                wc_elem.set('OID', wc['OID'])
            
            # Add RangeCheck children with CheckValue elements 
            for check in wc.get('rangeChecks', []):
                check_elem = ET.SubElement(wc_elem, f'{{{ns}}}RangeCheck' if ns else 'RangeCheck')
                self._apply_stored_attributes(check_elem, check)
                
                # Add CheckValue child elements 
                for check_value in check.get('checkValues', []):
                    cv_elem = ET.SubElement(check_elem, f'{{{ns}}}CheckValue' if ns else 'CheckValue')
                    self._apply_stored_attributes(cv_elem, check_value)
                    if check_value.get('text'):
                        cv_elem.text = check_value['text']
    
    def _create_item_group_defs(self, parent: ET.Element, item_groups: List[Dict[str, Any]], ns: str) -> None:
        """Create ItemGroupDef elements."""
        def_ns = self.namespace_map.get('def', '')
        xlink_ns = self.namespace_map.get('xlink', '')
        
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
                
                # Restore TranslatedText attributes (xml:lang, etc.)
                if ig.get('_translatedText_attributes'):
                    for attr_name, attr_value in ig['_translatedText_attributes'].items():
                        tt.set(attr_name, attr_value)
            
            # Add Class child elements 
            if ig.get('classElements'):
                for class_elem_data in ig['classElements']:
                    class_elem = ET.SubElement(ig_elem, f'{{{def_ns}}}Class' if def_ns else 'Class')
                    self._apply_stored_attributes(class_elem, class_elem_data)
                    if not class_elem.get('Name') and class_elem_data.get('name'):
                        class_elem.set('Name', class_elem_data['name'])
            
            # Add nested leaf elements 
            if ig.get('leaves'):
                for leaf in ig['leaves']:
                    leaf_elem = ET.SubElement(ig_elem, f'{{{def_ns}}}leaf' if def_ns else 'leaf')
                    
                    self._apply_stored_attributes(leaf_elem, leaf)
                    
                    if not leaf_elem.get('ID') and leaf.get('ID'):
                        leaf_elem.set('ID', leaf['ID'])
                    
                    # Set href
                    if leaf.get('href'):
                        if xlink_ns:
                            leaf_elem.set(f'{{{xlink_ns}}}href', leaf['href'])
                        else:
                            leaf_elem.set('href', leaf['href'])
                    
                    # Add title
                    if leaf.get('title'):
                        title_elem = ET.SubElement(leaf_elem, f'{{{def_ns}}}title' if def_ns else 'title')
                        title_elem.text = leaf['title']
            
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
                
                # Add WhereClauseRef 
                if item.get('whereClauseRef'):
                    wc_ref = item['whereClauseRef']
                    wc_ref_elem = ET.SubElement(ref_elem, f'{{{ns}}}WhereClauseRef' if ns else 'WhereClauseRef')
                    
                    self._apply_stored_attributes(wc_ref_elem, wc_ref)
                    
                    if not wc_ref_elem.get('WhereClauseOID') and wc_ref.get('whereClauseOID'):
                        wc_ref_elem.set('WhereClauseOID', wc_ref['whereClauseOID'])
    
    def _create_item_defs(self, parent: ET.Element, items: List[Dict[str, Any]], ns: str) -> None:
        """Create ItemDef elements."""
        def_ns = self.namespace_map.get('def', '')
        
        for item in items:
            item_elem = ET.SubElement(parent, f'{{{ns}}}ItemDef' if ns else 'ItemDef')
            
            # Apply stored attributes first
            self._apply_stored_attributes(item_elem, item)
            
            # Ensure key attributes are set (only if not already set by stored attributes)
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
                
                # Restore TranslatedText attributes (xml:lang, etc.)
                if item.get('_translatedText_attributes'):
                    for attr_name, attr_value in item['_translatedText_attributes'].items():
                        tt.set(attr_name, attr_value)
            
            # Add CodeListRef
            if item.get('codeList'):
                ref_elem = ET.SubElement(item_elem, f'{{{ns}}}CodeListRef' if ns else 'CodeListRef')
                ref_elem.set('CodeListOID', item['codeList'])
            
            # Add ValueListRef
            if item.get('valueListOID'):
                vlr_elem = ET.SubElement(item_elem, f'{{{ns}}}ValueListRef' if ns else 'ValueListRef')
                vlr_elem.set('ValueListOID', item['valueListOID'])
            
            # Add Alias elements 
            for alias in item.get('aliases', []):
                alias_elem = ET.SubElement(item_elem, f'{{{ns}}}Alias' if ns else 'Alias')
                
                self._apply_stored_attributes(alias_elem, alias)
                
                if not alias_elem.get('Context') and alias.get('context'):
                    alias_elem.set('Context', alias['context'])
                if not alias_elem.get('Name') and alias.get('name'):
                    alias_elem.set('Name', alias['name'])
            
            # Add Origin elements
            if item.get('origins'):
                def_ns = self.namespace_map.get('def', '')
                for origin in item['origins']:
                    origin_elem = ET.SubElement(
                        item_elem, 
                        f'{{{def_ns}}}Origin' if def_ns else 'Origin'
                    )
                    
                    # Restore Origin attributes
                    self._apply_stored_attributes(origin_elem, origin)
                    
                    if not origin_elem.get('Type') and origin.get('type'):
                        origin_elem.set('Type', origin['type'])
                    
                    # Add Description if present
                    if origin.get('description'):
                        desc = ET.SubElement(origin_elem, f'{{{ns}}}Description' if ns else 'Description')
                        tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                        tt.text = origin['description']
                        
                        # Restore TranslatedText attributes
                        if origin.get('_translatedText_attributes'):
                            for attr_name, attr_value in origin['_translatedText_attributes'].items():
                                tt.set(attr_name, attr_value)
                    
                    # Add DocumentRef if present
                    if origin.get('documentRef'):
                        doc_ref = origin['documentRef']
                        doc_ref_elem = ET.SubElement(origin_elem, f'{{{ns}}}DocumentRef' if ns else 'DocumentRef')
                        
                        self._apply_stored_attributes(doc_ref_elem, doc_ref)
                        
                        if not doc_ref_elem.get('leafID') and doc_ref.get('leafID'):
                            doc_ref_elem.set('leafID', doc_ref['leafID'])
    
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
                    if item.get('lang'):
                        lang_attr = f'{{{xml_ns}}}lang'
                        if lang_attr not in tt.attrib:
                            tt.set(lang_attr, item['lang'])
                    
                    tt.text = item['decode']
                
                # Add Alias elements 
                for alias in item.get('aliases', []):
                    alias_elem = ET.SubElement(cli_elem, f'{{{ns}}}Alias' if ns else 'Alias')
                    
                    self._apply_stored_attributes(alias_elem, alias)
                    
                    if not alias_elem.get('Context') and alias.get('context'):
                        alias_elem.set('Context', alias['context'])
                    if not alias_elem.get('Name') and alias.get('name'):
                        alias_elem.set('Name', alias['name'])
            
            # Add EnumeratedItem elements 
            for ei in cl.get('enumeratedItems', []):
                ei_elem = ET.SubElement(cl_elem, f'{{{ns}}}EnumeratedItem' if ns else 'EnumeratedItem')
                
                self._apply_stored_attributes(ei_elem, ei)
                
                if not ei_elem.get('CodedValue') and ei.get('codedValue'):
                    ei_elem.set('CodedValue', ei['codedValue'])
                
                # Set def:Rank if present
                if ei.get('rank'):
                    if def_ns:
                        ei_elem.set(f'{{{def_ns}}}Rank', str(ei['rank']))
                    elif not ei_elem.get('Rank'):
                        ei_elem.set('Rank', str(ei['rank']))
                
                # Add Alias elements
                for alias in ei.get('aliases', []):
                    alias_elem = ET.SubElement(ei_elem, f'{{{ns}}}Alias' if ns else 'Alias')
                    
                    self._apply_stored_attributes(alias_elem, alias)
                    
                    if not alias_elem.get('Context') and alias.get('context'):
                        alias_elem.set('Context', alias['context'])
                    if not alias_elem.get('Name') and alias.get('name'):
                        alias_elem.set('Name', alias['name'])
            
            # Add ExternalCodeList if present 
            if cl.get('externalCodeList'):
                ext_cl = cl['externalCodeList']
                ext_elem = ET.SubElement(cl_elem, f'{{{ns}}}ExternalCodeList' if ns else 'ExternalCodeList')
                
                self._apply_stored_attributes(ext_elem, ext_cl)
                
                if not ext_elem.get('Dictionary') and ext_cl.get('dictionary'):
                    ext_elem.set('Dictionary', ext_cl['dictionary'])
                if not ext_elem.get('Version') and ext_cl.get('version'):
                    ext_elem.set('Version', ext_cl['version'])
                if not ext_elem.get('ref') and ext_cl.get('ref'):
                    ext_elem.set('ref', ext_cl['ref'])
            
            # Add Alias elements at CodeList level 
            for alias in cl.get('aliases', []):
                alias_elem = ET.SubElement(cl_elem, f'{{{ns}}}Alias' if ns else 'Alias')
                
                self._apply_stored_attributes(alias_elem, alias)
                
                if not alias_elem.get('Context') and alias.get('context'):
                    alias_elem.set('Context', alias['context'])
                if not alias_elem.get('Name') and alias.get('name'):
                    alias_elem.set('Name', alias['name'])
    
    def _create_value_list_defs(self, parent: ET.Element, value_lists: List[Dict[str, Any]], ns: str) -> None:
        """Create ValueListDef elements ."""
        def_ns = self.namespace_map.get('def', '')
        
        for vl in value_lists:
            vl_elem = ET.SubElement(parent, f'{{{ns}}}ValueListDef' if ns else 'ValueListDef')
            
            self._apply_stored_attributes(vl_elem, vl)
            
            if not vl_elem.get('OID') and vl.get('OID'):
                vl_elem.set('OID', vl['OID'])
            
            # Add description if present
            if vl.get('description'):
                desc = ET.SubElement(vl_elem, f'{{{ns}}}Description' if ns else 'Description')
                tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                tt.text = vl['description']
                
                # Restore TranslatedText attributes (xml:lang, etc.)
                if vl.get('_translatedText_attributes'):
                    for attr_name, attr_value in vl['_translatedText_attributes'].items():
                        tt.set(attr_name, attr_value)
            
            # Add ItemRefs
            for item_ref in vl.get('itemRefs', []):
                ref_elem = ET.SubElement(vl_elem, f'{{{ns}}}ItemRef' if ns else 'ItemRef')
                
                self._apply_stored_attributes(ref_elem, item_ref)
                
                if not ref_elem.get('ItemOID') and item_ref.get('OID'):
                    ref_elem.set('ItemOID', item_ref['OID'])
                
                if not ref_elem.get('Mandatory') and item_ref.get('mandatory'):
                    ref_elem.set('Mandatory', str(item_ref['mandatory']))
                
                # Add method reference
                if item_ref.get('method'):
                    if def_ns:
                        ref_elem.set(f'{{{def_ns}}}MethodOID', item_ref['method'])
                
                # Add WhereClauseRef 
                if item_ref.get('whereClauseRef'):
                    wc_ref = item_ref['whereClauseRef']
                    wc_ref_elem = ET.SubElement(ref_elem, f'{{{ns}}}WhereClauseRef' if ns else 'WhereClauseRef')
                    
                    self._apply_stored_attributes(wc_ref_elem, wc_ref)
                    
                    if not wc_ref_elem.get('WhereClauseOID') and wc_ref.get('whereClauseOID'):
                        wc_ref_elem.set('WhereClauseOID', wc_ref['whereClauseOID'])
    
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
                    
                    # Restore TranslatedText attributes (xml:lang, etc.)
                    if method.get('_translatedText_attributes'):
                        for attr_name, attr_value in method['_translatedText_attributes'].items():
                            tt.set(attr_name, attr_value)
    
    def _create_analysis_result_displays(self, parent: ET.Element, displays: List[Dict[str, Any]], ns: str) -> None:
        """Create AnalysisResultDisplays elements with correct hierarchy.
        
        Each AnalysisResults element is a sibling under ResultDisplay.
        """
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
                
                # Restore TranslatedText attributes (xml:lang, etc.)
                if display.get('_translatedText_attributes'):
                    for attr_name, attr_value in display['_translatedText_attributes'].items():
                        tt.set(attr_name, attr_value)
            
            # Add ResultDisplay children
            for rd in display.get('resultDisplays', []):
                rd_elem = ET.SubElement(display_elem, f'{{{def_ns}}}ResultDisplay' if def_ns else 'ResultDisplay')

                self._apply_stored_attributes(rd_elem, rd)
                
                if not rd_elem.get('OID') and rd.get('OID'):
                    rd_elem.set('OID', rd['OID'])
                if not rd_elem.get('Name') and rd.get('name'):
                    rd_elem.set('Name', rd['name'])
                
                if rd.get('description'):
                    desc = ET.SubElement(rd_elem, f'{{{ns}}}Description' if ns else 'Description')
                    tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                    tt.text = rd['description']
                    
                    # Restore TranslatedText attributes (xml:lang, etc.)
                    if rd.get('_translatedText_attributes'):
                        for attr_name, attr_value in rd['_translatedText_attributes'].items():
                            tt.set(attr_name, attr_value)
                
                # Create AnalysisResults elements (can be multiple per ResultDisplay)
                for result in rd.get('analysisResults', []):
                    # Each AnalysisResults element is a sibling
                    analysis_results_elem = ET.SubElement(rd_elem, f'{{{def_ns}}}AnalysisResults' if def_ns else 'AnalysisResults')
                    
                    self._apply_stored_attributes(analysis_results_elem, result)
                    
                    if not analysis_results_elem.get('OID') and result.get('OID'):
                        analysis_results_elem.set('OID', result['OID'])
                    
                    if result.get('description'):
                        desc = ET.SubElement(analysis_results_elem, f'{{{ns}}}Description' if ns else 'Description')
                        tt = ET.SubElement(desc, f'{{{ns}}}TranslatedText' if ns else 'TranslatedText')
                        tt.text = result['description']
                        
                        # Restore TranslatedText attributes (xml:lang, etc.)
                        if result.get('_translatedText_attributes'):
                            for attr_name, attr_value in result['_translatedText_attributes'].items():
                                tt.set(attr_name, attr_value)
                    
                    # Restore child elements recursively (AnalysisVariable, AnalysisDataset, etc.)
                    self._restore_generic_children(analysis_results_elem, result, def_ns)
    
    def _restore_generic_children(self, parent_elem: ET.Element, parent_dict: Dict[str, Any], def_ns: str) -> None:
        """Recursively restore child elements from generic structure.
        
        Args:
            parent_elem: Parent XML element to add children to
            parent_dict: Parent dictionary containing _*_elements keys
            def_ns: Define namespace
        """
        # Process all keys that represent element lists
        for key, value in parent_dict.items():
            if key.startswith('_') and key.endswith('_elements') and key not in ['_attributes', '_translatedText_attributes']:
                # Extract element name from key (e.g., "_AnalysisVariable_elements" -> "AnalysisVariable")
                element_name = key[1:-9]  # Remove leading "_" and trailing "_elements"
                
                for elem_data in value:
                    # Create the child element
                    child_elem = ET.SubElement(parent_elem, f'{{{def_ns}}}{element_name}' if def_ns else element_name)
                    
                    # Apply attributes
                    if '_attributes' in elem_data:
                        for attr_name, attr_value in elem_data['_attributes'].items():
                            child_elem.set(attr_name, attr_value)
                    
                    # Add text content
                    if '_text' in elem_data and elem_data['_text']:
                        child_elem.text = elem_data['_text']
                    
                    # Recursively process nested children
                    self._restore_generic_children(child_elem, elem_data, def_ns)


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
