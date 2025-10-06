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
from typing import Dict, List, Any, Optional

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False


class DefineJSONToXMLConverter:
    """Convert Define-JSON back to Define-XML for true roundtrip validation."""
    
    def __init__(self, stylesheet_href: str = "define2-1.xsl"):
        """
        Initialize converter.
        
        Args:
            stylesheet_href: The href attribute for the XML stylesheet processing instruction.
                           Can be a relative path, absolute path, or URL.
                           Examples:
                           - "define2-1.xsl" (relative, default)
                           - "./define2-1.xsl" (explicit relative)
                           - "https://example.com/define2-1.xsl" (URL)
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
        
        # Generate ODM metadata from JSON content (data-driven, not hardcoded)
        study_info = self._extract_study_info(json_data)
        
        # Set ODM root attributes with generated metadata
        root.set('FileOID', study_info['file_oid'])
        root.set('CreationDateTime', datetime.now().isoformat())
        root.set('AsOfDateTime', datetime.now().isoformat())
        root.set('ODMVersion', '1.3.2')
        root.set('FileType', 'Snapshot')
        root.set('Originator', study_info['originator'])
        root.set('SourceSystem', 'define-json')
        root.set('SourceSystemVersion', '1.0.0')
        root.set('{%s}Context' % self.namespaces['def'], 'Other')
        
        # Create Study element with generated metadata
        study = ET.SubElement(root, 'Study')
        study.set('OID', study_info['study_oid'])
        
        # Global Variables with generated metadata
        global_vars = ET.SubElement(study, 'GlobalVariables')
        study_name = ET.SubElement(global_vars, 'StudyName')
        study_name.text = study_info['study_name']
        study_desc = ET.SubElement(global_vars, 'StudyDescription')
        study_desc.text = study_info['study_description']
        protocol = ET.SubElement(global_vars, 'ProtocolName')
        protocol.text = study_info['protocol_name']
        
        # MetaDataVersion with generated metadata
        mdv = ET.SubElement(study, 'MetaDataVersion')
        mdv.set('OID', study_info['mdv_oid'])
        mdv.set('Name', study_info['mdv_name'])
        mdv.set('Description', study_info['mdv_description'])
        mdv.set('{%s}DefineVersion' % self.namespaces['def'], '2.1.0')
        
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
        
        # Create ValueLists first (they need to be before ItemGroups in XML)
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
        
        self._create_item_defs(mdv, list(unique_items.values()), json_data.get('codeLists', []))
        
        # Process CodeLists
        self._create_code_lists(mdv, json_data.get('codeLists', []))
        
        # Process Methods
        self._create_methods(mdv, json_data.get('methods', []))
        
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
                # Handle both OID and itemOID for compatibility
                item_oid = item.get('OID') or item.get('itemOID', '')
                item_ref.set('ItemOID', item_oid)
                item_ref.set('Mandatory', item.get('mandatory', 'No'))
                
                # Handle both whereClause and whereClauseOID for compatibility
                where_clause = item.get('whereClause') or item.get('whereClauseOID')
                if where_clause:
                    wc_ref = ET.SubElement(item_ref, '{%s}WhereClauseRef' % self.namespaces['def'])
                    
                    # For Dataset Specialization: Convert shared WhereClause OID back to original format
                    shared_wc_oid = where_clause
                    
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
    
    def _extract_study_info(self, json_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract study information from JSON content, preserving existing names when available."""
        # PREFER existing ODM metadata from JSON if available
        # Otherwise, generate fallbacks based on content
        
        # Check for existing ODM metadata
        study_oid = json_data.get('studyOID')
        file_oid = json_data.get('fileOID')
        mdv_oid = json_data.get('metaDataVersionOID')
        
        # If no existing metadata, extract domain information for fallback generation
        if not study_oid or not file_oid or not mdv_oid:
            domains = set()
            item_count = 0
            dataset_count = len(json_data.get('itemGroups', []))
            
            for ig in json_data.get('itemGroups', []):
                domain = ig.get('name', '').upper()
                # Check for traditional domain codes (DM, AE, etc.) or use first part of descriptive names
                if domain and len(domain) <= 2:  # Traditional domain code
                    domains.add(domain)
                elif domain:  # Descriptive name - extract meaningful part
                    # Extract first meaningful word (e.g., "Vital_Sign" -> "VS", "Randomization" -> "RAND")
                    words = domain.split('_')
                    if words:
                        # Create abbreviation from first letters
                        abbrev = ''.join(word[0] for word in words[:2] if word)
                        if len(abbrev) <= 4:  # Reasonable abbreviation length
                            domains.add(abbrev)
                item_count += len(ig.get('items', []))
            
            # Generate meaningful identifiers based on content
            domain_list = sorted(domains)
            primary_domain = domain_list[0] if domain_list else 'STUDY'
            
            # Generate OIDs based on content only if not provided
            if not file_oid:
                file_oid = f"ODM.DEFINE.{primary_domain}.{datetime.now().strftime('%Y%m%d')}"
            if not study_oid:
                study_oid = f"ODM.STUDY.{primary_domain}"
            if not mdv_oid:
                mdv_oid = f"MDV.{primary_domain}"
            
            # PRESERVE existing names when available, generate meaningful defaults when missing
            study_name = json_data.get('studyName') or (f"Multi-Domain Study ({len(domains)} domains)" if len(domains) > 1 else f"{primary_domain} Study")
            study_description = json_data.get('studyDescription') or (f"Study containing {dataset_count} datasets with {item_count} variables across {len(domains)} domains" if len(domains) > 1 else f"Study containing {dataset_count} datasets with {item_count} variables")
            protocol_name = json_data.get('protocolName') or f"Protocol {primary_domain}"
            
            # For MetaDataVersion, use existing name/description if available
            mdv_name = json_data.get('metaDataVersionName') or f"MetaDataVersion {primary_domain}"
            mdv_description = json_data.get('description') or (f"Data definitions for {', '.join(domain_list)} domains" if domain_list else f"Data definitions for {dataset_count} datasets")
            
            # Generate originator based on content
            originator = f"Define-JSON Converter (Generated from {len(domains)} domains, {dataset_count} datasets)"
        else:
            # Use existing metadata
            study_name = json_data.get('studyName', 'Study')
            study_description = json_data.get('studyDescription', '')
            protocol_name = json_data.get('protocolName', 'Protocol')
            mdv_name = json_data.get('metaDataVersionName', 'MetaDataVersion')
            mdv_description = json_data.get('description', '')
            originator = "Define-JSON Converter"
        
        return {
            'file_oid': file_oid,
            'study_oid': study_oid,
            'mdv_oid': mdv_oid,
            'study_name': study_name,
            'study_description': study_description,
            'protocol_name': protocol_name,
            'mdv_name': mdv_name,
            'mdv_description': mdv_description,
            'originator': originator
        }

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
    
    def _create_item_defs(self, parent: ET.Element, variables: List[Dict[str, Any]], available_code_lists: List[Dict[str, Any]] = None):
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
            
            # Add CodeListRef if present or intelligently assign one
            codelist_oid = var.get('codelist') or var.get('codeList')
            if not codelist_oid and available_code_lists:
                codelist_oid = self._intelligently_assign_codelist(var, available_code_lists)
            
            if codelist_oid:
                cl_ref = ET.SubElement(item_elem, '{%s}CodeListRef' % self.namespaces['def'])
                cl_ref.set('CodeListOID', codelist_oid)
            
            # Add MethodRef if present
            if var.get('method'):
                method_ref = ET.SubElement(item_elem, '{%s}MethodRef' % self.namespaces['def'])
                method_ref.set('MethodOID', var['method'])
            
            # Add Origin if present
            origin = var.get('origin', {})
            if origin and (origin.get('type') or origin.get('source')):
                origin_elem = ET.SubElement(item_elem, '{%s}Origin' % self.namespaces['def'])
                if origin.get('type'):
                    origin_elem.set('Type', origin['type'])
                if origin.get('source'):
                    origin_elem.set('Source', origin['source'])
    
    def _intelligently_assign_codelist(self, item: Dict[str, Any], available_code_lists: List[Dict[str, Any]]) -> str:
        """Intelligently assign a CodeList to an item based on content analysis."""
        import re
        
        name = item.get('name', '').lower()
        description = item.get('description', '').lower()
        
        # Create a mapping of CodeList OIDs to their names for pattern matching
        codelist_map = {cl.get('oid', ''): cl.get('name', '').lower() for cl in available_code_lists}
        
        # Yes/No questions
        if any(word in name or word in description for word in ['are you', 'do you', 'have you', 'would you', 'can you', 'will you', 'is', 'was', 'did', 'should', 'could']):
            if 'CL.YESNO' in codelist_map:
                return 'CL.YESNO'
        
        # Satisfaction questions
        if any(word in name or word in description for word in ['satisfied', 'satisfaction', 'agree', 'disagree', 'comfortable', 'uncomfortable']):
            if 'CL.SATISFACTION' in codelist_map:
                return 'CL.SATISFACTION'
        
        # Likelihood questions
        if any(word in name or word in description for word in ['likely', 'unlikely', 'neutral', 'extremely likely', 'extremely unlikely']):
            if 'CL.LIKELIHOOD' in codelist_map:
                return 'CL.LIKELIHOOD'
        
        # Comfort level questions
        if any(word in name or word in description for word in ['comfortable', 'uncomfortable', 'very comfortable', 'very uncomfortable', 'comfort level']):
            if 'CL.COMFORT_LEVEL' in codelist_map:
                return 'CL.COMFORT_LEVEL'
        
        # Preference questions
        if any(word in name or word in description for word in ['prefer', 'preference', 'indifferent', 'tampon', 'clinic']):
            if 'CL.PREFERENCE' in codelist_map:
                return 'CL.PREFERENCE'
        
        # Likert scale questions
        if any(word in name or word in description for word in ['likert', 'scale', 'strongly agree', 'strongly disagree']):
            if 'CL.LIKERT_SCALE' in codelist_map:
                return 'CL.LIKERT_SCALE'
        
        # Concern level questions
        if any(word in name or word in description for word in ['concerned', 'not concerned', 'extremely concerned', 'moderately concerned', 'concern level']):
            if 'CL.CONCERN_LEVEL' in codelist_map:
                return 'CL.CONCERN_LEVEL'
        
        return None
    
    def _create_code_lists(self, parent: ET.Element, code_lists: List[Dict[str, Any]]):
        """Create CodeList elements."""
        for cl in code_lists:
            cl_elem = ET.SubElement(parent, 'CodeList')
            # Handle both 'OID' and 'oid' field names
            oid = cl.get('OID') or cl.get('oid', '')
            cl_elem.set('OID', oid)
            if cl.get('name'):
                cl_elem.set('Name', cl['name'])
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
            # Handle both 'OID' and 'oid' field names
            oid = method.get('OID') or method.get('oid', '')
            method_elem.set('OID', oid)
            if method.get('name'):
                method_elem.set('Name', method['name'])
            if method.get('type'):
                method_elem.set('Type', method['type'])
            
            if method.get('description'):
                desc = ET.SubElement(method_elem, 'Description')
                trans_text = ET.SubElement(desc, 'TranslatedText')
                trans_text.text = method['description']
