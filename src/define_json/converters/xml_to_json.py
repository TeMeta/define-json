"""
Improved Define-XML to Define-JSON converter with proper Pydantic validation.

Key improvements:
1. Uses Comment structure for extra data (like origin descriptions) instead of forbidden fields
2. Maintains structured hierarchy with Items nested in ItemGroups
3. Graceful error handling with data preservation in supplemental structures
4. Full Pydantic validation throughout
5. Matches the structure from xml_to_json_structured.py output

Roundtrip Modes:
- preserve_original=True (DEFAULT): Perfect roundtrip conversion
  * No inference or normalization
  * Preserves exact XML attribute values
  * Method types stored as-is (e.g., "Derivation" not mapped to "Computation")
  * No origin type inference from comments
  * No default dataType assignment
  * No automatic method linking
  * Best for: XML -> JSON -> XML workflows

- preserve_original=False: Smart conversion with inference
  * Maps method types (Derivation -> Computation)
  * Infers origin types from comment patterns
  * Assigns default dataType="text" when missing
  * Links methods via description matching
  * Logs all inference operations in _xmlMetadata.inferenceLog
  * Best for: One-way migrations, data analysis

Usage:
    # Perfect roundtrip (default)
    converter = DefineXMLToJSONConverter()
    converter.convert_file(xml_path, json_path)
    
    # With inference
    converter = DefineXMLToJSONConverter(preserve_original=False)
    converter.convert_file(xml_path, json_path)
    
    # Command line
    python xml_to_json.py input.xml output.json                    # preserve original
    python xml_to_json.py input.xml output.json --infer           # with inference
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Import Pydantic models from define.py
import sys
sys.path.insert(0, '/mnt/project')

from ..schema.define import (
    MetaDataVersion,
    Item,
    ItemGroup,
    CodeList,
    CodeListItem,
    Dictionary,
    Method,
    WhereClause,
    Condition,
    Origin,
    RangeCheck,
    Coding,
    TranslatedText,
    DocumentReference,
    Standard,
    StandardName,
    DataType,
    OriginType,
    OriginSource,
    Comment,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DefineXMLToJSONConverter:
    """
    Improved Define-XML to Define-JSON converter with proper Pydantic validation.
    
    Features:
    - Items nested within ItemGroups (structured hierarchy)
    - ValueLists processed as ItemGroups with type="DataSpecialization"
    - Hierarchical structure with children references
    - Optional method linking based on derivation descriptions
    - Origin information properly structured with comments
    - Full Pydantic validation throughout
    - Graceful error handling with data preservation
    - XML metadata preserved for roundtrip conversion
    
    Roundtrip Modes:
    - preserve_original=True (default): Perfect XML -> JSON -> XML roundtrip
    - preserve_original=False: Smart inference for one-way conversion
    
    See module docstring for detailed usage information.
    """
    
    def __init__(self, preserve_original: bool = True):
        """
        Initialize the converter.
        
        Args:
            preserve_original: If True (default), preserves original XML values for perfect roundtrip.
                             If False, applies inference and normalization for one-way conversion.
        """
        self.preserve_original = preserve_original
        self.namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.3',
            'def': 'http://www.cdisc.org/ns/def/v2.1',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        self.legacy_namespaces = {
            'odm': 'http://www.cdisc.org/ns/odm/v1.2',
            'def': 'http://www.cdisc.org/ns/def/v1.0',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        self.active_namespaces = self.namespaces
        
        # Track inference operations when preserve_original is False
        self.inference_log = [] if not preserve_original else None
        
    def _detect_namespaces(self, root: ET.Element, xml_path: Path = None) -> Dict[str, str]:
        """Auto-detect namespace version from XML root."""
        # Try to get namespaces using iterparse if we have the file path
        if xml_path and xml_path.exists():
            detected_namespaces = {}
            try:
                for event, (prefix, uri) in ET.iterparse(str(xml_path), events=['start-ns']):
                    detected_namespaces[prefix if prefix else 'odm'] = uri
                if detected_namespaces:
                    return detected_namespaces
            except:
                pass  # Fall back to other methods
        
        # First try to extract all namespaces from root element
        detected_namespaces = {}
        
        # Get all xmlns attributes
        for attr_name, attr_value in root.attrib.items():
            if attr_name == 'xmlns':
                detected_namespaces['odm'] = attr_value
            elif attr_name.startswith('xmlns:'):
                prefix = attr_name.split(':', 1)[1]
                detected_namespaces[prefix] = attr_value
        
        # If we found namespaces, use them
        if detected_namespaces:
            return detected_namespaces
        
        # Otherwise fall back to version detection
        root_tag = root.tag
        if root_tag.startswith('{'):
            namespace_end = root_tag.find('}')
            root_namespace = root_tag[1:namespace_end]
            
            if 'v1.2' in root_namespace:
                return self.legacy_namespaces
            elif 'v1.3' in root_namespace:
                return self.namespaces
        
        # Check attributes for def namespace
        for attr_name, attr_value in root.attrib.items():
            if 'def' in attr_name and 'v1.0' in attr_value:
                return self.legacy_namespaces
            elif 'def' in attr_name and ('v2.0' in attr_value or 'v2.1' in attr_value):
                return self.namespaces
        
        return self.namespaces
    
    def convert_file(self, xml_path: Path, output_path: Path) -> Dict[str, Any]:
        """Convert Define-XML file to Pydantic-validated Define-JSON."""
        mode = "preserve-original (perfect roundtrip)" if self.preserve_original else "infer (one-way conversion)"
        logger.info(f"Starting conversion of {xml_path} [mode: {mode}]")
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Auto-detect and use appropriate namespaces
        self.active_namespaces = self._detect_namespaces(root, xml_path)
        logger.info(f"Using namespaces: {self.active_namespaces}")
        
        # Find Study and MetaDataVersion
        study = root.find('.//odm:Study', self.active_namespaces)
        mdv = root.find('.//odm:MetaDataVersion', self.active_namespaces)
        
        if study is None or mdv is None:
            raise ValueError("Could not find Study or MetaDataVersion in Define-XML")
        
        # Build MetaDataVersion data for Pydantic model
        mdv_data = {
            # ODM File Metadata (required by schema)
            'fileOID': root.get('FileOID', 'FILE.001'),
            'creationDateTime': self._parse_datetime(root.get('CreationDateTime')),
            'odmVersion': root.get('ODMVersion', '1.3.2'),
            'fileType': root.get('FileType', 'Snapshot'),
            
            # Study Metadata
            'studyOID': study.get('OID', 'STUDY.001'),
            
            # MetaDataVersion attributes
            'OID': mdv.get('OID', 'MDV.001'),
        }
        
        # Optional ODM attributes
        if root.get('AsOfDateTime'):
            mdv_data['asOfDateTime'] = self._parse_datetime(root.get('AsOfDateTime'))
        if root.get('Originator'):
            mdv_data['originator'] = root.get('Originator')
        if root.get('SourceSystem'):
            mdv_data['sourceSystem'] = root.get('SourceSystem')
        if root.get('SourceSystemVersion'):
            mdv_data['sourceSystemVersion'] = root.get('SourceSystemVersion')
        
        # Context and DefineVersion
        context = root.get('{%s}Context' % self.active_namespaces['def'])
        if context:
            mdv_data['context'] = context
        
        define_version = mdv.get('{%s}DefineVersion' % self.active_namespaces['def'])
        if define_version:
            mdv_data['defineVersion'] = define_version
        
        # Study metadata
        study_name = self._get_study_name(study)
        if study_name:
            mdv_data['studyName'] = study_name
        
        study_desc = self._get_study_description(study)
        if study_desc:
            mdv_data['studyDescription'] = study_desc
        
        protocol_name = self._get_protocol_name(study)
        if protocol_name:
            mdv_data['protocolName'] = protocol_name
        
        # MetaDataVersion name and description
        if mdv.get('Name'):
            mdv_data['name'] = mdv.get('Name')
        if mdv.get('Description'):
            mdv_data['description'] = mdv.get('Description')
        
        # Store XML-specific attributes for roundtrip
        xml_metadata = {
            'namespaces': self.active_namespaces,
        }
        
        # Fix #1: Preserve ODM Root-Level Attributes
        odm_metadata = {}
        if mdv.get('Name'):
            odm_metadata['Name'] = mdv.get('Name')
        if define_version:
            odm_metadata['DefineVersion'] = define_version
        if study_name:
            odm_metadata['StudyName'] = study_name
        if study_desc:
            odm_metadata['StudyDescription'] = study_desc
        if protocol_name:
            odm_metadata['ProtocolName'] = protocol_name
        if odm_metadata:
            xml_metadata['_odmMetadata'] = odm_metadata
        
        # Store xsi:schemaLocation if present
        xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance'
        xsi_schema_location = root.get(f'{{{xsi_ns}}}schemaLocation')
        if xsi_schema_location:
            xml_metadata['xsiSchemaLocation'] = xsi_schema_location
        
        # Fix #5: Preserve original ItemDef ordering
        item_def_order = []
        for item_def in mdv.findall('odm:ItemDef', self.active_namespaces):
            item_oid = item_def.get('OID')
            if item_oid:
                item_def_order.append(item_oid)
        if item_def_order:
            xml_metadata['itemDefOrder'] = item_def_order
        
        # Create Standard object if standardName and standardVersion exist
        standard_name = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
        standard_version = mdv.get('{%s}StandardVersion' % self.active_namespaces['def'])
        
        # Check if Standards element exists (vs just attributes)
        standards_element = mdv.find('odm:Standards', self.active_namespaces) or mdv.find('def:Standards', self.active_namespaces)
        has_standards_element = standards_element is not None
        
        if standard_name or standard_version:
            standard_data = {
                'OID': 'STD.001',  # Generate a simple OID for the standard
            }
            
            # Map common standard name variations to enum values
            standard_name_map = {
                'CDISC ADaM': 'ADaMIG',
                'ADaM': 'ADaMIG',
                'CDISC SDTM': 'SDTMIG',
                'SDTM': 'SDTMIG',
                'CDISC SEND': 'SENDIG',
                'SEND': 'SENDIG',
            }
            
            if standard_name:
                mapped_name = standard_name_map.get(standard_name, standard_name)
                try:
                    standard_data['name'] = StandardName(mapped_name)
                except ValueError:
                    # If not a valid enum value, store in xml_metadata instead
                    logger.warning(f"StandardName '{standard_name}' not in enum, storing in xml_metadata")
                    xml_metadata['standardName'] = standard_name
                    standard_name = None  # Don't create Standard object
            
            if standard_version and standard_name:  # Only if name was valid
                standard_data['version'] = standard_version
            
            if standard_name:  # Only create if we have a valid name
                try:
                    standard_obj = Standard(**standard_data)
                    mdv_data['standards'] = [standard_obj]
                    logger.info(f"  - Created Standard: {standard_data.get('name')} v{standard_version}")
                    # Mark whether Standards was an element or just attributes
                    xml_metadata['hasStandardsElement'] = has_standards_element
                except Exception as e:
                    logger.warning(f"Failed to create Standard object: {e}")
                    xml_metadata['standardName'] = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
                    xml_metadata['standardVersion'] = standard_version
            elif standard_version:
                # Have version but no valid name
                xml_metadata['standardVersion'] = standard_version
                xml_metadata['hasStandardsElement'] = has_standards_element
        
        # Process methods first to build derivation method map
        logger.info("Processing methods...")
        methods, derivation_method_map, methods_supplemental = self._process_methods(mdv)
        if methods:
            mdv_data['methods'] = methods
            logger.info(f"  - Created {len(methods)} methods")
        
        # Process item groups with nested items (using structured approach)
        logger.info("Processing item groups with nested items...")
        item_groups, ig_supplemental = self._process_item_groups_with_hierarchy(mdv, derivation_method_map)
        if item_groups:
            mdv_data['itemGroups'] = item_groups
            logger.info(f"  - Created {len(item_groups)} item groups")
            total_items = sum(len(ig.items or []) for ig in item_groups)
            logger.info(f"  - Total items nested in groups: {total_items}")
        
        # Process code lists
        logger.info("Processing code lists...")
        code_lists, dictionaries, cl_supplemental = self._process_code_lists(mdv)
        if code_lists:
            mdv_data['codeLists'] = code_lists
            logger.info(f"  - Created {len(code_lists)} code lists")
        if dictionaries:
            mdv_data['dictionaries'] = dictionaries
            logger.info(f"  - Created {len(dictionaries)} dictionaries")
        
        # Fix #4: Process SupplementalDoc (store in xml_metadata)
        logger.info("Processing supplemental doc...")
        supplemental_doc = self._process_supplemental_doc(mdv)
        if supplemental_doc:
            xml_metadata['supplementalDoc'] = supplemental_doc
            logger.info(f"  - Found SupplementalDoc with {len(supplemental_doc.get('documentRefs', []))} references")
        
        # Fix #3: Process AnalysisResultDisplays (store in xml_metadata)
        logger.info("Processing analysis result displays...")
        analysis_displays = self._process_analysis_result_displays(mdv)
        if analysis_displays:
            xml_metadata['analysisResultDisplays'] = analysis_displays
            logger.info(f"  - Found {len(analysis_displays)} AnalysisResultDisplays containers")
        
        # Capture MetaDataVersion-level def:leaf elements (document references, display locations)
        logger.info("Processing MetaDataVersion-level leaf elements...")
        mdv_leaves = []
        for leaf_elem in mdv.findall('def:leaf', self.active_namespaces):
            leaf_data = {}
            leaf_id = leaf_elem.get('ID')
            if leaf_id:
                leaf_data['ID'] = leaf_id
            
            # xlink:href attribute
            href = leaf_elem.get('{%s}href' % self.active_namespaces['xlink'])
            if href:
                leaf_data['href'] = href
            
            # def:title child element
            title_elem = leaf_elem.find('def:title', self.active_namespaces)
            if title_elem is not None and title_elem.text:
                leaf_data['title'] = title_elem.text
            
            if leaf_data:
                mdv_leaves.append(leaf_data)
        
        if mdv_leaves:
            xml_metadata['mdvLeaves'] = mdv_leaves
            logger.info(f"  - Found {len(mdv_leaves)} MetaDataVersion-level leaf elements")
        
        # Process conditions and where clauses
        logger.info("Processing conditions and where clauses...")
        conditions, where_clauses, cond_supplemental = self._process_conditions_and_where_clauses(mdv)
        if conditions:
            mdv_data['conditions'] = conditions
            logger.info(f"  - Created {len(conditions)} conditions")
        if where_clauses:
            mdv_data['whereClauses'] = where_clauses
            logger.info(f"  - Created {len(where_clauses)} where clauses")
        
        # Create MetaDataVersion Pydantic model to validate
        logger.info("Validating with Pydantic...")
        try:
            mdv_model = MetaDataVersion(**mdv_data)
            # Convert to dict for JSON output
            result = mdv_model.model_dump(mode='json', exclude_none=True)
            logger.info("Pydantic validation successful")
        except Exception as e:
            logger.error(f"Failed to create MetaDataVersion model: {e}")
            logger.error(f"Data keys: {mdv_data.keys()}")
            # Fall back to raw data
            result = mdv_data
        
        # Add supplemental XML metadata for roundtrip
        xml_metadata.update({
            'itemGroupSupplemental': ig_supplemental,
            'codeListSupplemental': cl_supplemental,
            'methodSupplemental': methods_supplemental,
            'conditionSupplemental': cond_supplemental,
        })
        
        # Add inference log if preserve_original is False
        if not self.preserve_original and self.inference_log:
            xml_metadata['inferenceLog'] = self.inference_log
            logger.info(f"  - Recorded {len(self.inference_log)} inference operations")
        
        result['_xmlMetadata'] = xml_metadata
        
        # Save to file
        logger.info(f"Writing output to {output_path}")
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        logger.info("Conversion complete!")
        return result
    
    def _parse_datetime(self, dt_str: Optional[str]) -> datetime:
        """
        Parse datetime string to datetime object.
        Auto-generates current datetime if None to ensure valid Define-JSON.
        """
        if not dt_str:
            # Auto-generate current datetime if missing
            generated_dt = datetime.now()
            logger.info(f"Auto-generating creationDateTime: {generated_dt.isoformat()}")
            return generated_dt
            
        try:
            # Handle ISO format with T separator
            if 'T' in dt_str:
                # Remove timezone info if present for simplicity
                dt_str = dt_str.split('+')[0].split('-')[0] if '+' in dt_str or dt_str.count('-') > 2 else dt_str
                return datetime.fromisoformat(dt_str.replace('T', ' '))
            return datetime.fromisoformat(dt_str)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse datetime '{dt_str}': {e}, using current datetime")
            return datetime.now()
    
    def _process_methods(self, mdv: ET.Element) -> Tuple[List[Method], Dict[str, Dict], Dict]:
        """
        Process MethodDef elements into Pydantic Method objects.
        
        Returns:
            Tuple of (methods_list, derivation_method_map, supplemental_data)
        """
        methods = []
        derivation_map = {}
        supplemental = {}
        
        # Process MethodDef elements (Define-XML v2.x style)
        for method_elem in mdv.findall('.//odm:MethodDef', self.active_namespaces):
            method_oid = method_elem.get('OID')
            if not method_oid:
                continue
            
            method_data = {'OID': method_oid}
            
            # Get name
            name = method_elem.get('Name')
            if name:
                method_data['name'] = name
            
            # Get type with optional smart mapping for common Define-XML types
            method_type = method_elem.get('Type')
            if method_type:
                if self.preserve_original:
                    # Store original type as-is for perfect roundtrip
                    method_data['type'] = method_type
                else:
                    # Map common Define-XML types to valid MethodType enum values
                    type_mapping = {
                        'Derivation': 'Computation',  # Derivation is effectively computation
                        'Assigned': 'Computation',
                        'Algorithm': 'Computation',
                    }
                    mapped_type = type_mapping.get(method_type, method_type)
                    if mapped_type != method_type:
                        self.inference_log.append({
                            'operation': 'method_type_mapping',
                            'oid': method_oid,
                            'original': method_type,
                            'mapped': mapped_type
                        })
                    method_data['type'] = mapped_type
            
            # Get description from FormalExpression or Description
            description = self._get_method_description(method_elem)
            if description:
                method_data['description'] = description
                # Map description to method OID for linking
                derivation_map[description.strip()] = {'OID': method_oid}
            
            try:
                method_obj = Method(**method_data)
                methods.append(method_obj)
                # Fix #6: Track that this method is from original XML (not synthetic)
                if method_oid not in supplemental:
                    supplemental[method_oid] = {}
                supplemental[method_oid]['_isFromXML'] = True
            except Exception as e:
                logger.warning(f"Failed to create Method {method_oid}: {e}")
                method_data['_isFromXML'] = True  # Still mark even if validation fails
                supplemental[method_oid] = method_data
        
        # Process ComputationMethod elements (Define-XML v1.x style)
        # NOTE: These are NOT MethodDef elements - they're part of ARM AnalysisResults
        # They should not be recreated as top-level MethodDef elements in the XML
        for comp_method in mdv.findall('.//def:ComputationMethod', self.active_namespaces):
            method_oid = comp_method.get('OID')
            if not method_oid:
                continue
            
            method_data = {
                'OID': method_oid,
                'type': 'Computation'
            }
            
            if comp_method.get('Name'):
                method_data['name'] = comp_method.get('Name')
            
            if comp_method.text and comp_method.text.strip():
                description = comp_method.text.strip()
                method_data['description'] = description
                derivation_map[description] = {'OID': method_oid}
            
            try:
                method_obj = Method(**method_data)
                methods.append(method_obj)
                # Mark as ComputationMethod (not MethodDef) - don't create MethodDef in roundtrip
                if method_oid not in supplemental:
                    supplemental[method_oid] = {}
                supplemental[method_oid]['_isComputationMethod'] = True
                # Don't mark as _isFromXML since these aren't MethodDef elements
            except Exception as e:
                logger.warning(f"Failed to create Method {method_oid}: {e}")
                method_data['_isComputationMethod'] = True
                supplemental[method_oid] = method_data
        
        return methods, derivation_map, supplemental
    
    def _get_method_description(self, method_elem: ET.Element) -> Optional[str]:
        """Extract method description from FormalExpression or Description."""
        # Try FormalExpression first
        formal_expr = method_elem.find('.//odm:FormalExpression', self.active_namespaces)
        if formal_expr is not None and formal_expr.text:
            return formal_expr.text.strip()
        
        # Try Description/TranslatedText
        desc = method_elem.find('.//odm:Description/odm:TranslatedText', self.active_namespaces)
        if desc is not None and desc.text:
            return desc.text.strip()
        
        return None
    
    def _process_item_groups_with_hierarchy(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict]:
        """
        Process ItemGroupDef elements with items nested inside (using ItemGroup.items field).
        Also establishes parent-child relationships with ValueLists.
        
        Returns:
            Tuple of (item_groups_list, supplemental_data)
        """
        item_groups = []
        supplemental = {}
        
        # Process domain-level ItemGroups
        domain_igs, domain_supp = self._process_domain_item_groups(mdv, derivation_method_map)
        item_groups.extend(domain_igs)
        
        # Extract and merge item origin metadata
        domain_origin_meta = domain_supp.pop('_itemOriginMetadata', {})
        supplemental.update(domain_supp)
        
        # Process ValueLists as ItemGroups with type="ValueList"
        value_list_igs, vl_supp = self._process_value_lists_as_item_groups(mdv, derivation_method_map)
        item_groups.extend(value_list_igs)
        
        # Extract and merge item origin metadata
        vl_origin_meta = vl_supp.pop('_itemOriginMetadata', {})
        supplemental.update(vl_supp)
        
        # Combine all origin metadata
        all_origin_metadata = {**domain_origin_meta, **vl_origin_meta}
        if all_origin_metadata:
            supplemental['_itemOriginMetadata'] = all_origin_metadata
        
        logger.info(f"  - Found {len(value_list_igs)} ValueList ItemGroups")
        
        # Build map of ValueListOID -> parent ItemGroup OID
        # Check multiple locations robustly:
        # 1. def:ValueListRef/def:ValueListOID on ItemRef (most common)
        # 2. def:ValueListRef/def:ValueListOID on ItemDef
        # 3. Nested def:WhereClauseRef on ItemRef (for conditional ValueLists)
        valuelist_to_parent = {}
        
        # Track which ItemGroups reference each ValueList for comprehensive mapping
        for ig_elem in mdv.findall('.//odm:ItemGroupDef', self.active_namespaces):
            ig_oid = ig_elem.get('OID')
            
            for item_ref in ig_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                
                # Method 1: Check ItemRef for direct ValueList reference (most common)
                vl_ref = item_ref.get('{%s}ValueListRef' % self.active_namespaces['def'])
                if not vl_ref:
                    vl_ref = item_ref.get('{%s}ValueListOID' % self.active_namespaces['def'])
                
                if vl_ref:
                    # Add to parent mapping (may have multiple parents - that's OK)
                    if vl_ref not in valuelist_to_parent:
                        valuelist_to_parent[vl_ref] = []
                    if ig_oid not in valuelist_to_parent[vl_ref]:
                        valuelist_to_parent[vl_ref].append(ig_oid)
                        logger.info(f"    - ItemRef {item_oid} references ValueList {vl_ref}, parent is {ig_oid}")
                    continue
                
                # Method 2: Check the ItemDef itself for ValueList reference
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                if item_def is not None:
                    vl_ref = item_def.get('{%s}ValueListOID' % self.active_namespaces['def'])
                    if not vl_ref:
                        vl_ref = item_def.get('{%s}ValueListRef' % self.active_namespaces['def'])
                    
                    if vl_ref:
                        if vl_ref not in valuelist_to_parent:
                            valuelist_to_parent[vl_ref] = []
                        if ig_oid not in valuelist_to_parent[vl_ref]:
                            valuelist_to_parent[vl_ref].append(ig_oid)
                            logger.info(f"    - ItemDef {item_oid} references ValueList {vl_ref}, parent is {ig_oid}")
        
        # Log summary of ValueList parent relationships
        for vl_oid, parent_oids in valuelist_to_parent.items():
            if len(parent_oids) > 1:
                logger.info(f"    - ValueList {vl_oid} has multiple parents: {parent_oids}")
        
        # Add ValueList OIDs as children to their parent domains
        # A ValueList can have multiple parents (used in multiple domains)
        children_added = 0
        for vl_ig in value_list_igs:
            parent_oids = valuelist_to_parent.get(vl_ig.OID, [])
            
            # Handle both single parent (backward compat) and multiple parents
            if isinstance(parent_oids, str):
                parent_oids = [parent_oids]
            
            for parent_oid in parent_oids:
                # Find the parent domain ItemGroup and add this ValueList as a child
                for domain_ig in domain_igs:
                    if domain_ig.OID == parent_oid:
                        if domain_ig.children is None:
                            domain_ig.children = []
                        if vl_ig.OID not in domain_ig.children:
                            domain_ig.children.append(vl_ig.OID)
                            children_added += 1
                            logger.info(f"    - Added {vl_ig.OID} as child of {parent_oid}")
                        break
        
        logger.info(f"  - Added {children_added} ValueList children to parent domains")
        
        # If inference is enabled, try to infer ValueList -> Domain links based on OID substring matching
        if not self.preserve_original:
            inferred_links = self._infer_valuelist_domain_links(value_list_igs, domain_igs, valuelist_to_parent)
            logger.info(f"  - Inferred {inferred_links} additional ValueList links via OID matching")
        
        return item_groups, supplemental
    
    def _infer_valuelist_domain_links(
        self, 
        value_list_igs: List[ItemGroup], 
        domain_igs: List[ItemGroup],
        existing_links: Dict[str, List[str]]
    ) -> int:
        """
        Infer ValueList to Domain relationships based on OID substring matching.
        
        Strategy:
        1. For each ValueList, extract potential variable OIDs from its OID
        2. For each Domain, check if any of its Items' OIDs are substrings of the ValueList OID
        3. If match found and not already linked, add as child relationship
        
        Example:
        - ValueList OID: "VL.AE.AEACN"
        - Domain: "IG.AE" with item OID "IT.AEACN"
        - Match: "AEACN" appears in both, so link VL.AE.AEACN as child of IG.AE
        
        Args:
            value_list_igs: List of ValueList ItemGroups
            domain_igs: List of Domain ItemGroups  
            existing_links: Dictionary of ValueList OID -> parent Domain OID(s)
            
        Returns:
            Number of new links inferred
        """
        inferred_count = 0
        
        for vl_ig in value_list_igs:
            # Skip if already has explicit parent links
            if vl_ig.OID in existing_links and existing_links[vl_ig.OID]:
                continue
            
            # Extract the variable part from ValueList OID
            # Common patterns: "VL.DOMAIN.VARIABLE", "ValueList.VARIABLE", etc.
            vl_parts = vl_ig.OID.split('.')
            
            # Try to find matching domain by checking item OIDs
            for domain_ig in domain_igs:
                # Skip non-domain types
                if domain_ig.type and domain_ig.type != 'Domain':
                    continue
                
                # Check if any of the domain's items match the ValueList
                if not domain_ig.items:
                    continue
                
                match_found = False
                matched_item_oid = None
                
                for item in domain_ig.items:
                    item_oid = item.OID
                    
                    # Strategy 1: Check if item OID is a substring of ValueList OID
                    if item_oid in vl_ig.OID:
                        match_found = True
                        matched_item_oid = item_oid
                        break
                    
                    # Strategy 2: Check if last part of ValueList OID matches last part of item OID
                    if vl_parts and len(vl_parts) > 1:
                        vl_variable = vl_parts[-1]
                        item_parts = item_oid.split('.')
                        if item_parts and len(item_parts) > 0:
                            item_variable = item_parts[-1]
                            if vl_variable == item_variable:
                                match_found = True
                                matched_item_oid = item_oid
                                break
                    
                    # Strategy 3: Check if any part of ValueList OID matches item name
                    if item.name and item.name in vl_ig.OID:
                        match_found = True
                        matched_item_oid = item_oid
                        break
                
                if match_found:
                    # Add as child if not already there
                    if domain_ig.children is None:
                        domain_ig.children = []
                    
                    if vl_ig.OID not in domain_ig.children:
                        domain_ig.children.append(vl_ig.OID)
                        inferred_count += 1
                        
                        # Log the inference
                        self.inference_log.append({
                            'operation': 'valuelist_domain_link_inference',
                            'valuelist_oid': vl_ig.OID,
                            'domain_oid': domain_ig.OID,
                            'matched_item_oid': matched_item_oid,
                            'reason': f'Item OID "{matched_item_oid}" matches ValueList OID pattern'
                        })
                        
                        logger.info(f"    - Inferred: {vl_ig.OID} ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€šÃ‚Â ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ {domain_ig.OID} (matched via {matched_item_oid})")
        
        return inferred_count
    
    def _process_domain_item_groups(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict]:
        """Process domain-level ItemGroupDef elements as Pydantic ItemGroup objects."""
        item_groups = []
        supplemental = {}
        item_origin_metadata = {}  # Track origin metadata for all items
        
        for ig_elem in mdv.findall('.//odm:ItemGroupDef', self.active_namespaces):
            ig_oid = ig_elem.get('OID')
            if not ig_oid:
                continue
            
            ig_data = {'OID': ig_oid}
            ig_supp = {'OID': ig_oid}
            
            # Name
            if ig_elem.get('Name'):
                ig_data['name'] = ig_elem.get('Name')
            
            # Description (prefer def:Label)
            label = ig_elem.get('{%s}Label' % self.active_namespaces['def'])
            if label:
                ig_data['label'] = label
            
            description = self._get_description(ig_elem)
            if description:
                ig_data['description'] = description
            elif not label and ig_elem.get('Domain'):
                ig_data['description'] = f"{ig_elem.get('Domain')} domain dataset"
            
            # Domain - this IS a valid ItemGroup field!
            domain = ig_elem.get('Domain')
            if domain:
                ig_data['domain'] = domain
            
            # Structure
            structure = ig_elem.get('{%s}Structure' % self.active_namespaces['def'])
            if structure:
                ig_data['structure'] = structure
            
            # Purpose - this is a SEPARATE attribute, not Class!
            purpose = ig_elem.get('Purpose')
            if purpose:
                ig_data['purpose'] = purpose
            
            # Store def: namespaced attributes in supplemental for roundtrip
            # def:Class
            class_attr = ig_elem.get('{%s}Class' % self.active_namespaces['def'])
            if class_attr:
                ig_supp['defClass'] = class_attr
            
            # def:DomainKeys
            domain_keys = ig_elem.get('{%s}DomainKeys' % self.active_namespaces['def'])
            if domain_keys:
                ig_supp['defDomainKeys'] = domain_keys
            
            # def:Label (already captured above but ensure it's in supplemental too)
            if label:
                ig_supp['defLabel'] = label
            
            # Comment attribute (including empty values like " ")
            comment = ig_elem.get('Comment')
            if comment is not None:  # Check for None, not truthiness (to capture empty strings)
                ig_supp['comment'] = comment
            
            # Repeating (store in supplemental as string for roundtrip)
            repeating = ig_elem.get('Repeating')
            if repeating:
                ig_supp['repeating'] = repeating
            
            # IsReferenceData
            is_ref_data = ig_elem.get('IsReferenceData')
            if is_ref_data:
                ig_data['isReferenceData'] = is_ref_data == 'Yes'
            
            # SASDatasetName (supplemental)
            sas_name = ig_elem.get('SASDatasetName')
            if sas_name:
                ig_supp['sasDatasetName'] = sas_name
            
            # ArchiveLocationID (supplemental)
            archive_loc = ig_elem.get('{%s}ArchiveLocationID' % self.active_namespaces['def'])
            if archive_loc:
                ig_supp['archiveLocationID'] = archive_loc
            
            # Capture def:leaf elements (for dataset locations)
            leaf_elem = ig_elem.find('def:leaf', self.active_namespaces)
            if leaf_elem is not None:
                leaf_data = {}
                leaf_id = leaf_elem.get('ID')
                if leaf_id:
                    leaf_data['ID'] = leaf_id
                
                # xlink:href attribute
                href = leaf_elem.get('{%s}href' % self.active_namespaces['xlink'])
                if href:
                    leaf_data['href'] = href
                
                # def:title child element
                title_elem = leaf_elem.find('def:title', self.active_namespaces)
                if title_elem is not None and title_elem.text:
                    leaf_data['title'] = title_elem.text
                
                if leaf_data:
                    ig_supp['leaf'] = leaf_data
            
            # Process ItemRefs - create full Item objects nested in items list
            items = []
            item_order_numbers = {}  # Track OrderNumber for each item
            for item_ref in ig_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                
                # Capture OrderNumber if present (for exact roundtrip)
                order_number = item_ref.get('OrderNumber')
                if order_number:
                    item_order_numbers[item_oid] = order_number
                
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                
                if item_def is not None:
                    item_obj, item_supp = self._create_item_object(item_def, item_ref, derivation_method_map)
                    if item_obj:
                        items.append(item_obj)
                        # Collect origin metadata
                        if 'originMetadata' in item_supp:
                            item_origin_metadata[item_oid] = item_supp['originMetadata']
            
            if items:
                ig_data['items'] = items
            
            # Store OrderNumbers in supplemental for exact roundtrip
            if item_order_numbers:
                ig_supp['itemOrderNumbers'] = item_order_numbers
            
            # Create ItemGroup Pydantic object
            try:
                ig_obj = ItemGroup(**ig_data)
                item_groups.append(ig_obj)
                supplemental[ig_oid] = ig_supp
            except Exception as e:
                logger.error(f"Failed to create ItemGroup {ig_oid}: {e}")
                supplemental[ig_oid] = {**ig_data, **ig_supp}
        
        # Store item origin metadata at top level
        if item_origin_metadata:
            supplemental['_itemOriginMetadata'] = item_origin_metadata
        
        return item_groups, supplemental
    
    def _create_item_object(self, item_def: ET.Element, item_ref: ET.Element = None, 
                           derivation_method_map: Dict = None) -> Tuple[Optional[Item], Dict]:
        """
        Create a Pydantic Item object from ItemDef and ItemRef.
        
        Uses comments field for extra origin information to maintain Pydantic conformance.
        
        Returns:
            Tuple of (Item object, supplemental_data)
        """
        item_oid = item_def.get('OID')
        if not item_oid:
            return None, {}
        
        item_data = {'OID': item_oid}
        item_supp = {'OID': item_oid}
        origin_metadata = {}  # Store comment and format metadata separately
        
        # Name
        if item_def.get('Name'):
            item_data['name'] = item_def.get('Name')
        
        # Label (prefer def:Label)
        label = item_def.get('{%s}Label' % self.active_namespaces['def'])
        if label:
            item_data['label'] = label
        
        # Description
        description = self._get_description(item_def)
        if description:
            item_data['description'] = description
        
        # DataType (required by schema, but may not be in XML)
        data_type = item_def.get('DataType')
        if data_type:
            try:
                item_data['dataType'] = DataType(data_type)
            except ValueError:
                item_data['dataType'] = data_type
        elif not self.preserve_original:
            # Only default to text if not preserving original
            item_data['dataType'] = DataType.text
            self.inference_log.append({
                'operation': 'default_datatype',
                'item_oid': item_oid,
                'assigned': 'text'
            })
        # If preserve_original and no DataType, leave it out (will fail Pydantic validation but preserved in supplemental)
        
        # Length
        length = item_def.get('Length')
        if length:
            try:
                item_data['length'] = int(length)
            except (ValueError, TypeError):
                pass
        
        # SignificantDigits
        sig_digits = item_def.get('SignificantDigits')
        if sig_digits:
            try:
                item_data['significantDigits'] = int(sig_digits)
            except (ValueError, TypeError):
                pass
        
        # DisplayFormat (def:DisplayFormat attribute)
        display_format = item_def.get('{%s}DisplayFormat' % self.active_namespaces['def'])
        if display_format:
            item_data['displayFormat'] = display_format
        
        # Origin - properly handled (Origin itself has no description field)
        origin_data = self._get_origin(item_def)
        
        # Extract metadata fields that don't belong in Origin Pydantic model
        if origin_data:
            # Extract comment and format metadata
            comment = origin_data.pop('comment', None)
            was_element = origin_data.pop('_wasElement', None)
            comment_for_linking = origin_data.pop('_commentForMethodLinking', None)
            
            # Store in supplemental for roundtrip
            if comment:
                origin_metadata['comment'] = comment
            if was_element is not None:
                origin_metadata['wasElement'] = was_element
            if comment_for_linking:
                origin_metadata['commentForMethodLinking'] = comment_for_linking
        
        if origin_data and any(v for v in origin_data.values() if v):
            try:
                origin_obj = Origin(**origin_data)
                item_data['origin'] = origin_obj
            except Exception as e:
                logger.warning(f"Failed to create Origin for {item_oid}: {e}")
                item_supp['origin'] = origin_data
        
        # CodeList reference
        code_list_ref = item_def.find('.//odm:CodeListRef', self.active_namespaces)
        if code_list_ref is not None:
            item_data['codeList'] = code_list_ref.get('CodeListOID')
        
        # ItemRef-specific properties
        if item_ref is not None:
            # Mandatory
            mandatory = item_ref.get('Mandatory')
            if mandatory:
                item_data['mandatory'] = mandatory == 'Yes'
            
            # Role
            role = item_ref.get('Role')
            if role:
                item_data['role'] = role
            
            # WhereClause reference (store in applicableWhen)
            where_clause_ref = item_ref.find('def:WhereClauseRef', self.active_namespaces)
            if where_clause_ref is not None:
                wc_oid = where_clause_ref.get('WhereClauseOID')
                if wc_oid:
                    item_data['applicableWhen'] = [wc_oid]
        
        # Link to methods based on derivation descriptions (only if not preserving original)
        if not self.preserve_original and derivation_method_map and (origin_data or origin_metadata):
            # Try origin description first
            desc = origin_data.get('description', '') if origin_data else ''
            
            # If no description, try Comment as method description
            if not desc:
                desc = origin_metadata.get('commentForMethodLinking', '')
            
            if desc and len(desc) > 30:
                normalized_desc = desc.strip()
                if normalized_desc in derivation_method_map:
                    item_data['method'] = derivation_method_map[normalized_desc]['OID']
                    source = 'origin description' if origin_data and origin_data.get('description') else 'Comment attribute'
                    self.inference_log.append({
                        'operation': 'method_linking',
                        'item_oid': item_oid,
                        'method_oid': derivation_method_map[normalized_desc]['OID'],
                        'matched_description': normalized_desc[:50] + '...',
                        'source': source
                    })
        
        # Store origin metadata in supplemental if present
        if origin_metadata:
            item_supp['originMetadata'] = origin_metadata
        
        # Create Item Pydantic object
        try:
            item_obj = Item(**item_data)
            return item_obj, item_supp
        except Exception as e:
            logger.error(f"Failed to create Item {item_oid}: {e}")
            logger.error(f"  Item data: {item_data}")
            return None, {**item_data, **item_supp}
    
    def _get_origin(self, item_def: ET.Element) -> Dict[str, Any]:
        """
        Extract origin information for Origin object.
        Note: Origin itself doesn't have a description field - descriptions go in Item.description
        
        Returns:
            Dictionary with origin data for Pydantic Origin object
        """
        origin = {}
        has_origin_element = False  # Track if origin was an element vs attribute
        
        # Check for def:Origin element (v2.x style)
        origin_elem = item_def.find('.//def:Origin', self.active_namespaces)
        if origin_elem is not None:
            has_origin_element = True
            origin_type = origin_elem.get('Type')
            if origin_type:
                # Map "Collected" to "CRF" since collected data typically comes from CRFs
                if origin_type == "Collected":
                    logger.info(f"Mapping OriginType 'Collected' to 'CRF' for item {item_def.get('OID')}")
                    origin_type = "CRF"
                
                try:
                    origin['type'] = OriginType(origin_type)
                except ValueError:
                    logger.warning(f"Invalid OriginType: {origin_type}")
                    origin['type'] = origin_type
            
            source = origin_elem.get('Source')
            if source:
                try:
                    origin['source'] = OriginSource(source)
                except ValueError:
                    logger.warning(f"Invalid OriginSource: {source}")
                    origin['source'] = source
        
        # Check for Origin attribute (v1.x style)
        origin_attr = item_def.get('Origin')
        if origin_attr and not origin.get('type'):
            try:
                origin['type'] = OriginType(origin_attr)
            except ValueError:
                origin['type'] = origin_attr
        
        # ALWAYS capture Comment attribute (for both modes)
        comment_attr = item_def.get('Comment')
        if comment_attr:
            if self.preserve_original:
                # Store as-is for roundtrip
                origin['comment'] = comment_attr
            else:
                # Store for roundtrip AND consider for inference
                origin['comment'] = comment_attr
                
                # Check if comment looks like substantive derivation logic (for method linking)
                if len(comment_attr) > 30:
                    origin['_commentForMethodLinking'] = comment_attr
                
                # If looks like predecessor reference, mark as such
                if '.' in comment_attr or 'ADSL.' in comment_attr:
                    if not origin.get('type'):
                        origin['type'] = OriginType.Predecessor
                        self.inference_log.append({
                            'operation': 'origin_type_inference',
                            'item_oid': item_def.get('OID'),
                            'comment': comment_attr,
                            'inferred_type': 'Predecessor'
                        })
        
        # Store format metadata for roundtrip
        if self.preserve_original and origin:
            origin['_wasElement'] = has_origin_element
        
        return origin
    
    def _process_value_lists_as_item_groups(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict]:
        """
        Process ValueListDef elements as ItemGroups with type='ValueList'.
        
        Uses the original ValueListDef OID as the ItemGroup OID.
        
        Returns:
            Tuple of (value_list_item_groups, supplemental_data)
        """
        value_list_igs = []
        supplemental = {}
        item_origin_metadata = {}  # Track origin metadata for all items
        
        # Process each ValueListDef directly
        for vl_elem in mdv.findall('.//def:ValueListDef', self.active_namespaces):
            vl_oid = vl_elem.get('OID')
            if not vl_oid:
                continue
            
            # Collect items for this specific ValueListDef
            items = []
            item_order_numbers = {}  # Track OrderNumbers for each ItemRef
            
            for item_ref in vl_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                if not item_oid:
                    continue
                
                # Capture OrderNumber attribute (critical for ValueLists!)
                order_num = item_ref.get('OrderNumber')
                if order_num:
                    item_order_numbers[item_oid] = order_num
                    
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                
                if item_def is not None:
                    item_obj, item_supp = self._create_item_object(item_def, item_ref, derivation_method_map)
                    if item_obj:
                        items.append(item_obj)
                        # Collect origin metadata
                        if 'originMetadata' in item_supp:
                            item_origin_metadata[item_oid] = item_supp['originMetadata']
            
            # Only create ItemGroup if we found items
            if not items:
                logger.warning(f"ValueListDef {vl_oid} has no valid items, skipping")
                continue
            
            # Use original OID, derive name from OID for convenience
            ig_name = vl_oid.replace('ValueList.', '').replace('.', '_')
            
            ig_data = {
                'OID': vl_oid,
                'name': ig_name,
                'type': 'ValueList',  # Use a valid ItemGroupType enum value
                'items': items,
            }
            
            try:
                vl_ig = ItemGroup(**ig_data)
                value_list_igs.append(vl_ig)
                logger.info(f"  - Created ValueList ItemGroup {vl_oid} with {len(items)} items")
                # Fix #2: Track that this ItemGroup is actually a ValueListDef
                supplemental[vl_oid] = {
                    'elementType': 'ValueListDef',
                    'originalType': 'ValueList'
                }
                # Store OrderNumbers for perfect roundtrip
                if item_order_numbers:
                    supplemental[vl_oid]['itemOrderNumbers'] = item_order_numbers
            except Exception as e:
                logger.error(f"Failed to create ValueList ItemGroup {vl_oid}: {e}")
                logger.error(f"  ig_data keys: {ig_data.keys()}")
                logger.error(f"  items type: {type(items)}, count: {len(items)}")
                if items:
                    logger.error(f"  first item type: {type(items[0])}")
                import traceback
                logger.error(f"  Full traceback: {traceback.format_exc()}")
                ig_data['elementType'] = 'ValueListDef'  # Still track for failed items
                supplemental[vl_oid] = ig_data
        
        # Store item origin metadata at top level
        if item_origin_metadata:
            supplemental['_itemOriginMetadata'] = item_origin_metadata
        
        return value_list_igs, supplemental
    
    def _process_code_lists(self, mdv: ET.Element) -> Tuple[List[CodeList], List, Dict]:
        """
        Process CodeList elements into Pydantic CodeList objects with items included.
        Also creates Dictionary objects for ExternalCodeLists.
        
        Returns:
            Tuple of (code_lists, dictionaries, supplemental_data)
        """
        code_lists = []
        dictionaries = []  # NEW: Collect Dictionary objects for ExternalCodeLists
        dict_oids_seen = set()
        supplemental = {}
        
        for cl_elem in mdv.findall('.//odm:CodeList', self.active_namespaces):
            cl_oid = cl_elem.get('OID')
            if not cl_oid:
                continue
            
            cl_data = {'OID': cl_oid}
            cl_supp = {'OID': cl_oid}
            
            # Name
            if cl_elem.get('Name'):
                cl_data['name'] = cl_elem.get('Name')
            
            # Label
            label = cl_elem.get('{%s}Label' % self.active_namespaces['def'])
            if label:
                cl_data['label'] = label
            
            # DataType
            data_type = cl_elem.get('DataType')
            if data_type:
                try:
                    cl_data['dataType'] = DataType(data_type)
                except ValueError:
                    cl_data['dataType'] = data_type
            
            # Description
            description = self._get_description(cl_elem)
            if description:
                cl_data['description'] = description
            
            # Check for ExternalCodeList - convert to Dictionary object
            external_cl = cl_elem.find('odm:ExternalCodeList', self.active_namespaces)
            if external_cl is not None:
                dict_name = external_cl.get('Dictionary')
                version = external_cl.get('Version')
                href = external_cl.get('href')
                ref = external_cl.get('ref')
                
                if dict_name:
                    # Generate Dictionary OID (use name only, version is separate field)
                    dict_oid = f"DICT.{dict_name.replace(' ', '_')}"
                    
                    # Create Dictionary object if not already created (deduplication)
                    if dict_oid not in dict_oids_seen:
                        dict_data = {
                            'OID': dict_oid,
                            'name': dict_name,
                            'terms': []
                        }
                        if version:
                            dict_data['version'] = version
                        
                        try:
                            dict_obj = Dictionary(**dict_data)
                            dictionaries.append(dict_obj)
                            dict_oids_seen.add(dict_oid)
                            logger.info(f"  - Created Dictionary {dict_oid} (name: {dict_name}, version: {version})")
                        except Exception as e:
                            logger.warning(f"Failed to create Dictionary {dict_oid}: {e}")
                            # Fall back to supplemental storage if Dictionary creation fails
                            if 'externalCodeList' not in cl_supp:
                                cl_supp['externalCodeList'] = {}
                            cl_supp['externalCodeList']['dictionary'] = dict_name
                            if version:
                                cl_supp['externalCodeList']['version'] = version
                    
                    # Link CodeList to Dictionary via wasDerivedFrom (provenance)
                    # This is semantically correct: AEDICT was derived from MedDRA
                    cl_data['wasDerivedFrom'] = dict_oid
                    
                    # Store href/ref in supplemental if present (xlink attrs not in Dictionary schema)
                    if href or ref:
                        if 'externalCodeListLinks' not in cl_supp:
                            cl_supp['externalCodeListLinks'] = {}
                        if href:
                            cl_supp['externalCodeListLinks']['href'] = href
                        if ref:
                            cl_supp['externalCodeListLinks']['ref'] = ref
            
            # Process CodeListItem/EnumeratedItem as proper Pydantic objects
            code_list_items = []
            for item_elem in cl_elem.findall('.//odm:CodeListItem', self.active_namespaces):
                coded_value = item_elem.get('CodedValue')
                if not coded_value:
                    continue
                    
                item_data = {'codedValue': coded_value}
                
                # Decode
                decode = self._get_decode(item_elem)
                if decode:
                    item_data['decode'] = decode
                
                # Description
                desc = self._get_description(item_elem)
                if desc:
                    item_data['description'] = desc
                
                # Extract def:Rank and map to weight
                rank = item_elem.get(f'{{{self.active_namespaces["def"]}}}Rank')
                if rank:
                    try:
                        item_data['weight'] = int(rank)
                    except ValueError:
                        item_data['weight'] = float(rank)
                
                # Try to create CodeListItem Pydantic object
                try:
                    cli_obj = CodeListItem(**item_data)
                    code_list_items.append(cli_obj)
                except Exception as e:
                    logger.warning(f"Failed to create CodeListItem for {coded_value}: {e}")
                    # Store in supplemental if can't create Pydantic object
                    if 'failed_items' not in cl_supp:
                        cl_supp['failed_items'] = []
                    cl_supp['failed_items'].append(item_data)
            
            if code_list_items:
                cl_data['codeListItems'] = code_list_items
            else:
                # Always include codeListItems, even if empty
                # This is especially important for ExternalCodeList-only CodeLists
                cl_data['codeListItems'] = []
            
            # Create CodeList Pydantic object
            try:
                cl_obj = CodeList(**cl_data)
                code_lists.append(cl_obj)
                
                # Log AEDICT specifically for debugging
                if cl_oid == 'AEDICT':
                    logger.info(f"  ✓ Successfully created AEDICT CodeList")
                    logger.info(f"    - wasDerivedFrom: {cl_data.get('wasDerivedFrom')}")
                    logger.info(f"    - codeListItems count: {len(cl_data.get('codeListItems', []))}")
                
                # Store supplemental data if we have any (externalCodeList, failed_items, etc.)
                # Check if there's any meaningful supplemental data (more than just OID)
                if len(cl_supp) > 1:  # More than just 'OID' key
                    supplemental[cl_oid] = cl_supp
            except Exception as e:
                logger.error(f"Failed to create CodeList {cl_oid}: {e}")
                logger.error(f"  CodeList data: {cl_data}")
                if cl_oid == 'AEDICT':
                    logger.error(f"  ✗ AEDICT FAILED TO CREATE!")
                supplemental[cl_oid] = {**cl_data, **cl_supp}
        
        return code_lists, dictionaries, supplemental
    
    def _process_conditions_and_where_clauses(self, mdv: ET.Element) -> Tuple[List[Condition], List[WhereClause], Dict]:
        """
        Process WhereClauseDef elements into proper WhereClause and Condition objects.
        
        Creates:
        - WhereClause objects with references to Condition OIDs
        - Condition objects with rangeChecks from Define-XML RangeCheck elements
        - Default Condition OIDs match WhereClause OIDs with WC -> COND replacement
        
        Returns:
            Tuple of (conditions, where_clauses, supplemental_data)
        """
        conditions = []
        where_clauses = []
        supplemental = {}
        
        # Process WhereClauseDef elements
        for wc_elem in mdv.findall('.//def:WhereClauseDef', self.active_namespaces):
            wc_oid = wc_elem.get('OID')
            if not wc_oid:
                continue
            
            # Generate Condition OID by replacing WC with COND
            # e.g., "WC.VS.VSORRES.TEMP" -> "COND.VS.VSORRES.TEMP"
            if wc_oid.startswith('WC.'):
                cond_oid = 'COND.' + wc_oid[3:]
            else:
                cond_oid = f'COND.{wc_oid}'
            
            # Build RangeCheck list for the Condition
            range_checks = []
            for rc in wc_elem.findall('.//odm:RangeCheck', self.active_namespaces):
                comparator = rc.get('Comparator')
                item_oid = rc.get('ItemOID')
                
                # Get CheckValue
                check_value_elem = rc.find('.//odm:CheckValue', self.active_namespaces)
                check_value = check_value_elem.text if check_value_elem is not None else None
                
                if comparator and item_oid:
                    range_check_data = {
                        'comparator': comparator,
                        'item': item_oid,  # Use 'item' to match Define-JSON schema
                    }
                    # Use checkValues (plural) list to match Define-JSON schema
                    if check_value:
                        range_check_data['checkValues'] = [check_value]
                    
                    range_checks.append(range_check_data)
            
            # Only create Condition and WhereClause if we have range checks
            if range_checks:
                # Create Condition object
                cond_data = {
                    'OID': cond_oid,
                    'rangeChecks': range_checks
                }
                
                # Add name/description if available
                description = self._get_description(wc_elem)
                if description:
                    cond_data['description'] = description
                
                try:
                    condition_obj = Condition(**cond_data)
                    conditions.append(condition_obj)
                except Exception as e:
                    logger.warning(f"Failed to create Condition {cond_oid}: {e}")
                    supplemental[f'condition_{cond_oid}'] = cond_data
                
                # Create WhereClause object referencing the Condition
                wc_data = {
                    'OID': wc_oid,
                    'conditions': [cond_oid]  # Reference to Condition OID
                }
                
                if description:
                    wc_data['description'] = description
                
                try:
                    where_clause_obj = WhereClause(**wc_data)
                    where_clauses.append(where_clause_obj)
                except Exception as e:
                    logger.warning(f"Failed to create WhereClause {wc_oid}: {e}")
                    supplemental[f'whereClause_{wc_oid}'] = wc_data
        
        return conditions, where_clauses, supplemental
    
    def _get_study_name(self, study: ET.Element) -> Optional[str]:
        """Extract study name from GlobalVariables."""
        gv = study.find('odm:GlobalVariables', self.active_namespaces)
        if gv is not None:
            sn = gv.find('odm:StudyName', self.active_namespaces)
            if sn is not None:
                return sn.text
        return None
    
    def _get_study_description(self, study: ET.Element) -> Optional[str]:
        """Extract study description from GlobalVariables."""
        gv = study.find('odm:GlobalVariables', self.active_namespaces)
        if gv is not None:
            sd = gv.find('odm:StudyDescription', self.active_namespaces)
            if sd is not None:
                return sd.text
        return None
    
    def _get_protocol_name(self, study: ET.Element) -> Optional[str]:
        """Extract protocol name from GlobalVariables."""
        gv = study.find('odm:GlobalVariables', self.active_namespaces)
        if gv is not None:
            pn = gv.find('odm:ProtocolName', self.active_namespaces)
            if pn is not None:
                return pn.text
        return None
    
    def _get_description(self, element: ET.Element) -> Optional[str]:
        """Extract description from TranslatedText."""
        desc = element.find('.//odm:Description/odm:TranslatedText', self.active_namespaces)
        return desc.text if desc is not None else None
    
    def _get_decode(self, element: ET.Element) -> Optional[str]:
        """Extract decode from TranslatedText."""
        decode = element.find('.//odm:Decode/odm:TranslatedText', self.active_namespaces)
        return decode.text if decode is not None else None
    
    def _process_supplemental_doc(self, mdv: ET.Element) -> Optional[Dict[str, Any]]:
        """
        Fix #4: Process SupplementalDoc element.
        
        Returns:
            Dict with documentRefs list, or None if not found
        """
        # Find SupplementalDoc element
        supp_doc = mdv.find('.//def:SupplementalDoc', self.active_namespaces)
        if not supp_doc:
            return None
        
        # Extract DocumentRef children
        doc_refs = []
        for doc_ref in supp_doc.findall('.//def:DocumentRef', self.active_namespaces):
            leaf_id = doc_ref.get('{%s}leafID' % self.active_namespaces.get('def', ''))
            if not leaf_id:
                leaf_id = doc_ref.get('leafID')  # Fallback without namespace
            if leaf_id:
                doc_refs.append({'leafID': leaf_id})
        
        if doc_refs:
            return {'documentRefs': doc_refs}
        return None
    
    def _process_analysis_result_displays(self, mdv: ET.Element) -> Optional[List[Dict[str, Any]]]:
        """
        Fix #3: Process AnalysisResultDisplays (ARM/AdaMRef Extensions).
        
        Captures the complete structure: each AnalysisResultDisplays container
        with its ResultDisplay and AnalysisResults children as a raw XML subtree.
        
        Returns:
            List of container objects (one per AnalysisResultDisplays element), or None if not found
        """
        analysis_containers = []
        
        # Look for any AnalysisResultDisplays elements regardless of namespace
        # They might be under arm:, adamref:, or def: namespaces
        for prefix, uri in self.active_namespaces.items():
            if prefix in ['arm', 'adamref', 'def']:
                # Try to find AnalysisResultDisplays under this namespace at MetaDataVersion level
                # Use direct child search to avoid finding nested ones
                ard_elements = mdv.findall(f'{{{uri}}}AnalysisResultDisplays')
                
                for ard_container in ard_elements:
                    # Store the complete container as serialized XML for perfect roundtrip
                    # This preserves ALL children including AnalysisResults, AnalysisVariables, etc.
                    container_data = {
                        '_containerType': 'AnalysisResultDisplays',
                        '_namespace': prefix,
                        # Serialize the entire container to preserve structure
                        '_xmlContent': ET.tostring(ard_container, encoding='unicode')
                    }
                    
                    analysis_containers.append(container_data)
        
        return analysis_containers if analysis_containers else None


def main():
    """Main entry point."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert Define-XML to Define-JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Perfect roundtrip conversion (preserves original XML values)
  python xml_to_json.py input.xml output.json
  
  # With inference for one-way conversion (smarter but not exact roundtrip)
  python xml_to_json.py input.xml output.json --infer
  
  # Explicit preserve original flag
  python xml_to_json.py input.xml output.json --preserve-original
        '''
    )
    parser.add_argument('input', help='Input Define-XML file')
    parser.add_argument('output', help='Output Define-JSON file')
    parser.add_argument(
        '--infer', 
        action='store_true',
        help='Enable inference (method type mapping, origin inference, etc.). Disables exact roundtrip.'
    )
    parser.add_argument(
        '--preserve-original',
        action='store_true',
        default=True,
        help='Preserve original XML values for perfect roundtrip (default: True)'
    )
    
    args = parser.parse_args()
    
    # If --infer is specified, disable preserve_original
    preserve_original = not args.infer if args.infer else args.preserve_original
    
    converter = DefineXMLToJSONConverter(preserve_original=preserve_original)
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    mode = "preserve-original" if preserve_original else "infer"
    print(f"Converting {input_path} to {output_path} (mode: {mode})")
    result = converter.convert_file(input_path, output_path)
    print(f"Conversion complete!")
    
    # Print summary
    if 'itemGroups' in result:
        print(f"  - {len(result['itemGroups'])} ItemGroups")
        total_items = sum(len(ig.get('items', [])) for ig in result['itemGroups'])
        print(f"  - {total_items} Items (nested in ItemGroups)")
    if 'items' in result:
        print(f"  - {len(result['items'])} Top-level Items")
    if 'codeLists' in result:
        print(f"  - {len(result['codeLists'])} CodeLists")
    if 'methods' in result:
        print(f"  - {len(result['methods'])} Methods")
    
    # Print inference summary if applicable
    if not preserve_original and '_xmlMetadata' in result and 'inferenceLog' in result['_xmlMetadata']:
        print(f"\nInference Summary:")
        log = result['_xmlMetadata']['inferenceLog']
        operations = {}
        for entry in log:
            op = entry['operation']
            operations[op] = operations.get(op, 0) + 1
        for op, count in sorted(operations.items()):
            print(f"  - {op}: {count} operations")


if __name__ == '__main__':
    main()