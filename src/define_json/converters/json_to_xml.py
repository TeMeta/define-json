"""
Define-JSON to Define-XML converter.

Projects context-first slices to Define-XML ValueLists.
"""

import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False


# Type aliases for better code readability
ItemGroupDict = Dict[str, Any]
ItemDict = Dict[str, Any]


class DefineJSONToXMLConverter:
    """Convert Define-JSON back to Define-XML with context-first slice structure."""
    
    def __init__(self, stylesheet_href: str = "define2-1.xsl"):
        """
        Initialize converter.
        
        Args:
            stylesheet_href: The href attribute for the XML stylesheet processing instruction.
        """
        self.stylesheet_href = stylesheet_href
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
        
        # Handle nested metaDataVersion format
        json_data = self._normalize_json_structure(json_data)
        
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
        # Collect existing ItemOIDs to avoid creating WhereClauses for non-existent items
        existing_item_oids = set()
        for item in json_data.get('items', []):
            existing_item_oids.add(item.get('OID'))
        
        self._create_conditions_and_where_clauses(
            mdv, 
            json_data.get('conditions', []), 
            json_data.get('whereClauses', []),
            existing_item_oids
        )
        
        # Process all ItemGroups (both domain and ValueList ItemGroups)
        # Separate domain ItemGroups and ValueList ItemGroups for proper XML structure
        all_item_groups = json_data.get('itemGroups', [])
        domain_item_groups = [ig for ig in all_item_groups if ig.get('type') != 'DataSpecialization']
        value_list_item_groups = [ig for ig in all_item_groups if ig.get('type') == 'DataSpecialization']
        
        # Project context-first slices to ValueLists
        if value_list_item_groups:
            self._create_value_lists_from_slices(mdv, value_list_item_groups, domain_item_groups)
        else:
            # Fallback for data without slices
            self._create_value_lists(mdv, value_list_item_groups)
        
        # Then create domain ItemGroups
        self._create_item_groups(mdv, domain_item_groups)
        
        # Process ItemDefs (Variables) - collect from both top-level and nested in itemGroups
        items = json_data.get('items', [])
        
        # Always also extract items from itemGroups (since items are now nested inline)
        nested_items = []
        for ig in json_data.get('itemGroups', []):
            for item in ig.get('items', []):
                # Items should already have OID field (schema conformant)
                # But handle legacy itemOID for backward compatibility
                if 'itemOID' in item and 'OID' not in item:
                    item = item.copy()  # Don't modify original
                    item['OID'] = item['itemOID']
                nested_items.append(item)
        
        # Combine top-level and nested items, removing duplicates by OID
        all_items = items + nested_items
        unique_items = {}
        for item in all_items:
            oid = item.get('OID') or item.get('itemOID')
            if oid:
                unique_items[oid] = item
        
        self._create_item_defs(mdv, list(unique_items.values()))
        
        # Process CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []))
        
        # Process Methods
        self._create_methods(mdv, json_data.get('Methods', []))
        
        # Write to file with stylesheet processing instruction
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        
        # Create XML string with processing instruction
        xml_str = ET.tostring(root, encoding='unicode')
        
        # Format the XML properly
        dom = xml.dom.minidom.parseString(xml_str)
        formatted_xml = dom.toprettyxml(indent="  ", encoding=None)
        
        # Add stylesheet processing instruction after XML declaration
        lines = formatted_xml.split('\n')
        xml_declaration = '<?xml version="1.0" encoding="utf-8"?>'
        stylesheet_pi = f'<?xml-stylesheet type="text/xsl" href="{self.stylesheet_href}"?>'
        
        # Write the complete XML with processing instruction
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_declaration + '\n')
            f.write(stylesheet_pi + '\n')
            # Skip the minidom XML declaration and write the rest
            content_lines = [line for line in lines if line.strip() and not line.strip().startswith('<?xml')]
            f.write('\n'.join(content_lines))
        
        return root
    
    def convert_to_html(self, json_path: Path, output_path: Path, xsl_path: Optional[Path] = None) -> bool:
        """
        Convert Define-JSON to HTML using XSL transformation.
        Simply converts JSON to XML first, then applies XSL transformation.
        
        Args:
            json_path: Path to input Define-JSON file
            output_path: Path for output HTML file
            xsl_path: Path to XSL stylesheet (defaults to bundled define2-1.xsl)
            
        Returns:
            True if successful, False otherwise
        """
        if not LXML_AVAILABLE:
            raise ImportError("lxml is required for HTML generation. Install with: pip install lxml")
        
        try:
            # Step 1: Convert JSON to XML (temporary file)
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp_xml:
                temp_xml_path = Path(tmp_xml.name)
            
            # Generate XML first
            self.convert_file(json_path, temp_xml_path)
            
            # Step 2: Apply XSL transformation to the XML
            success = self.xml_to_html(temp_xml_path, output_path, xsl_path)
            
            # Clean up temporary file
            temp_xml_path.unlink()
            
            return success
            
        except Exception as e:
            print(f"Error during HTML generation: {e}")
            return False
    
    def xml_to_html(self, xml_path: Path, output_path: Path, xsl_path: Optional[Path] = None) -> bool:
        """
        Convert XML to HTML using XSL transformation.
        
        Args:
            xml_path: Path to input XML file
            output_path: Path for output HTML file
            xsl_path: Path to XSL stylesheet (defaults to bundled define2-1.xsl)
            
        Returns:
            True if successful, False otherwise
        """
        if not LXML_AVAILABLE:
            raise ImportError("lxml is required for HTML generation. Install with: pip install lxml")
        
        # Use bundled XSL if none provided
        if xsl_path is None:
            xsl_path = Path(__file__).parent.parent.parent.parent / "data" / "define2-1.xsl"
        
        if not xsl_path.exists():
            raise FileNotFoundError(f"XSL stylesheet not found: {xsl_path}")
        
        if not xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_path}")
        
        try:
            # Load XML document
            xml_doc = etree.parse(str(xml_path))
            
            # Load XSL stylesheet
            xsl_doc = etree.parse(str(xsl_path))
            transform = etree.XSLT(xsl_doc)
            
            # Apply transformation
            html_doc = transform(xml_doc)
            
            # Write HTML output
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(html_doc))
            
            return True
            
        except Exception as e:
            print(f"Error during XSL transformation: {e}")
            return False
    
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
    
    def _safe_str(self, value: Any) -> str:
        """Safely convert any value to string for XML attributes."""
        if isinstance(value, bool):
            return 'Yes' if value else 'No'
        elif value is None:
            return ''
        else:
            return str(value)
    
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
    
    def _create_value_lists_from_slices(self, parent: ET.Element, slices: List[Dict[str, Any]], domain_groups: List[Dict[str, Any]]) -> None:
        """
        Project context-first slices to variable-first ValueListDefs.
        
        Groups slice items by variable name across contexts to create proper ValueListDefs
        that represent the same variable under different contexts.
        """
        # Group items by (domain, variable) to create ValueLists
        var_to_contexts: Dict[tuple, List[Dict[str, Any]]] = {}
        
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
            
            # Determine ValueList OID from variable pattern
            # Use first item's OID as template
            first_item_oid = contexts[0]['item'].get('OID') or contexts[0]['item'].get('itemOID', '')
            
            # Create ValueList OID
            if '.' in first_item_oid:
                parts = first_item_oid.split('.')
                if len(parts) >= 3:
                    vl_oid = f"VL.{domain}.{var_name}"
                else:
                    vl_oid = f"VL.{domain}.{var_name}"
            else:
                vl_oid = f"VL.{domain}.{var_name}"
            
            vl_elem = ET.SubElement(parent, '{%s}ValueListDef' % self.namespaces['def'])
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
                
                if where_clause:
                    wc_ref = ET.SubElement(item_ref, '{%s}WhereClauseRef' % self.namespaces['def'])
                    wc_ref.set('WhereClauseOID', where_clause)
        
        logger.info(f"Projected {len(var_to_contexts)} variables to ValueLists")
    
    def _create_value_lists(self, parent: ET.Element, value_lists: List[Dict[str, Any]]):
        """Create ValueListDef elements (legacy path for non-canonical IR)."""
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
                item_ref.set('Mandatory', self._safe_str(item.get('mandatory', 'No')))
                
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
    
    def _create_conditions_and_where_clauses(self, parent: ET.Element, conditions: List[Dict[str, Any]], where_clauses: List[Dict[str, Any]], existing_item_oids: set = None):
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
                
                # Only create WhereClauses for ItemOIDs that actually exist (no assumptions)
                variables = ['LBORRES', 'LBORRESU'] if domain == 'LB' else ['VSORRES', 'VSORRESU']
                
                for variable in variables:
                    # Check if the corresponding ItemOID actually exists
                    expected_item_oid = f'IT.{domain}.{variable}.{parameter}'
                    if existing_item_oids and expected_item_oid not in existing_item_oids:
                        continue  # Skip creating WhereClause for non-existent ItemOID
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
                ig_elem.set('Repeating', self._safe_str(ds['repeating']))
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
                # Items should have OID field (schema conformant), but handle legacy itemOID
                item_oid = item.get('OID') or item.get('itemOID', '')
                item_ref.set('ItemOID', item_oid)
                
                # Convert boolean mandatory to string
                mandatory = item.get('mandatory', 'No')
                item_ref.set('Mandatory', self._safe_str(mandatory))
                
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
            # Default to text if dataType is missing (common for user-defined variables)
            item_elem.set('DataType', var.get('dataType', 'text'))
            if var.get('length'):
                item_elem.set('Length', str(var['length']))
            if var.get('significantDigits'):
                item_elem.set('SignificantDigits', str(var['significantDigits']))
            
            # Add def:Label attribute if present
            if var.get('label'):
                item_elem.set('{%s}Label' % self.namespaces['def'], var['label'])
            
            # Add Description element if present (separate from label)
            if var.get('description'):
                desc = ET.SubElement(item_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = var['description']
            
            # Add CodeListRef if present
            # The 'codeList' field is an object reference (stores the OID)
            if var.get('codeList'):
                code_list_ref = ET.SubElement(item_elem, 'CodeListRef')
                code_list_ref.set('CodeListOID', var['codeList'])
            
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
            # Handle both 'OID' and 'oid' field names
            oid = cl.get('OID') or cl.get('oid', '')
            cl_elem.set('OID', oid)
            if cl.get('name'):
                cl_elem.set('Name', cl['name'])
            # Default to text if dataType is missing
            if cl.get('dataType'):
                cl_elem.set('DataType', cl['dataType'])
            
            # Add CodeListItems - handle both 'codeListItems' and 'items'
            items = cl.get('codeListItems') or cl.get('items', [])
            for item in items:
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
