"""
Define-XML to Define-JSON converter.

Portable converter with no external dependencies that transforms Define-XML
files into Define-JSON format while preserving all semantic information.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class PortableDefineXMLToJSONConverter:
    """Portable Define-XML to Define-JSON converter with no external dependencies."""
    
    def __init__(self):
        self.namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
    
    def convert_file(self, xml_path: Path, output_path: Path) -> Dict[str, Any]:
        """Convert Define-XML file to Define-JSON."""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Find Study and MetaDataVersion
        study = root.find('.//odm:Study', self.namespaces)
        mdv = root.find('.//odm:MetaDataVersion', self.namespaces)
        
        if not study or not mdv:
            raise ValueError("Could not find Study or MetaDataVersion in Define-XML")
        
        # Extract ALL original metadata (no hardcoding!)
        metadata = {
            'fileOID': root.get('FileOID'),
            'asOfDateTime': root.get('AsOfDateTime'),
            'creationDateTime': root.get('CreationDateTime'),
            'odmVersion': root.get('ODMVersion'),
            'fileType': root.get('FileType'),
            'originator': root.get('Originator'),
            'sourceSystem': root.get('SourceSystem'),
            'sourceSystemVersion': root.get('SourceSystemVersion'),
            'context': root.get('{%s}Context' % self.namespaces['def']),
            'studyOID': study.get('OID'),
            'studyName': self._get_study_name(study),
            'studyDescription': self._get_study_description(study),
            'protocolName': self._get_protocol_name(study),
            'defineVersion': mdv.get('{%s}DefineVersion' % self.namespaces['def'])
        }
        
        # Build Define-JSON structure
        define_json = {
            'metadata': metadata,
            'metaDataVersion': {
                'OID': mdv.get('OID'),
                'name': mdv.get('Name', mdv.get('OID')),
                'description': mdv.get('Description', '')
            }
        }
        
        # Process main elements
        define_json['Datasets'] = self._process_item_groups(mdv)
        define_json['Variables'] = self._process_items(mdv)
        define_json['ValueLists'] = self._process_value_lists(mdv)
        define_json['CodeLists'] = self._process_code_lists(mdv)
        define_json['WhereClauses'] = self._process_where_clauses(mdv)
        define_json['Methods'] = self._process_methods(mdv)
        define_json['Standards'] = self._process_standards(mdv)
        define_json['AnnotatedCRF'] = self._process_annotated_crf(mdv)
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(define_json, f, indent=2)
        
        return define_json
    
    def _process_item_groups(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ItemGroupDef elements."""
        item_groups = []
        for ig in mdv.findall('.//odm:ItemGroupDef', self.namespaces):
            item_group = {
                'OID': ig.get('OID'),
                'name': ig.get('Name'),
                'description': self._get_description(ig),
                'label': ig.get('def:Label', ''),
                'domain': ig.get('Domain'),
                'structure': ig.get('def:Structure'),
                'class': ig.get('def:Class'),
                'repeating': ig.get('Repeating') == 'Yes',
                'sasDatasetName': ig.get('SASDatasetName'),
                'archiveLocationID': ig.get('def:ArchiveLocationID'),
                'items': []
            }
            
            # Process ItemRefs
            for item_ref in ig.findall('odm:ItemRef', self.namespaces):
                # Get WhereClauseRef child element
                where_clause_ref = item_ref.find('def:WhereClauseRef', self.namespaces)
                where_clause_oid = where_clause_ref.get('WhereClauseOID') if where_clause_ref is not None else None
                
                item_group['items'].append({
                    'itemOID': item_ref.get('ItemOID'),
                    'mandatory': item_ref.get('Mandatory', 'No'),
                    'role': item_ref.get('Role'),
                    'whereClauseOID': where_clause_oid
                })
            
            item_groups.append(item_group)
        
        return item_groups
    
    def _process_items(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ItemDef elements."""
        items = []
        for item in mdv.findall('.//odm:ItemDef', self.namespaces):
            items.append({
                'OID': item.get('OID'),
                'name': item.get('Name'),
                'dataType': item.get('DataType'),
                'length': item.get('Length'),
                'significantDigits': item.get('SignificantDigits'),
                'description': self._get_description(item),
                'label': item.get('def:Label'),
                'origin': self._get_origin(item)
            })
        return items
    
    def _process_value_lists(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process ValueListDef elements."""
        value_lists = []
        for vl in mdv.findall('.//def:ValueListDef', self.namespaces):
            value_list = {
                'OID': vl.get('OID'),
                'name': vl.get('OID'),  # Use OID as name
                'description': self._get_description(vl),
                'items': []
            }
            
            # Process ItemRefs in ValueList
            for item_ref in vl.findall('odm:ItemRef', self.namespaces):
                # Get WhereClauseRef child element
                where_clause_ref = item_ref.find('def:WhereClauseRef', self.namespaces)
                where_clause_oid = where_clause_ref.get('WhereClauseOID') if where_clause_ref is not None else None
                
                value_list['items'].append({
                    'itemOID': item_ref.get('ItemOID'),
                    'mandatory': item_ref.get('Mandatory', 'No'),
                    'whereClauseOID': where_clause_oid
                })
            
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
    
    def _process_where_clauses(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process WhereClauseDef elements."""
        where_clauses = []
        for wc in mdv.findall('.//def:WhereClauseDef', self.namespaces):
            where_clause = {
                'oid': wc.get('OID'),
                'description': self._get_description(wc),
                'conditions': []
            }
            
            # Process RangeChecks
            for rc in wc.findall('.//odm:RangeCheck', self.namespaces):
                check_value = rc.find('.//odm:CheckValue', self.namespaces)
                if check_value is not None:
                    where_clause['conditions'].append(
                        f"{rc.get('Comparator', 'EQ')} {check_value.text or ''}"
                    )
            
            where_clauses.append(where_clause)
        
        return where_clauses
    
    def _process_methods(self, mdv: ET.Element) -> List[Dict[str, Any]]:
        """Process MethodDef elements."""
        methods = []
        for method in mdv.findall('.//odm:MethodDef', self.namespaces):
            methods.append({
                'oid': method.get('OID'),
                'name': method.get('Name'),
                'type': method.get('Type'),
                'description': self._get_description(method)
            })
        return methods
    
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
        """Extract origin information."""
        origin_elem = element.find('.//def:Origin', self.namespaces)
        if origin_elem is not None:
            return {
                'type': origin_elem.get('Type'),
                'source': origin_elem.get('Source')
            }
        return {}
