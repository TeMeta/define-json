"""
Improved Define-XML to Define-JSON converter with proper Pydantic validation.

Key improvements:
1. Uses Comment structure for extra data (like origin descriptions) instead of forbidden fields
2. Maintains structured hierarchy with Items nested in ItemGroups
3. Graceful error handling with data preservation in supplemental structures
4. Full Pydantic validation throughout
5. Matches the structure from xml_to_json_structured.py output
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
    - Method linking based on derivation descriptions
    - Origin information properly structured with comments
    - Full Pydantic validation throughout
    - Graceful error handling with data preservation
    - XML metadata preserved for roundtrip conversion
    """
    
    def __init__(self):
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
        
    def _detect_namespaces(self, root: ET.Element) -> Dict[str, str]:
        """Auto-detect namespace version from XML root."""
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
        logger.info(f"Starting conversion of {xml_path}")
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Auto-detect and use appropriate namespaces
        self.active_namespaces = self._detect_namespaces(root)
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
        
        # Create Standard object if standardName and standardVersion exist
        standard_name = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
        standard_version = mdv.get('{%s}StandardVersion' % self.active_namespaces['def'])
        
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
                except Exception as e:
                    logger.warning(f"Failed to create Standard object: {e}")
                    xml_metadata['standardName'] = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
                    xml_metadata['standardVersion'] = standard_version
            elif standard_version:
                # Have version but no valid name
                xml_metadata['standardVersion'] = standard_version
        
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
        code_lists, cl_supplemental = self._process_code_lists(mdv)
        if code_lists:
            mdv_data['codeLists'] = code_lists
            logger.info(f"  - Created {len(code_lists)} code lists")
        
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
            logger.info("âœ“ Pydantic validation successful")
        except Exception as e:
            logger.error(f"âœ— Failed to create MetaDataVersion model: {e}")
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
        
        result['_xmlMetadata'] = xml_metadata
        
        # Save to file
        logger.info(f"Writing output to {output_path}")
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        logger.info("âœ“ Conversion complete!")
        return result
    
    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not dt_str:
            return None
        try:
            # Handle ISO format with T separator
            if 'T' in dt_str:
                # Remove timezone info if present for simplicity
                dt_str = dt_str.split('+')[0].split('-')[0] if '+' in dt_str or dt_str.count('-') > 2 else dt_str
                return datetime.fromisoformat(dt_str.replace('T', ' '))
            return datetime.fromisoformat(dt_str)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse datetime '{dt_str}': {e}")
            return None
    
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
            
            # Get type with smart mapping for common Define-XML types
            method_type = method_elem.get('Type')
            if method_type:
                # Map common Define-XML types to valid MethodType enum values
                type_mapping = {
                    'Derivation': 'Computation',  # Derivation is effectively computation
                    'Assigned': 'Computation',
                    'Algorithm': 'Computation',
                }
                mapped_type = type_mapping.get(method_type, method_type)
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
            except Exception as e:
                logger.warning(f"Failed to create Method {method_oid}: {e}")
                supplemental[method_oid] = method_data
        
        # Process ComputationMethod elements (Define-XML v1.x style)
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
            except Exception as e:
                logger.warning(f"Failed to create Method {method_oid}: {e}")
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
        supplemental.update(domain_supp)
        
        # Process ValueLists as ItemGroups with type="ValueList"
        value_list_igs, vl_supp = self._process_value_lists_as_item_groups(mdv, derivation_method_map)
        item_groups.extend(value_list_igs)
        supplemental.update(vl_supp)
        
        logger.info(f"  - Found {len(value_list_igs)} ValueList ItemGroups")
        
        # Build map of ValueListOID -> parent ItemGroup OID
        # ONLY use explicit def:ValueListRef or def:ValueListOID attributes
        # No inference - for perfect roundtrip conversion
        valuelist_to_parent = {}
        
        # Check for explicit def:ValueListRef attributes on ItemRef or ItemDef
        for ig_elem in mdv.findall('.//odm:ItemGroupDef', self.active_namespaces):
            ig_oid = ig_elem.get('OID')
            
            for item_ref in ig_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                
                # Check ItemRef for ValueList reference
                vl_ref = item_ref.get('{%s}ValueListRef' % self.active_namespaces['def'])
                if not vl_ref:
                    vl_ref = item_ref.get('{%s}ValueListOID' % self.active_namespaces['def'])
                
                if vl_ref:
                    valuelist_to_parent[vl_ref] = ig_oid
                    logger.info(f"    - ItemRef {item_oid} explicitly references ValueList {vl_ref}, parent is {ig_oid}")
                    continue
                
                # Also check the ItemDef itself
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                if item_def is not None:
                    vl_ref = item_def.get('{%s}ValueListOID' % self.active_namespaces['def'])
                    if not vl_ref:
                        vl_ref = item_def.get('{%s}ValueListRef' % self.active_namespaces['def'])
                    
                    if vl_ref:
                        valuelist_to_parent[vl_ref] = ig_oid
                        logger.info(f"    - ItemDef {item_oid} explicitly references ValueList {vl_ref}, parent is {ig_oid}")
        
        # Add ValueList OIDs as children to their parent domains
        children_added = 0
        for vl_ig in value_list_igs:
            parent_oid = valuelist_to_parent.get(vl_ig.OID)
            if parent_oid:
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
        
        return item_groups, supplemental
    
    def _process_domain_item_groups(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict]:
        """Process domain-level ItemGroupDef elements as Pydantic ItemGroup objects."""
        item_groups = []
        supplemental = {}
        
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
            
            # Class -> map to purpose
            class_attr = ig_elem.get('{%s}Class' % self.active_namespaces['def'])
            if class_attr:
                ig_data['purpose'] = class_attr
            
            # Repeating (store in supplemental as string for roundtrip)
            repeating = ig_elem.get('Repeating')
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
            
            # Process ItemRefs - create full Item objects nested in items list
            items = []
            for item_ref in ig_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                
                if item_def is not None:
                    item_obj, item_supp = self._create_item_object(item_def, item_ref, derivation_method_map)
                    if item_obj:
                        items.append(item_obj)
            
            if items:
                ig_data['items'] = items
            
            # Create ItemGroup Pydantic object
            try:
                ig_obj = ItemGroup(**ig_data)
                item_groups.append(ig_obj)
                supplemental[ig_oid] = ig_supp
            except Exception as e:
                logger.error(f"Failed to create ItemGroup {ig_oid}: {e}")
                supplemental[ig_oid] = {**ig_data, **ig_supp}
        
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
        
        # DataType (required)
        data_type = item_def.get('DataType')
        if data_type:
            try:
                item_data['dataType'] = DataType(data_type)
            except ValueError:
                item_data['dataType'] = data_type
        else:
            # Default to text if not specified
            item_data['dataType'] = DataType.text
        
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
        
        # Origin - properly handled (Origin itself has no description field)
        origin_data = self._get_origin(item_def)
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
        
        # Link to methods based on derivation descriptions
        if derivation_method_map and origin_data:
            desc = origin_data.get('description', '')
            if desc and len(desc) > 30:
                normalized_desc = desc.strip()
                if normalized_desc in derivation_method_map:
                    item_data['method'] = derivation_method_map[normalized_desc]['OID']
        
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
        
        # Check for def:Origin element (v2.x style)
        origin_elem = item_def.find('.//def:Origin', self.active_namespaces)
        if origin_elem is not None:
            origin_type = origin_elem.get('Type')
            if origin_type:
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
        
        # Check for Comment attribute (predecessor info in Define-XML v1.0)
        comment_attr = item_def.get('Comment')
        if comment_attr:
            # If looks like predecessor, mark as such
            if '.' in comment_attr or 'ADSL.' in comment_attr:
                if not origin.get('type'):
                    origin['type'] = OriginType.Predecessor
        
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
        
        # Process each ValueListDef directly
        for vl_elem in mdv.findall('.//def:ValueListDef', self.active_namespaces):
            vl_oid = vl_elem.get('OID')
            if not vl_oid:
                continue
            
            # Collect items for this specific ValueListDef
            items = []
            
            for item_ref in vl_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                if not item_oid:
                    continue
                    
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                
                if item_def is not None:
                    item_obj, item_supp = self._create_item_object(item_def, item_ref, derivation_method_map)
                    if item_obj:
                        items.append(item_obj)
            
            # Only create ItemGroup if we found items
            if not items:
                logger.warning(f"ValueListDef {vl_oid} has no valid items, skipping")
                continue
            
            # Use original OID, derive name from OID for convenience
            ig_name = vl_oid.replace('ValueList.', '').replace('.', '_')
            
            ig_data = {
                'OID': vl_oid,
                'name': ig_name,
                'type': 'ValueList',  # ValueLists have their own type
                'items': items,
            }
            
            try:
                vl_ig = ItemGroup(**ig_data)
                value_list_igs.append(vl_ig)
                logger.info(f"  - Created ValueList ItemGroup {vl_oid} with {len(items)} items")
            except Exception as e:
                logger.error(f"Failed to create ValueList ItemGroup {vl_oid}: {e}")
                logger.error(f"  ig_data keys: {ig_data.keys()}")
                logger.error(f"  items type: {type(items)}, count: {len(items)}")
                if items:
                    logger.error(f"  first item type: {type(items[0])}")
                import traceback
                logger.error(f"  Full traceback: {traceback.format_exc()}")
                supplemental[vl_oid] = ig_data
        
        return value_list_igs, supplemental
    
    def _process_code_lists(self, mdv: ET.Element) -> Tuple[List[CodeList], Dict]:
        """
        Process CodeList elements into Pydantic CodeList objects with items included.
        
        Returns:
            Tuple of (code_lists, supplemental_data)
        """
        code_lists = []
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
            
            # Create CodeList Pydantic object
            try:
                cl_obj = CodeList(**cl_data)
                code_lists.append(cl_obj)
                if cl_supp.get('failed_items'):
                    supplemental[cl_oid] = cl_supp
            except Exception as e:
                logger.error(f"Failed to create CodeList {cl_oid}: {e}")
                supplemental[cl_oid] = {**cl_data, **cl_supp}
        
        return code_lists, supplemental
    
    def _process_conditions_and_where_clauses(self, mdv: ET.Element) -> Tuple[List[Condition], List[WhereClause], Dict]:
        """
        Process WhereClauseDef elements.
        
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
            
            wc_data = {'OID': wc_oid}
            wc_supp = {'OID': wc_oid}
            
            # Process RangeCheck elements as conditions
            range_checks = wc_elem.findall('.//odm:RangeCheck', self.active_namespaces)
            wc_conditions = []
            
            for rc in range_checks:
                comparator = rc.get('Comparator')
                item_oid = rc.get('ItemOID')
                
                # Get CheckValue
                check_value_elem = rc.find('.//odm:CheckValue', self.active_namespaces)
                check_value = check_value_elem.text if check_value_elem is not None else None
                
                if comparator and item_oid:
                    wc_conditions.append({
                        'comparator': comparator,
                        'itemOID': item_oid,
                        'checkValue': check_value
                    })
            
            if wc_conditions:
                wc_supp['conditions'] = wc_conditions
            
            # Store as supplemental for now
            supplemental[wc_oid] = wc_supp
        
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


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python xml_to_json_improved.py <input.xml> <output.json>")
        sys.exit(1)
    
    converter = DefineXMLToJSONConverter()
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    print(f"Converting {input_path} to {output_path}")
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


if __name__ == '__main__':
    main()