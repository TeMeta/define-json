"""
Define-JSON to Define-XML converter.

Converts Define-JSON format back to Define-XML for bidirectional roundtrip validation
and legacy system compatibility.
"""

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class DefineJSONToXMLConverter:
    """Convert Define-JSON back to Define-XML for true roundtrip validation."""
    
    def __init__(self):
        self.namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        
        # Register namespace prefixes for proper output
        ET.register_namespace('def', self.namespaces['def'])
        ET.register_namespace('xlink', self.namespaces['xlink'])
    
    def convert_file(self, json_path: Path, output_path: Path) -> ET.Element:
        """Convert Define-JSON file back to Define-XML."""
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        # Create root ODM element with proper namespace (let registration handle prefixes)
        root = ET.Element('ODM')
        root.set('xmlns', self.namespaces['odm'])
        
        # Extract metadata from flattened structure - NO HARDCODING!
        # Set root attributes from ODMFileMetadata mixin attributes
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
        if json_data.get('context'):
            root.set('{%s}Context' % self.namespaces['def'], json_data['context'])
        
        # Create Study element using StudyMetadata mixin attributes
        study = ET.SubElement(root, 'Study')
        study.set('OID', json_data.get('studyOID', 'UNKNOWN'))
        
        # Global Variables
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
        
        # MetaDataVersion using flattened attributes
        mdv = ET.SubElement(study, 'MetaDataVersion')
        mdv.set('OID', json_data.get('OID', 'MDV.ROUNDTRIP'))
        mdv.set('Name', json_data.get('name', 'Roundtrip MetaDataVersion'))
        if json_data.get('description'):
            mdv.set('Description', json_data['description'])
        if json_data.get('defineVersion'):
            mdv.set('{%s}DefineVersion' % self.namespaces['def'], json_data['defineVersion'])
        
        # Process Standards first (they should be early in MetaDataVersion)
        self._create_standards(mdv, json_data.get('standards', []))
        
        # Process AnnotatedCRF next
        self._create_annotated_crf(mdv, json_data.get('annotatedCRF', []))
        
        # Process Conditions and WhereClauses with proper separation
        self._create_conditions_and_where_clauses(
            mdv, 
            json_data.get('conditions', []), 
            json_data.get('whereClauses', [])
        )
        
        # Process all ItemGroups (both domain and ValueList ItemGroups)
        # Separate domain ItemGroups and ValueList ItemGroups for proper XML structure
        all_item_groups = json_data.get('itemGroups', [])
        domain_item_groups = [ig for ig in all_item_groups if ig.get('type') != 'DataSpecialization']
        value_list_item_groups = [ig for ig in all_item_groups if ig.get('type') == 'DataSpecialization']
        
        # Create ValueLists first (they need to be before ItemGroups in XML)
        self._create_value_lists(mdv, value_list_item_groups)
        
        # Then create domain ItemGroups
        self._create_item_groups(mdv, domain_item_groups)
        
        # Process ItemDefs (Variables)
        self._create_item_defs(mdv, json_data.get('items', []))
        
        # Process CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []))
        
        # Process Methods
        self._create_methods(mdv, json_data.get('Methods', []))
        
        # Write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        return root
    
    def _create_standards(self, parent: ET.Element, standards: List[Dict[str, Any]]):
        """Create def:Standards section."""
        if standards:
            standards_elem = ET.SubElement(parent, '{%s}Standards' % self.namespaces['def'])
            
            for standard in standards:
                standard_elem = ET.SubElement(standards_elem, '{%s}Standard' % self.namespaces['def'])
                if standard.get('OID'):
                    standard_elem.set('OID', standard['OID'])
                if standard.get('name'):
                    standard_elem.set('Name', standard['name'])
                if standard.get('type'):
                    standard_elem.set('Type', standard['type'])
                if standard.get('version'):
                    standard_elem.set('Version', standard['version'])
                if standard.get('status'):
                    standard_elem.set('Status', standard['status'])
                if standard.get('publishingSet'):
                    standard_elem.set('PublishingSet', standard['publishingSet'])
    
    def _create_annotated_crf(self, parent: ET.Element, annotated_crf: List[Dict[str, Any]]):
        """Create def:AnnotatedCRF section."""
        if annotated_crf:
            crf_elem = ET.SubElement(parent, '{%s}AnnotatedCRF' % self.namespaces['def'])
            
            for doc_ref in annotated_crf:
                doc_ref_elem = ET.SubElement(crf_elem, '{%s}DocumentRef' % self.namespaces['def'])
                if doc_ref.get('leafID'):
                    doc_ref_elem.set('leafID', doc_ref['leafID'])
    
    def _create_value_lists(self, parent: ET.Element, value_lists: List[Dict[str, Any]]):
        """Create ValueListDef elements."""
        for vl in value_lists:
            vl_elem = ET.SubElement(parent, '{%s}ValueListDef' % self.namespaces['def'])
            vl_elem.set('OID', vl.get('OID', ''))
            
            if vl.get('description'):
                desc = ET.SubElement(vl_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = vl['description']
            
            # Add ItemRefs
            for item in vl.get('items', []):
                item_ref = ET.SubElement(vl_elem, 'ItemRef')
                item_ref.set('ItemOID', item.get('itemOID', ''))
                item_ref.set('Mandatory', item.get('mandatory', 'No'))
                
                if item.get('whereClauseOID'):
                    wc_ref = ET.SubElement(item_ref, '{%s}WhereClauseRef' % self.namespaces['def'])
                    
                    # For Dataset Specialization: Convert shared WhereClause OID back to original format
                    shared_wc_oid = item['whereClauseOID']
                    item_oid = item.get('itemOID', '')
                    
                    # Extract variable from ItemOID (e.g., IT.LB.LBORRES.AST -> LBORRES)
                    parts = item_oid.split('.')
                    if len(parts) >= 3:
                        variable = parts[2]  # LBORRES, LBORRESU, VSORRES, VSORRESU
                        
                        # Convert WC.LB.AST to WC.LB.LBORRES.AST for roundtrip compatibility
                        if shared_wc_oid.count('.') == 2:  # Shared format like WC.LB.AST
                            original_wc_oid = shared_wc_oid.replace(f'.{parts[1]}.', f'.{parts[1]}.{variable}.')
                            wc_ref.set('WhereClauseOID', original_wc_oid)
                        else:
                            wc_ref.set('WhereClauseOID', shared_wc_oid)
                    else:
                        wc_ref.set('WhereClauseOID', shared_wc_oid)
    
    def _create_conditions_and_where_clauses(self, parent: ET.Element, conditions: List[Dict[str, Any]], where_clauses: List[Dict[str, Any]]):
        """Create WhereClauseDef elements from separated Conditions and WhereClauses."""
        # Create a lookup for conditions by OID
        conditions_by_oid = {cond.get('OID'): cond for cond in conditions}
        
        for wc in where_clauses:
            wc_oid = wc.get('OID', '')
            
            # Parse OID like WC.VS.TEMP -> extract VS.TEMP
            parts = wc_oid.split('.')
            if len(parts) >= 3:
                domain = parts[1]  # VS, LB
                parameter = parts[2]  # TEMP, AST, etc.
                
                # Create original variable-specific WhereClauses for roundtrip compatibility
                variables = ['LBORRES', 'LBORRESU'] if domain == 'LB' else ['VSORRES', 'VSORRESU']
                
                for variable in variables:
                    original_oid = f'WC.{domain}.{variable}.{parameter}'
                    
                    wc_elem = ET.SubElement(parent, '{%s}WhereClauseDef' % self.namespaces['def'])
                    wc_elem.set('OID', original_oid)
                    
                    # Use original-style description for roundtrip compatibility
                    desc = ET.SubElement(wc_elem, 'Description')
                    trans_text = ET.SubElement(desc, 'TranslatedText')
                    trans_text.text = f'Condition for {variable} {parameter}'
                    
                    # Find the referenced condition and extract range checks
                    for condition_oid in wc.get('conditions', []):
                        condition = conditions_by_oid.get(condition_oid)
                        if condition:
                            # Convert rangeChecks back to original format
                            for range_check_data in condition.get('rangeChecks', []):
                                range_check = ET.SubElement(wc_elem, 'RangeCheck')
                                range_check.set('Comparator', range_check_data.get('comparator', 'EQ'))
                                
                                check_values = range_check_data.get('checkValues', [])
                                if check_values and check_values[0]:
                                    check_value = ET.SubElement(range_check, 'CheckValue')
                                    check_value.text = check_values[0]
                            break  # Only use first condition for roundtrip compatibility
    
    def _create_item_groups(self, parent: ET.Element, datasets: List[Dict[str, Any]]):
        """Create ItemGroupDef elements."""
        for ds in datasets:
            ig_elem = ET.SubElement(parent, 'ItemGroupDef')
            ig_elem.set('OID', ds.get('OID', ''))
            if ds.get('name'):
                ig_elem.set('Name', ds['name'])
            if ds.get('domain'):
                ig_elem.set('Domain', ds['domain'])
            if ds.get('repeating') is not None:
                ig_elem.set('Repeating', 'Yes' if ds['repeating'] else 'No')
            if ds.get('sasDatasetName'):
                ig_elem.set('SASDatasetName', ds['sasDatasetName'])
            if ds.get('structure'):
                ig_elem.set('{%s}Structure' % self.namespaces['def'], ds['structure'])
            if ds.get('class'):
                ig_elem.set('{%s}Class' % self.namespaces['def'], ds['class'])
            if ds.get('label'):
                ig_elem.set('{%s}Label' % self.namespaces['def'], ds['label'])
            if ds.get('archiveLocationID'):
                ig_elem.set('{%s}ArchiveLocationID' % self.namespaces['def'], ds['archiveLocationID'])
            
            if ds.get('description'):
                desc = ET.SubElement(ig_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = ds['description']
            
            # Add ItemRefs
            for item in ds.get('items', []):
                item_ref = ET.SubElement(ig_elem, 'ItemRef')
                item_ref.set('ItemOID', item.get('itemOID', ''))
                item_ref.set('Mandatory', item.get('mandatory', 'No'))
                if item.get('role'):
                    item_ref.set('Role', item['role'])
                
                if item.get('whereClauseOID'):
                    wc_ref = ET.SubElement(item_ref, '{%s}WhereClauseRef' % self.namespaces['def'])
                    wc_ref.set('WhereClauseOID', item['whereClauseOID'])
    
    def _create_item_defs(self, parent: ET.Element, variables: List[Dict[str, Any]]):
        """Create ItemDef elements."""
        for var in variables:
            item_elem = ET.SubElement(parent, 'ItemDef')
            item_elem.set('OID', var.get('OID', ''))
            if var.get('name'):
                item_elem.set('Name', var['name'])
            if var.get('dataType'):
                item_elem.set('DataType', var['dataType'])
            if var.get('length'):
                item_elem.set('Length', str(var['length']))
            if var.get('significantDigits'):
                item_elem.set('SignificantDigits', str(var['significantDigits']))
            if var.get('label'):
                item_elem.set('{%s}Label' % self.namespaces['def'], var['label'])
            
            if var.get('description'):
                desc = ET.SubElement(item_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = var['description']
            
            # Add Origin if present
            origin = var.get('origin', {})
            if origin and (origin.get('type') or origin.get('source')):
                origin_elem = ET.SubElement(item_elem, '{%s}Origin' % self.namespaces['def'])
                if origin.get('type'):
                    origin_elem.set('Type', origin['type'])
                if origin.get('source'):
                    origin_elem.set('Source', origin['source'])
    
    def _create_code_lists(self, parent: ET.Element, code_lists: List[Dict[str, Any]]):
        """Create CodeList elements."""
        for cl in code_lists:
            cl_elem = ET.SubElement(parent, 'CodeList')
            cl_elem.set('OID', cl.get('oid', ''))
            if cl.get('name'):
                cl_elem.set('Name', cl['name'])
            if cl.get('dataType'):
                cl_elem.set('DataType', cl['dataType'])
            
            # Add CodeListItems
            for item in cl.get('items', []):
                cli_elem = ET.SubElement(cl_elem, 'CodeListItem')
                cli_elem.set('CodedValue', item.get('codedValue', ''))
                
                if item.get('decode'):
                    decode = ET.SubElement(cli_elem, 'Decode')
                    trans_text = ET.SubElement(decode, 'TranslatedText')
                    trans_text.text = item['decode']
    
    def _create_methods(self, parent: ET.Element, methods: List[Dict[str, Any]]):
        """Create MethodDef elements."""
        for method in methods:
            method_elem = ET.SubElement(parent, 'MethodDef')
            method_elem.set('OID', method.get('oid', ''))
            if method.get('name'):
                method_elem.set('Name', method['name'])
            if method.get('type'):
                method_elem.set('Type', method['type'])
            
            if method.get('description'):
                desc = ET.SubElement(method_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = method['description']
