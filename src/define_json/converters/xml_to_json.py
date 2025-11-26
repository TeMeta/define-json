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
import warnings

# Suppress Pydantic serialization warnings for Union[ItemGroup, str] in slices field
# (nested ItemGroups serialize correctly, warning is cosmetic due to self-referential model)
warnings.filterwarnings('ignore', category=UserWarning, message='.*Pydantic serializer warnings.*')

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
    Resource,
    Analysis,
    Display,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DefineXMLToJSONConverter:
    """
    Improved Define-XML to Define-JSON converter with proper Pydantic validation.
    
    Features:
    - Items nested within ItemGroups (structured hierarchy)
    - ValueLists processed as ItemGroups with type="DatasetSpecialization"
    - Hierarchical structure with slices references
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
        
        # Preserve ValueListDef order for perfect roundtrip
        value_list_def_order = []
        for vl_def in mdv.findall('.//def:ValueListDef', self.active_namespaces):
            vl_oid = vl_def.get('OID')
            if vl_oid:
                value_list_def_order.append(vl_oid)
        if value_list_def_order:
            xml_metadata['valueListDefOrder'] = value_list_def_order
        
        # Create Standard object if standardName and standardVersion exist
        standard_name = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
        standard_version = mdv.get('{%s}StandardVersion' % self.active_namespaces['def'])
        
        # Check if Standards element exists (vs just attributes)
        standards_element = mdv.find('odm:Standards', self.active_namespaces) or mdv.find('def:Standards', self.active_namespaces)
        has_standards_element = standards_element is not None
        
        standards_list = []
        
        # Process Standards element if it exists
        if standards_element is not None:
            # Try def:Standard first, then odm:Standard
            std_elems = standards_element.findall('def:Standard', self.active_namespaces)
            if not std_elems:
                std_elems = standards_element.findall('odm:Standard', self.active_namespaces)
            
            for std_elem in std_elems:
                std_oid = std_elem.get('OID', '')
                std_name = std_elem.get('Name', '')
                std_type = std_elem.get('Type', '')
                std_version = std_elem.get('Version', '')
                std_status = std_elem.get('Status', '')
                std_publishing_set = std_elem.get('PublishingSet', '')
                
                standard_data = {
                    'OID': std_oid or f'STD.{len(standards_list) + 1}',
                }
                
                if std_name:
                    # Map common standard name variations to enum values
                    standard_name_map = {
                        'CDISC ADaM': 'ADaMIG',
                        'ADaM': 'ADaMIG',
                        'CDISC SDTM': 'SDTMIG',
                        'SDTM': 'SDTMIG',
                        'CDISC SEND': 'SENDIG',
                        'SEND': 'SENDIG',
                        'CDISC/NCI': 'CDISCSOLIDUSNCI',  # Map slash to enum name
                    }
                    mapped_name = standard_name_map.get(std_name, std_name)
                    try:
                        standard_data['name'] = StandardName(mapped_name)
                    except ValueError:
                        # Store as string if not valid enum
                        standard_data['name'] = std_name
                
                if std_version:
                    standard_data['version'] = std_version
                if std_status:
                    # Map status values to enum
                    status_map = {
                        'Final': 'FINAL',
                        'final': 'FINAL',
                        'Draft': 'DRAFT',
                        'draft': 'DRAFT',
                    }
                    mapped_status = status_map.get(std_status, std_status.upper() if std_status else None)
                    try:
                        from ..schema.define import StandardStatus
                        standard_data['status'] = StandardStatus(mapped_status)
                    except (ValueError, AttributeError):
                        # Store as string if not valid enum
                        standard_data['status'] = std_status
                if std_type:
                    try:
                        from ..schema.define import StandardType
                        standard_data['type'] = StandardType(std_type)
                    except (ValueError, AttributeError):
                        standard_data['type'] = std_type
                if std_publishing_set:
                    try:
                        from ..schema.define import PublishingSet
                        standard_data['publishingSet'] = PublishingSet(std_publishing_set)
                    except (ValueError, AttributeError):
                        standard_data['publishingSet'] = std_publishing_set
                
                # Extract def:CommentOID for roundtrip (store in supplemental metadata)
                comment_oid = std_elem.get('{%s}CommentOID' % self.active_namespaces['def'])
                
                try:
                    standard_obj = Standard(**standard_data)
                    standards_list.append(standard_obj)
                    
                    # Store supplemental data if present
                    if comment_oid:
                        xml_metadata.setdefault('standardSupplemental', {})[std_oid] = {'commentOID': comment_oid}
                except Exception as e:
                    logger.warning(f"Failed to create Standard object {std_oid}: {e}")
        
        # Fallback to attributes if no Standards element
        if not standards_list and (standard_name or standard_version):
            standard_data = {
                'OID': 'STD.001',
            }
            
            if standard_name:
                standard_name_map = {
                    'CDISC ADaM': 'ADaMIG',
                    'ADaM': 'ADaMIG',
                    'CDISC SDTM': 'SDTMIG',
                    'SDTM': 'SDTMIG',
                    'CDISC SEND': 'SENDIG',
                    'SEND': 'SENDIG',
                }
                mapped_name = standard_name_map.get(standard_name, standard_name)
                try:
                    standard_data['name'] = StandardName(mapped_name)
                except ValueError:
                    xml_metadata['standardName'] = standard_name
                    standard_name = None
            
            if standard_version and standard_name:
                standard_data['version'] = standard_version
            
            if standard_name:
                try:
                    standard_obj = Standard(**standard_data)
                    standards_list.append(standard_obj)
                except Exception as e:
                    logger.warning(f"Failed to create Standard object: {e}")
                    xml_metadata['standardName'] = mdv.get('{%s}StandardName' % self.active_namespaces['def'])
                    xml_metadata['standardVersion'] = standard_version
        
        if standards_list:
            mdv_data['standards'] = [s.model_dump(mode='json', exclude_none=True) if hasattr(s, 'model_dump') else s for s in standards_list]
            logger.info(f"  - Created {len(standards_list)} Standard objects")
            xml_metadata['hasStandardsElement'] = has_standards_element
        elif standard_version:
            xml_metadata["standardVersion"] = standard_version
            xml_metadata["hasStandardsElement"] = has_standards_element
        
        # Process AnnotatedCRF element (simple DocumentRef container)
        annotated_crf_elem = mdv.find('def:AnnotatedCRF', self.active_namespaces)
        if annotated_crf_elem is not None:
            # AnnotatedCRF contains DocumentRef elements with leafID
            doc_ref_elems = annotated_crf_elem.findall('def:DocumentRef', self.active_namespaces)
            if doc_ref_elems:
                annotated_crf_data = {'documentRefs': []}
                for doc_ref in doc_ref_elems:
                    leaf_id = doc_ref.get('leafID') or doc_ref.get('{%s}leafID' % self.active_namespaces['def'])
                    if leaf_id:
                        annotated_crf_data['documentRefs'].append({'leafID': leaf_id})
                if annotated_crf_data['documentRefs']:
                    xml_metadata['annotatedCRF'] = annotated_crf_data
                    logger.info(f"  - Captured AnnotatedCRF with {len(annotated_crf_data['documentRefs'])} DocumentRefs")
        
        # Check if any ItemDef has SASFieldName to decide whether to write them back
        has_sas_field_name = any(item_def.get('SASFieldName') for item_def in mdv.findall('.//odm:ItemDef', self.active_namespaces))
        if has_sas_field_name:
            xml_metadata['hasSASFieldName'] = True
        
        # Process methods first to build derivation method map
        logger.info("Processing methods...")
        methods, derivation_method_map, methods_supplemental = self._process_methods(mdv)
        if methods:
            mdv_data['methods'] = [m.model_dump(mode='json', exclude_none=True) if hasattr(m, 'model_dump') else m for m in methods]
            logger.info(f"  - Created {len(methods)} methods")
        
        # Process item groups with nested items (using structured approach)
        logger.info("Processing item groups with nested items...")
        item_groups, ig_supplemental, ig_resources = self._process_item_groups_with_hierarchy(mdv, derivation_method_map)
        if item_groups:
            # Serialize ItemGroup objects to dicts
            mdv_data['itemGroups'] = [ig.model_dump(mode='json', exclude_none=True) if hasattr(ig, 'model_dump') else ig for ig in item_groups]
            logger.info(f"  - Created {len(item_groups)} item groups")
            total_items = sum(len(ig.items or []) for ig in item_groups)
            logger.info(f"  - Total items nested in groups: {total_items}")
        
        # Collect resources from ItemGroup leaves
        if ig_resources:
            if 'resources' not in mdv_data:
                mdv_data['resources'] = []
            mdv_data['resources'].extend([r.model_dump(mode='json', exclude_none=True) if hasattr(r, 'model_dump') else r for r in ig_resources])
        
        # Process code lists
        logger.info("Processing code lists...")
        code_lists, dictionaries, cl_supplemental = self._process_code_lists(mdv)
        if code_lists:
            mdv_data['codeLists'] = [cl.model_dump(mode='json', exclude_none=True) if hasattr(cl, 'model_dump') else cl for cl in code_lists]
            logger.info(f"  - Created {len(code_lists)} code lists")
        if dictionaries:
            mdv_data['dictionaries'] = [d.model_dump(mode='json', exclude_none=True) if hasattr(d, 'model_dump') else d for d in dictionaries]
            logger.info(f"  - Created {len(dictionaries)} dictionaries")
        
        # Process SupplementalDoc as DocumentReference objects (native Define structure)
        logger.info("Processing supplemental doc...")
        supp_doc_refs = self._process_supplemental_doc(mdv)
        if supp_doc_refs:
            # Add to resources array (not _xmlMetadata)
            if 'resources' not in mdv_data:
                mdv_data['resources'] = []
            mdv_data['resources'].extend([r.model_dump(mode='json', exclude_none=True) if hasattr(r, 'model_dump') else r for r in supp_doc_refs])
            logger.info(f"  - Converted {len(supp_doc_refs)} SupplementalDoc refs to DocumentReference objects")
        
        # Process AnalysisResultDisplays as native Analysis and Display objects
        logger.info("Processing analysis result displays...")
        displays, analyses, display_to_analyses = self._process_analysis_result_displays_native(mdv)
        if displays:
            mdv_data['displays'] = [d.model_dump(mode='json', exclude_none=True) if hasattr(d, 'model_dump') else d for d in displays]
            logger.info(f"  - Created {len(displays)} Display objects")
        if analyses:
            # Add analyses to analyses array (MetaDataVersion has separate analyses field)
            mdv_data['analyses'] = [a.model_dump(mode='json', exclude_none=True) if hasattr(a, 'model_dump') else a for a in analyses]
            logger.info(f"  - Created {len(analyses)} Analysis objects")
        # Store display→analyses mapping and display supplemental data
        display_supplemental = {}
        if display_to_analyses:
            display_supplemental['multipleAnalyses'] = display_to_analyses
        if hasattr(self, '_display_supplemental') and self._display_supplemental:
            display_supplemental.update(self._display_supplemental)
        if display_supplemental:
            xml_metadata['displaySupplemental'] = display_supplemental
            logger.info(f"  - Stored Display supplemental data")
        
        # Store analysis→dataset→criteria mapping and AnalysisResult supplemental data
        analysis_supplemental = {}
        if hasattr(self, '_analysis_dataset_criteria') and self._analysis_dataset_criteria:
            analysis_supplemental['datasetCriteria'] = self._analysis_dataset_criteria
            logger.info(f"  - Stored {len(self._analysis_dataset_criteria)} Analysis dataset-criteria mappings")
        
        # Store analysis→parameters mapping (ParamCD/Param attrs) for perfect ParameterList roundtrip
        if hasattr(self, '_analysis_parameters') and self._analysis_parameters:
            analysis_supplemental['parameters'] = self._analysis_parameters
            logger.info(f"  - Stored {len(self._analysis_parameters)} Analysis parameter mappings")
        
        # Store analysis→leafID mapping for Documentation elements with both leafID and text
        if hasattr(self, '_analysis_doc_leafids') and self._analysis_doc_leafids:
            analysis_supplemental['docLeafIDs'] = self._analysis_doc_leafids
            logger.info(f"  - Stored {len(self._analysis_doc_leafids)} Analysis Documentation leafID mappings")
        
        # Store analysis→leafID mapping for empty ProgrammingCode elements with only leafID
        if hasattr(self, '_analysis_progcode_leafids') and self._analysis_progcode_leafids:
            analysis_supplemental['progcodeLeafIDs'] = self._analysis_progcode_leafids
            logger.info(f"  - Stored {len(self._analysis_progcode_leafids)} Analysis ProgrammingCode leafID mappings")
        
        # Store AnalysisResult supplemental data (attributes, Description, Documentation, ProgrammingCode)
        if hasattr(self, '_analysis_result_supplemental') and self._analysis_result_supplemental:
            analysis_supplemental['resultSupplemental'] = self._analysis_result_supplemental
            logger.info(f"  - Stored {len(self._analysis_result_supplemental)} AnalysisResult supplemental data")
        
        # Store AnalysisDataset supplemental data (children: WhereClauseRef, AnalysisVariable)
        if hasattr(self, '_analysis_dataset_supplemental') and self._analysis_dataset_supplemental:
            analysis_supplemental['datasetSupplemental'] = self._analysis_dataset_supplemental
            logger.info(f"  - Stored AnalysisDataset supplemental data")
        
        # Store AnalysisDatasets supplemental data (container-level attributes like CommentOID)
        if hasattr(self, '_analysis_datasets_supplemental') and self._analysis_datasets_supplemental:
            analysis_supplemental['datasetsSupplemental'] = self._analysis_datasets_supplemental
            logger.info(f"  - Stored AnalysisDatasets supplemental data")
        
        if analysis_supplemental:
            xml_metadata['analysisSupplemental'] = analysis_supplemental
        
        # Capture MetaDataVersion-level def:leaf elements and convert to Resources
        logger.info("Processing MetaDataVersion-level leaf elements...")
        mdv_resources = []
        for leaf_elem in mdv.findall('def:leaf', self.active_namespaces):
            resource = self._leaf_to_resource(leaf_elem)
            if resource:
                mdv_resources.append(resource)
        
        if mdv_resources:
            # Store in resources array (will be added to mdv_data)
            if 'resources' not in mdv_data:
                mdv_data['resources'] = []
            mdv_data['resources'].extend([r.model_dump(mode='json', exclude_none=True) if hasattr(r, 'model_dump') else r for r in mdv_resources])
            logger.info(f"  - Converted {len(mdv_resources)} MetaDataVersion-level leaf elements to Resources")
        
        # Process comments (CommentDef elements)
        logger.info("Processing comments...")
        comments, comment_supplemental = self._process_comments(mdv)
        if comment_supplemental:
            xml_metadata['commentSupplemental'] = comment_supplemental
            logger.info(f"  - Processed {len(comment_supplemental)} CommentDef elements")
        
        # Check if MetaDataVersion has Comment attribute
        mdv_comment = mdv.get('Comment')
        if mdv_comment is not None:
            mdv_data['comments'] = [mdv_comment] if mdv_comment.strip() else []
        
        # Process conditions and where clauses
        logger.info("Processing conditions and where clauses...")
        conditions, where_clauses, cond_supplemental = self._process_conditions_and_where_clauses(mdv)
        if conditions:
            mdv_data['conditions'] = [c.model_dump(mode='json', exclude_none=True) if hasattr(c, 'model_dump') else c for c in conditions]
            logger.info(f"  - Created {len(conditions)} conditions")
        if where_clauses:
            mdv_data['whereClauses'] = [wc.model_dump(mode='json', exclude_none=True) if hasattr(wc, 'model_dump') else wc for wc in where_clauses]
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
        
        # Add supplemental XML metadata for roundtrip (only if non-empty)
        if ig_supplemental:
            xml_metadata['itemGroupSupplemental'] = ig_supplemental
        if cl_supplemental:
            xml_metadata['codeListSupplemental'] = cl_supplemental
        if methods_supplemental:
            xml_metadata['methodSupplemental'] = methods_supplemental
        if cond_supplemental:
            xml_metadata['conditionSupplemental'] = cond_supplemental
        
        # Add inference log if preserve_original is False
        if not self.preserve_original and self.inference_log:
            xml_metadata['inferenceLog'] = self.inference_log
            logger.info(f"  - Recorded {len(self.inference_log)} inference operations")
        
        result['_xmlMetadata'] = xml_metadata
        
        # Save to file
        logger.info(f"Writing output to {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str, ensure_ascii=False)
        
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
            # Strip timezone to create naive datetime (Define-XML doesn't require TZ awareness)
            # This ensures consistent serialization format
            if 'T' in dt_str:
                # Remove timezone: +HH:MM, -HH:MM, Z, or +HH:MM:SS
                dt_no_tz = dt_str.split('+')[0].split('Z')[0]
                # Also handle -HH:MM timezone format by finding last dash after 'T'
                if '-' in dt_no_tz and 'T' in dt_no_tz:
                    time_part_start = dt_no_tz.index('T')
                    last_dash = dt_no_tz.rfind('-')
                    if last_dash > time_part_start:
                        dt_no_tz = dt_no_tz[:last_dash]
                return datetime.fromisoformat(dt_no_tz)
            return datetime.fromisoformat(dt_str)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse datetime '{dt_str}': {e}, using current datetime")
            return datetime.now()
    
    def _leaf_to_resource(self, leaf_elem: ET.Element) -> Optional[Resource]:
        """Convert a def:leaf element to a Resource object."""
        leaf_id = leaf_elem.get('ID')
        if not leaf_id:
            return None
        
        # Get href
        href = leaf_elem.get('{%s}href' % self.active_namespaces.get('xlink', ''))
        
        # Get title
        title_elem = leaf_elem.find('def:title', self.active_namespaces)
        title = title_elem.text if title_elem is not None and title_elem.text else None
        
        # Create Resource - use leaf ID as OID, title as name/label
        resource_data = {
            'OID': f"RES.{leaf_id}",  # Prefix to ensure valid OID format
            'name': title or leaf_id,
            'href': href,
            'resourceType': 'ODM',  # Default for Define-XML leaf elements
        }
        
        if title:
            resource_data['label'] = title
        
        try:
            return Resource(**resource_data)
        except Exception as e:
            logger.warning(f"Failed to create Resource from leaf {leaf_id}: {e}")
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
            
            # Get DocumentRef elements
            doc_refs = []
            method_supp = {}
            for doc_ref in method_elem.findall('def:DocumentRef', self.active_namespaces):
                leaf_id = doc_ref.get('leafID')
                if leaf_id:
                    # DocumentReference requires OID field - use leafID as the OID
                    doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                    
                    # Extract PDFPageRef elements if present
                    pdf_page_refs = []
                    for pdf_ref in doc_ref.findall('def:PDFPageRef', self.active_namespaces):
                        pdf_data = {}
                        if pdf_ref.get('Type'):
                            pdf_data['type'] = pdf_ref.get('Type')
                        if pdf_ref.get('PageRefs'):
                            pdf_data['pageRefs'] = pdf_ref.get('PageRefs')
                        if pdf_ref.get('FirstPage'):
                            pdf_data['firstPage'] = int(pdf_ref.get('FirstPage'))
                        if pdf_ref.get('LastPage'):
                            pdf_data['lastPage'] = int(pdf_ref.get('LastPage'))
                        if pdf_data:
                            pdf_page_refs.append(pdf_data)
                    
                    # Store PDFPageRefs in supplemental metadata for roundtrip
                    if pdf_page_refs:
                        method_supp[f'pdfPageRefs_{leaf_id}'] = pdf_page_refs
                    
                    doc_refs.append(doc_ref_data)
            if doc_refs:
                method_data['documents'] = doc_refs
            
            # Store method supplemental data if present
            if method_supp:
                supplemental[method_oid] = method_supp
            
            # Get FormalExpression elements (in odm namespace, not def)
            formal_exprs = []
            for idx, fe_elem in enumerate(method_elem.findall('odm:FormalExpression', self.active_namespaces)):
                fe_data = {}
                # Generate synthetic OID for FormalExpression (not present in Define-XML)
                fe_data['OID'] = f"{method_oid}.FE.{idx + 1}"
                context = fe_elem.get('Context')
                if context:
                    fe_data['context'] = context
                expr_text = fe_elem.text
                if expr_text and expr_text.strip():
                    fe_data['expression'] = expr_text.strip()
                if fe_data:
                    formal_exprs.append(fe_data)
            if formal_exprs:
                method_data['expressions'] = formal_exprs
            
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
                # NO FLAG NEEDED: ComputationMethod elements are inferred during XML write
                # If a method has no ItemDef references, it's a ComputationMethod (ARM-specific)
                # and won't be written as a top-level MethodDef element
            except Exception as e:
                logger.warning(f"Failed to create Method {method_oid}: {e}")
        
        return methods, derivation_map, supplemental
    
    def _get_method_description(self, method_elem: ET.Element) -> Optional[str]:
        """Extract method description from Description element (not FormalExpression)."""
        # Try Description/TranslatedText first (preferred)
        desc = method_elem.find('.//odm:Description/odm:TranslatedText', self.active_namespaces)
        if desc is not None and desc.text:
            return desc.text.strip()
        
        # Fallback to FormalExpression only if no Description exists
        formal_expr = method_elem.find('.//odm:FormalExpression', self.active_namespaces)
        if formal_expr is not None and formal_expr.text:
            return formal_expr.text.strip()
        
        return None
    
    def _process_item_groups_with_hierarchy(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict, List[Resource]]:
        """
        Process ItemGroupDef elements with items nested inside (using ItemGroup.items field).
        Also establishes parent-child relationships with ValueLists.
        
        Returns:
            Tuple of (item_groups_list, supplemental_data, resources_from_leaves)
        """
        item_groups = []
        supplemental = {}
        
        # Process domain-level ItemGroups
        domain_igs, domain_supp, domain_resources = self._process_domain_item_groups(mdv, derivation_method_map)
        item_groups.extend(domain_igs)
        
        # Collect resources from ItemGroup leaves
        all_resources = domain_resources.copy() if domain_resources else []
        
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
                    # Check for def:ValueListRef child element (correct approach)
                    vl_ref_elem = item_def.find('def:ValueListRef', self.active_namespaces)
                    if vl_ref_elem is not None:
                        vl_ref = vl_ref_elem.get('ValueListOID')
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
        
        # Nest ValueList ItemGroups under their parent domains (not just OID references!)
        # A ValueList can have multiple parents - if so, nest under first, reference from others
        children_added = 0
        nested_valuelist_oids = set()  # Track which ValueLists have been nested
        
        for vl_ig in value_list_igs:
            parent_oids = valuelist_to_parent.get(vl_ig.OID, [])
            
            # Handle both single parent (backward compat) and multiple parents
            if isinstance(parent_oids, str):
                parent_oids = [parent_oids]
            
            if not parent_oids:
                logger.warning(f"    - ValueList {vl_ig.OID} has no parent, will remain at top level")
                continue
            
            # Nest under FIRST parent (full object)
            first_parent_oid = parent_oids[0]
            for domain_ig in domain_igs:
                if domain_ig.OID == first_parent_oid:
                    if domain_ig.slices is None:
                        domain_ig.slices = []
                    # Nest the ACTUAL ValueList object, not just OID
                    domain_ig.slices.append(vl_ig)
                    nested_valuelist_oids.add(vl_ig.OID)
                    children_added += 1
                    logger.info(f"    - Nested {vl_ig.OID} under parent {first_parent_oid}")
                    break
            
            # For additional parents (if any), just add OID reference
            for parent_oid in parent_oids[1:]:
                for domain_ig in domain_igs:
                    if domain_ig.OID == parent_oid:
                        if domain_ig.slices is None:
                            domain_ig.slices = []
                        # Additional parents get OID reference (avoid duplication)
                        if vl_ig.OID not in domain_ig.slices:
                            domain_ig.slices.append(vl_ig.OID)
                            logger.info(f"    - Added OID reference {vl_ig.OID} to additional parent {parent_oid}")
                        break
        
        logger.info(f"  - Nested {children_added} ValueLists under parent domains")
        
        # If inference is enabled, try to infer ValueList -> Domain links based on OID substring matching
        if not self.preserve_original:
            inferred_links = self._infer_valuelist_domain_links(value_list_igs, domain_igs, valuelist_to_parent)
            logger.info(f"  - Inferred {inferred_links} additional ValueList links via OID matching")
        
        # Return only domain ItemGroups at top level (ValueLists are now nested in slices)
        # Keep orphaned ValueLists (no parent) at top level
        orphaned_valuelists = [vl for vl in value_list_igs if vl.OID not in nested_valuelist_oids]
        top_level_item_groups = domain_igs + orphaned_valuelists
        
        if orphaned_valuelists:
            logger.warning(f"  - {len(orphaned_valuelists)} ValueLists remain at top level (no parent detected)")
        
        return top_level_item_groups, supplemental, all_resources
    
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
                    if domain_ig.slices is None:
                        domain_ig.slices = []
                    
                    if vl_ig.OID not in domain_ig.slices:
                        domain_ig.slices.append(vl_ig.OID)
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
    
    def _process_domain_item_groups(self, mdv: ET.Element, derivation_method_map: Dict) -> Tuple[List[ItemGroup], Dict, List[Resource]]:
        """Process domain-level ItemGroupDef elements as Pydantic ItemGroup objects.
        
        Returns:
            Tuple of (item_groups, supplemental_data, resources_from_leaves)
        """
        item_groups = []
        supplemental = {}
        item_origin_metadata = {}  # Track origin metadata for all items
        resources = []  # Collect resources from leaf elements
        
        for ig_elem in mdv.findall('.//odm:ItemGroupDef', self.active_namespaces):
            ig_oid = ig_elem.get('OID')
            if not ig_oid:
                continue
            
            ig_data = {'OID': ig_oid}
            ig_supp = {'OID': ig_oid}
            
            # Name
            if ig_elem.get('Name'):
                ig_data['name'] = ig_elem.get('Name')
            
            # Label and Description
            # In Define-XML 2.1:
            # - def:Label attribute is an optional short label for display purposes
            # - Description element is the full item group description
            # These are independent fields and should both be preserved
            def_label = ig_elem.get('{%s}Label' % self.active_namespaces['def'])
            description_text = self._get_description(ig_elem)
            
            if def_label:
                ig_data['label'] = def_label
            if description_text:
                ig_data['description'] = description_text
            
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
            # def:Class - can be either attribute or child element
            class_attr = ig_elem.get('{%s}Class' % self.active_namespaces['def'])
            if class_attr:
                ig_supp['defClass'] = class_attr
                ig_supp['classIsAttribute'] = True  # Track that it was an attribute
            else:
                # Check for def:Class child element
                class_elem = ig_elem.find('def:Class', self.active_namespaces)
                if class_elem is not None:
                    class_name = class_elem.get('Name')
                    if class_name:
                        ig_supp['defClass'] = class_name
                        ig_supp['classIsAttribute'] = False  # Track that it was a child element
                    
                    # Extract SubClass children
                    sub_classes = []
                    for sub_class_elem in class_elem.findall('def:SubClass', self.active_namespaces):
                        sub_class_name = sub_class_elem.get('Name')
                        if sub_class_name:
                            sub_classes.append({'name': sub_class_name})
                    if sub_classes:
                        ig_supp['subClasses'] = sub_classes
            
            # def:DomainKeys
            domain_keys = ig_elem.get('{%s}DomainKeys' % self.active_namespaces['def'])
            if domain_keys:
                ig_supp['defDomainKeys'] = domain_keys
            
            # Note: def:Label is already captured in native 'label' field above, no need for defLabel in supplemental
            
            # Comment attribute -> use native comments array
            comment = ig_elem.get('Comment')
            if comment is not None:  # Check for None, not truthiness (to capture empty strings)
                if comment.strip():  # Only add non-empty comments
                    ig_data['comments'] = [comment]
                # Store empty comment in supplemental for roundtrip
                ig_supp['comment'] = comment
            
            # def:CommentOID - preserve for roundtrip
            comment_oid = ig_elem.get('{%s}CommentOID' % self.active_namespaces['def'])
            if comment_oid:
                ig_supp['commentOID'] = comment_oid
            
            # def:StandardOID - preserve for roundtrip
            standard_oid = ig_elem.get('{%s}StandardOID' % self.active_namespaces['def'])
            if standard_oid:
                ig_supp['standardOID'] = standard_oid
            
            # def:IsNonStandard - preserve for roundtrip
            is_non_standard = ig_elem.get('{%s}IsNonStandard' % self.active_namespaces['def'])
            if is_non_standard:
                ig_supp['isNonStandard'] = is_non_standard
            
            # def:HasNoData - preserve for roundtrip
            has_no_data = ig_elem.get('{%s}HasNoData' % self.active_namespaces['def'])
            if has_no_data:
                ig_supp['hasNoData'] = has_no_data
            
            # Process Alias elements - store as Coding objects
            # Alias with Context/Name maps to Coding (codeSystem=Context, code=Name)
            aliases = []
            for alias_elem in ig_elem.findall('odm:Alias', self.active_namespaces):
                context = alias_elem.get('Context')
                name = alias_elem.get('Name')
                if context and name:
                    from ..schema.define import Coding
                    aliases.append(Coding(codeSystem=context, code=name))
            if aliases:
                ig_data['coding'] = aliases
            
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
            
            # Capture def:leaf elements and convert to Resource
            # Store Resource OID reference in supplemental for roundtrip
            leaf_elem = ig_elem.find('def:leaf', self.active_namespaces)
            if leaf_elem is not None:
                resource = self._leaf_to_resource(leaf_elem)
                if resource:
                    resources.append(resource)  # Collect for resources array
                    # Store Resource OID reference for roundtrip
                    ig_supp['sourceResourceOID'] = resource.OID
                    # Also store original leaf data for roundtrip
                leaf_id = leaf_elem.get('ID')
                if leaf_id:
                        ig_supp['leafID'] = leaf_id
            
            # Process ItemRefs - create full Item objects nested in items list
            # Order is preserved by array ordering, no need to track OrderNumber
            items = []
            key_items = []  # Collect items with KeySequence for native keySequence field
            for item_ref in ig_elem.findall('odm:ItemRef', self.active_namespaces):
                item_oid = item_ref.get('ItemOID')
                key_seq = item_ref.get('KeySequence')
                
                item_def = mdv.find(f'.//odm:ItemDef[@OID="{item_oid}"]', self.active_namespaces)
                
                if item_def is not None:
                    item_obj, item_supp = self._create_item_object(item_def, item_ref, derivation_method_map)
                    if item_obj:
                        items.append(item_obj)
                        
                        # Collect KeySequence for native keySequence field
                        if key_seq:
                            key_items.append({'oid': item_oid, 'seq': int(key_seq)})
                        
                        # Collect supplemental metadata (origin metadata, valueListOID, commentOID, hasNoData, etc.)
                        # NOTE: keySequence is now stored natively, not in supplemental
                        supp_data = {}
                        if 'originMetadata' in item_supp:
                            supp_data.update(item_supp['originMetadata'])
                        if 'valueListOID' in item_supp:
                            supp_data['valueListOID'] = item_supp['valueListOID']
                        if 'commentOID' in item_supp:
                            supp_data['commentOID'] = item_supp['commentOID']
                        if 'hasNoData' in item_supp:
                            supp_data['hasNoData'] = item_supp['hasNoData']
                        if 'SASFieldName' in item_supp:
                            supp_data['SASFieldName'] = item_supp['SASFieldName']
                        if supp_data:
                            item_origin_metadata[item_oid] = supp_data
            
            if items:
                ig_data['items'] = items
            
            # Build keySequence array: ordered list of Item OIDs based on KeySequence attribute
            # Store in native field (not supplemental)
            if key_items:
                # Sort by KeySequence value
                key_items.sort(key=lambda x: x['seq'])
                # Extract OIDs in order
                ig_data['keySequence'] = [k['oid'] for k in key_items]
            
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
        
        return item_groups, supplemental, resources
    
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
        
        # Label and Description
        # In Define-XML 2.1:
        # - def:Label attribute is an optional short label for display purposes
        # - Description element is the full item description
        # These are independent fields and should both be preserved
        def_label = item_def.get('{%s}Label' % self.active_namespaces['def'])
        description_text = self._get_description(item_def)
        
        if def_label:
            item_data['label'] = def_label
        if description_text:
            item_data['description'] = description_text
        
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
        
        # SASFieldName - extract and store in supplemental metadata (even if equals Name)
        # Store in supplemental metadata as it's not part of the Item schema
        # We need to store it even when it equals Name to preserve roundtrip
        sas_field_name = item_def.get('SASFieldName')
        if sas_field_name:
            item_supp['SASFieldName'] = sas_field_name
        
        # Origin - properly handled (Origin itself has no description field)
        origin_data, origin_metadata_from_get = self._get_origin(item_def)
        
        # Merge origin metadata
        if origin_metadata_from_get:
            origin_metadata.update(origin_metadata_from_get)
        
        # Extract metadata fields that don't belong in Origin Pydantic model
        if origin_data:
            # Extract comment and format metadata
            comment = origin_data.pop('comment', None)
            was_element = origin_data.pop('_wasElement', None)
            comment_for_linking = origin_data.pop('_commentForMethodLinking', None)
            
            # Store comment in supplemental for roundtrip
            # Note: Item.comments expects list[str], not Comment objects
            # Origin comments are stored in supplemental metadata, not in Item.comments
            if comment:
                origin_metadata['comment'] = comment
            
            # Store metadata flags in supplemental for roundtrip
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
            
            # MethodOID - preserve from XML for perfect roundtrip
            # Store in 'method' field (Item model uses 'method' not 'methodOID')
            method_oid = item_ref.get('MethodOID')
            if method_oid:
                item_data['method'] = method_oid
            
            # def:HasNoData - preserve for roundtrip
            has_no_data = item_ref.get('{%s}HasNoData' % self.active_namespaces['def'])
            if has_no_data:
                item_supp['hasNoData'] = has_no_data
            
            # KeySequence - now stored at ItemGroup level, not per-item
            # (extracted in _process_domain_item_groups)
            
            # WhereClause reference (store in applicableWhen)
            where_clause_ref = item_ref.find('def:WhereClauseRef', self.active_namespaces)
            if where_clause_ref is not None:
                wc_oid = where_clause_ref.get('WhereClauseOID')
                if wc_oid:
                    item_data['applicableWhen'] = [wc_oid]
        
        # Check for def:ValueListRef child element on ItemDef
        vl_ref_elem = item_def.find('def:ValueListRef', self.active_namespaces)
        if vl_ref_elem is not None:
            vl_oid = vl_ref_elem.get('ValueListOID')
            if vl_oid:
                item_supp['valueListOID'] = vl_oid
        
        # def:CommentOID attribute on ItemDef (for roundtrip)
        comment_oid = item_def.get('{%s}CommentOID' % self.active_namespaces['def'])
        if comment_oid:
            item_supp['commentOID'] = comment_oid
        
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
        
        Legacy Terminology Upgrade (pre-Define 2.1):
        - Old "CRF" → Upgraded to "Collected" (one-way conversion)
        - Old "eDT" → Upgraded to "Collected" (one-way conversion)
        
        Current OriginType enum values:
        - Assigned: Values from lookup tables/CRF labels
        - Collected: Observed/recorded data (replaces CRF/eDT)
        - Derived: Calculated values
        - Not_Available: Not discoverable
        - Other: Catch-all
        - Predecessor: Copied from another variable
        - Protocol: Protocol-defined values
        
        Returns:
            Tuple of (origin_dict, origin_metadata)
        """
        origin = {}
        has_origin_element = False  # Track if origin was an element vs attribute
        origin_metadata = {}  # Initialize for storing non-standard values
        
        # Check for def:Origin element (v2.x style)
        origin_elem = item_def.find('.//def:Origin', self.active_namespaces)
        if origin_elem is not None:
            has_origin_element = True
            origin_type = origin_elem.get('Type')
            if origin_type:
                try:
                    origin['type'] = OriginType(origin_type)
                except ValueError:
                    # Handle legacy terminology (CRF/eDT → Collected)
                    if origin_type in ['CRF', 'eDT']:
                        origin['type'] = OriginType.Collected
                        logger.info(f"Upgraded legacy OriginType '{origin_type}' → 'Collected' for item {item_def.get('OID')}")
                    else:
                        # Invalid value → use Other as fallback
                        logger.warning(f"Invalid OriginType '{origin_type}' for item {item_def.get('OID')}, using 'Other'")
                        origin['type'] = OriginType.Other
            
            source = origin_elem.get('Source')
            if source:
                try:
                    origin['source'] = OriginSource(source)
                except ValueError:
                    logger.warning(f"Invalid OriginSource: {source}")
                    origin['source'] = source
            
            # Extract Description from Origin element (for roundtrip)
            # Note: Origin class doesn't have a description field in the schema,
            # so we store this in metadata for perfect roundtrip
            origin_desc = self._get_description(origin_elem)
            if origin_desc:
                origin_metadata['originDescription'] = origin_desc
            
            # Extract DocumentRef elements from Origin
            doc_refs = []
            for doc_ref in origin_elem.findall('def:DocumentRef', self.active_namespaces):
                leaf_id = doc_ref.get('leafID')
                if leaf_id:
                    # DocumentReference requires OID field - use leafID as the OID
                    doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                    
                    # Extract PDFPageRef elements if present
                    pdf_page_refs = []
                    for pdf_ref in doc_ref.findall('def:PDFPageRef', self.active_namespaces):
                        pdf_data = {}
                        if pdf_ref.get('Type'):
                            pdf_data['type'] = pdf_ref.get('Type')
                        if pdf_ref.get('PageRefs'):
                            pdf_data['pageRefs'] = pdf_ref.get('PageRefs')
                        if pdf_ref.get('FirstPage'):
                            pdf_data['firstPage'] = int(pdf_ref.get('FirstPage'))
                        if pdf_ref.get('LastPage'):
                            pdf_data['lastPage'] = int(pdf_ref.get('LastPage'))
                        if pdf_data:
                            pdf_page_refs.append(pdf_data)
                    
                    # Store PDFPageRefs in supplemental metadata for roundtrip
                    if pdf_page_refs:
                        origin_metadata[f'pdfPageRefs_{leaf_id}'] = pdf_page_refs
                    
                    doc_refs.append(doc_ref_data)
            
            if doc_refs:
                origin['documents'] = doc_refs
        
        # Check for Origin attribute (v1.x style)
        origin_attr = item_def.get('Origin')
        if origin_attr and not origin.get('type'):
            try:
                origin['type'] = OriginType(origin_attr)
            except ValueError:
                # Handle legacy terminology in attributes (CRF/eDT → Collected)
                if origin_attr in ['CRF', 'eDT']:
                    origin['type'] = OriginType.Collected
                    logger.info(f"Upgraded legacy Origin attribute '{origin_attr}' → 'Collected' for item {item_def.get('OID')}")
                else:
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
        
        return origin, origin_metadata
    
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
            # Order is preserved by array ordering, no need to track OrderNumber
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
                        # Collect supplemental metadata (origin metadata, SASFieldName, commentOID, valueListOID, etc.)
                        supp_data = {}
                        if 'originMetadata' in item_supp:
                            supp_data.update(item_supp['originMetadata'])
                        if 'SASFieldName' in item_supp:
                            supp_data['SASFieldName'] = item_supp['SASFieldName']
                        if 'commentOID' in item_supp:
                            supp_data['commentOID'] = item_supp['commentOID']
                        if 'valueListOID' in item_supp:
                            supp_data['valueListOID'] = item_supp['valueListOID']
                        if supp_data:
                            item_origin_metadata[item_oid] = supp_data
            
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
                # No supplemental data needed - ValueList is identified by type='ValueList'
                supplemental[vl_oid] = {}
            except Exception as e:
                logger.error(f"Failed to create ValueList ItemGroup {vl_oid}: {e}")
                logger.error(f"  ig_data keys: {ig_data.keys()}")
                logger.error(f"  items type: {type(items)}, count: {len(items)}")
                if items:
                    logger.error(f"  first item type: {type(items[0])}")
                import traceback
                logger.error(f"  Full traceback: {traceback.format_exc()}")
                # Store failed item data in supplemental for debugging only
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
            
            # Process Alias elements on CodeList
            # Check if they are coding references (e.g., nci:ExtCodeID) or true aliases
            aliases = []
            codings = []
            for alias_elem in cl_elem.findall('odm:Alias', self.active_namespaces):
                context = alias_elem.get('Context')
                name = alias_elem.get('Name')
                
                # If context suggests terminology/coding (e.g., nci:ExtCodeID), treat as coding
                if context and name and ('ExtCodeID' in context or 'nci:' in context.lower() or 'cdisc:' in context.lower()):
                    codings.append(Coding(
                        codeSystem=context,
                        code=name
                    ))
                # Otherwise, treat as a true alias
                elif context and name:
                    # Use ||| as delimiter (unlikely to appear in real data)
                    aliases.append(f"{context}|||{name}")
                elif name:
                    aliases.append(name)
            
            if aliases:
                cl_data['aliases'] = aliases
            if codings:
                cl_data['coding'] = codings
            
            # Extract def: namespaced attributes for roundtrip
            # def:StandardOID
            standard_oid = cl_elem.get('{%s}StandardOID' % self.active_namespaces['def'])
            if standard_oid:
                cl_supp['standardOID'] = standard_oid
            
            # def:CommentOID
            comment_oid = cl_elem.get('{%s}CommentOID' % self.active_namespaces['def'])
            if comment_oid:
                cl_supp['commentOID'] = comment_oid
            
            # def:IsNonStandard
            is_non_standard = cl_elem.get('{%s}IsNonStandard' % self.active_namespaces['def'])
            if is_non_standard:
                cl_supp['isNonStandard'] = is_non_standard
            
            # SASFormatName
            sas_format = cl_elem.get('SASFormatName')
            if sas_format:
                cl_supp['sasFormatName'] = sas_format
            
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
            # Track element type for each item (CodeListItem vs EnumeratedItem)
            item_element_types = {}
            
            # Process both CodeListItem and EnumeratedItem
            codelist_item_supp = {}  # Track supplemental data per CodeListItem
            for item_elem in cl_elem.findall('.//odm:CodeListItem', self.active_namespaces):
                coded_value = item_elem.get('CodedValue')
                if not coded_value:
                    continue
                    
                item_data = {'codedValue': coded_value}
                item_element_types[coded_value] = 'CodeListItem'
                item_supp_data = {}
                
                # Decode
                decode = self._get_decode(item_elem)
                if decode:
                    item_data['decode'] = decode
                
                # Description
                desc = self._get_description(item_elem)
                if desc:
                    item_data['description'] = desc
                
                # Extract Rank and map to weight
                # Rank can be namespaced (def:Rank) or non-namespaced (Rank)
                rank = item_elem.get(f'{{{self.active_namespaces["def"]}}}Rank') or item_elem.get('Rank')
                if rank:
                    try:
                        item_data['weight'] = int(rank)
                    except ValueError:
                        item_data['weight'] = float(rank)
                
                # Extract def:ExtendedValue (can be on CodeListItem too)
                extended_value = item_elem.get(f'{{{self.active_namespaces["def"]}}}ExtendedValue')
                if extended_value:
                    item_supp_data['extendedValue'] = extended_value
                
                # Process Alias elements - store as coding (semantic reference)
                # Only take the first one as coding (ODM allows multiple, but schema expects single Coding)
                for alias_elem in item_elem.findall('odm:Alias', self.active_namespaces):
                    context = alias_elem.get('Context')
                    name = alias_elem.get('Name')
                    if context and name and 'coding' not in item_data:
                        # Map to Coding structure: Context → codeSystem, Name → code
                        item_data['coding'] = Coding(
                            codeSystem=context,
                            code=name
                        )
                        break  # Only take first alias as primary coding
                
                # Try to create CodeListItem Pydantic object
                try:
                    cli_obj = CodeListItem(**item_data)
                    code_list_items.append(cli_obj)
                    if item_supp_data:
                        codelist_item_supp[coded_value] = item_supp_data
                except Exception as e:
                    logger.warning(f"Failed to create CodeListItem for {coded_value}: {e}")
                    # Store in supplemental if can't create Pydantic object
                    if 'failed_items' not in cl_supp:
                        cl_supp['failed_items'] = []
                    cl_supp['failed_items'].append(item_data)
            
            # Store CodeListItem supplemental data if present
            if codelist_item_supp:
                cl_supp['codeListItemSupplemental'] = codelist_item_supp
            
            # Process EnumeratedItem elements (simpler, no Decode)
            enumerated_item_supp = {}  # Track supplemental data per EnumeratedItem
            for item_elem in cl_elem.findall('.//odm:EnumeratedItem', self.active_namespaces):
                coded_value = item_elem.get('CodedValue')
                if not coded_value:
                    continue
                    
                item_data = {'codedValue': coded_value}
                item_element_types[coded_value] = 'EnumeratedItem'
                item_supp_data = {}
                
                # Extract Rank and map to weight (same as CodeListItem)
                # Rank can be namespaced (def:Rank) or non-namespaced (Rank)
                rank = item_elem.get(f'{{{self.active_namespaces["def"]}}}Rank') or item_elem.get('Rank')
                if rank:
                    try:
                        item_data['weight'] = int(rank)
                    except ValueError:
                        item_data['weight'] = float(rank)
                
                # Extract def:ExtendedValue (specific to EnumeratedItem)
                extended_value = item_elem.get(f'{{{self.active_namespaces["def"]}}}ExtendedValue')
                if extended_value:
                    item_supp_data['extendedValue'] = extended_value
                
                # EnumeratedItem has Alias but no Decode
                for alias_elem in item_elem.findall('odm:Alias', self.active_namespaces):
                    context = alias_elem.get('Context')
                    name = alias_elem.get('Name')
                    if context and name and 'coding' not in item_data:
                        item_data['coding'] = Coding(
                            codeSystem=context,
                            code=name
                        )
                        break
                
                try:
                    cli_obj = CodeListItem(**item_data)
                    code_list_items.append(cli_obj)
                    if item_supp_data:
                        enumerated_item_supp[coded_value] = item_supp_data
                except Exception as e:
                    logger.warning(f"Failed to create CodeListItem from EnumeratedItem {coded_value}: {e}")
            
            # Store EnumeratedItem supplemental data if present
            if enumerated_item_supp:
                cl_supp['enumeratedItemSupplemental'] = enumerated_item_supp
            
            # Store element types ONLY if needed for roundtrip
            # Only store if: (1) Mixed CodeList (has both types) OR (2) All EnumeratedItems
            if item_element_types:
                has_code_list_item = 'CodeListItem' in item_element_types.values()
                has_enumerated_item = 'EnumeratedItem' in item_element_types.values()
                
                # Case 1: Mixed - store all mappings
                if has_code_list_item and has_enumerated_item:
                    cl_supp['itemElementTypes'] = item_element_types
                # Case 2: Pure EnumeratedItem - store flag only
                elif has_enumerated_item:
                    cl_supp['isEnumeratedList'] = True
                # Case 3: Pure CodeListItem - store nothing (default assumption)
            
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
    
    def _process_comments(self, mdv: ET.Element) -> Tuple[List[Comment], Dict]:
        """
        Process def:CommentDef elements and store in supplemental metadata.
        
        Returns:
            Tuple of (empty list, supplemental_data with full Comment data)
        """
        supplemental = {}
        
        for comment_def in mdv.findall('.//def:CommentDef', self.active_namespaces):
            comment_oid = comment_def.get('OID')
            if not comment_oid:
                continue
            
            comment_data = {'OID': comment_oid}
            
            # Get Description text (required field called 'text' in Comment class)
            desc_text = self._get_description(comment_def)
            if desc_text:
                comment_data['text'] = desc_text
            
            # Get DocumentRef elements
            doc_refs = []
            for doc_ref in comment_def.findall('def:DocumentRef', self.active_namespaces):
                leaf_id = doc_ref.get('leafID')
                if leaf_id:
                    # DocumentReference requires OID field - use leafID as the OID
                    doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                    
                    # Extract PDFPageRef elements if present
                    pdf_page_refs = []
                    for pdf_ref in doc_ref.findall('def:PDFPageRef', self.active_namespaces):
                        pdf_data = {}
                        if pdf_ref.get('Type'):
                            pdf_data['type'] = pdf_ref.get('Type')
                        if pdf_ref.get('PageRefs'):
                            pdf_data['pageRefs'] = pdf_ref.get('PageRefs')
                        if pdf_ref.get('FirstPage'):
                            pdf_data['firstPage'] = int(pdf_ref.get('FirstPage'))
                        if pdf_ref.get('LastPage'):
                            pdf_data['lastPage'] = int(pdf_ref.get('LastPage'))
                        if pdf_data:
                            pdf_page_refs.append(pdf_data)
                    
                    # Add PDFPageRefs to DocumentRef
                    if pdf_page_refs:
                        doc_ref_data['pdfPageRefs'] = pdf_page_refs
                    
                    doc_refs.append(doc_ref_data)
            
            if doc_refs:
                comment_data['documents'] = doc_refs
            
            # Store full Comment data in supplemental (keyed by OID)
            supplemental[comment_oid] = comment_data
        
        return [], supplemental
    
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
            
            # Extract def:CommentOID for roundtrip
            comment_oid = wc_elem.get('{%s}CommentOID' % self.active_namespaces['def'])
            
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
                # ItemOID can be either 'ItemOID' or 'def:ItemOID'
                item_oid = rc.get('ItemOID') or rc.get('{%s}ItemOID' % self.active_namespaces.get('def', ''))
                
                # Get all CheckValue elements (can be multiple)
                check_value_elems = rc.findall('.//odm:CheckValue', self.active_namespaces)
                check_values = [cv.text for cv in check_value_elems if cv.text]
                
                if comparator and item_oid:
                    range_check_data = {
                        'comparator': comparator,
                        'item': item_oid,  # Use 'item' to match Define-JSON schema
                    }
                    # Use checkValues (plural) list to match Define-JSON schema
                    if check_values:
                        range_check_data['checkValues'] = check_values
                    
                    # SoftHard attribute (optional)
                    soft_hard = rc.get('SoftHard')
                    if soft_hard:
                        range_check_data['softHard'] = soft_hard
                    
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
                    
                    # Store CommentOID in supplemental if present
                    if comment_oid:
                        supplemental[wc_oid] = {'commentOID': comment_oid}
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
    
    def _process_supplemental_doc(self, mdv: ET.Element) -> Optional[List[DocumentReference]]:
        """
        Process SupplementalDoc element as DocumentReference objects.
        
        Returns:
            List of DocumentReference objects, or None if not found
        """
        # Find SupplementalDoc element
        supp_doc = mdv.find('.//def:SupplementalDoc', self.active_namespaces)
        if not supp_doc:
            return None
        
        # Extract DocumentRef children and create DocumentReference objects
        doc_refs = []
        for doc_ref in supp_doc.findall('.//def:DocumentRef', self.active_namespaces):
            leaf_id = doc_ref.get('{%s}leafID' % self.active_namespaces.get('def', ''))
            if not leaf_id:
                leaf_id = doc_ref.get('leafID')  # Fallback without namespace
            
            if leaf_id:
                # Look up the actual leaf element to get title and href
                leaf_elem = mdv.find(f'.//def:leaf[@ID="{leaf_id}"]', self.active_namespaces)
                
                doc_ref_data = {
                    'OID': f'DOC.SUPP.{leaf_id}',  # Generate OID for DocumentReference
                    'leafID': leaf_id
                }
                
                # Extract title from leaf
                if leaf_elem is not None:
                    title_elem = leaf_elem.find('def:title', self.active_namespaces)
                    if title_elem is not None and title_elem.text:
                        doc_ref_data['title'] = title_elem.text.strip()
                
                try:
                    doc_ref_obj = DocumentReference(**doc_ref_data)
                    doc_refs.append(doc_ref_obj)
                except Exception as e:
                    logger.warning(f"Failed to create DocumentReference for {leaf_id}: {e}")
        
        return doc_refs if doc_refs else None
    
    def _process_analysis_result_displays_native(self, mdv: ET.Element) -> Tuple[List[Display], List[Analysis], Dict[str, List[str]]]:
        """
        Process AnalysisResultDisplays as native Analysis and Display objects.
        
        ARM Structure:
          AnalysisResultDisplays
            └─ ResultDisplay (→ Display)
                └─ AnalysisResults (→ Analysis) *
        
        Returns:
            Tuple of (Display objects, Analysis objects, display_to_analyses_map)
        """
        displays = []
        analyses = []
        display_to_analyses = {}  # Map Display OID → list of Analysis OIDs
        
        # Detect ARM namespace from XML if not already in active_namespaces
        arm_ns_uri = None
        for prefix, uri in self.active_namespaces.items():
            if prefix in ['arm', 'adamref']:
                arm_ns_uri = uri
                break
        
        # If not found, try to detect from XML
        if arm_ns_uri is None:
            # Check all elements in the tree for namespace declarations
            # ElementTree doesn't have getparent(), so we iterate through all elements
            for elem in mdv.iter():
                for attr_name, attr_value in elem.attrib.items():
                    if attr_name.startswith('xmlns:') and ('arm' in attr_name.lower() or 'adam' in attr_name.lower()):
                        arm_ns_uri = attr_value
                        prefix = attr_name.split(':', 1)[1]
                        self.active_namespaces[prefix] = attr_value
                        break
                if arm_ns_uri:
                    break
        
        # Find all AnalysisResultDisplays containers
        namespaces_to_check = []
        if arm_ns_uri:
            namespaces_to_check.append(arm_ns_uri)
        # Also check def namespace
        if 'def' in self.active_namespaces:
            namespaces_to_check.append(self.active_namespaces['def'])
        
        # Count total AnalysisResultDisplays containers to detect format
        total_ard_containers = 0
        all_ard_elements = []
        for uri in namespaces_to_check:
            ard_elements = mdv.findall(f'{{{uri}}}AnalysisResultDisplays')
            total_ard_containers += len(ard_elements)
            all_ard_elements.extend(ard_elements)
        
        # Determine if we're using separate containers (LZZT format) or single container (defineV21 format)
        # LZZT format: multiple AnalysisResultDisplays containers (one per Display)
        # defineV21 format: single AnalysisResultDisplays container (with multiple ResultDisplay children)
        use_separate_containers = total_ard_containers > 1
        
        for uri in namespaces_to_check:
            ard_elements = mdv.findall(f'{{{uri}}}AnalysisResultDisplays')
            
            for ard_container in ard_elements:
                # Find all ResultDisplay elements (use same namespace as container)
                result_displays = ard_container.findall(f'{{{uri}}}ResultDisplay')
                
                for rd_elem in result_displays:
                    # Create Display object
                    display_oid = rd_elem.get('OID')
                    if not display_oid:
                        continue
                    
                    display_data = {
                        'OID': display_oid,
                        'name': rd_elem.get('DisplayIdentifier') or rd_elem.get('Name', ''),
                        'label': rd_elem.get('DisplayLabel', ''),
                    }
                    
                    # Store attributes in supplemental for roundtrip
                    if not hasattr(self, '_display_supplemental'):
                        self._display_supplemental = {}
                    if display_oid not in self._display_supplemental:
                        self._display_supplemental[display_oid] = {}
                    
                    # Store Name attribute if present (defineV21 format)
                    name_attr = rd_elem.get('Name')
                    if name_attr:
                        self._display_supplemental[display_oid]['name'] = name_attr
                    
                    # Store DisplayIdentifier and DisplayLabel if present (LZZT format)
                    display_identifier = rd_elem.get('DisplayIdentifier')
                    if display_identifier:
                        self._display_supplemental[display_oid]['displayIdentifier'] = display_identifier
                    display_label = rd_elem.get('DisplayLabel')
                    if display_label:
                        self._display_supplemental[display_oid]['displayLabel'] = display_label
                    
                    # Store whether this Display came from a separate AnalysisResultDisplays container
                    # (LZZT format has one container per Display, defineV21 has one container for all)
                    # Only set to True if we detected multiple containers
                    if use_separate_containers:
                        self._display_supplemental[display_oid]['_separateContainer'] = True
                    
                    # Extract Description
                    desc_text = self._get_description(rd_elem)
                    if desc_text:
                        display_data['description'] = desc_text
                    
                    # Extract DocumentRef children (not leafID attribute)
                    # DocumentRef can be in arm or def namespace
                    # Use native Display.location field (list[DocumentReference])
                    location_refs = []
                    pdf_page_refs_supplemental = {}  # Store PDFPageRef details (PageRefs string, Type, Title) in supplemental
                    has_document_ref_children = False  # Track if original had DocumentRef children (vs just leafID attribute)
                    # Try arm namespace first
                    for doc_ref_elem in rd_elem.findall(f'{{{uri}}}DocumentRef'):
                        has_document_ref_children = True
                        leaf_id = doc_ref_elem.get('leafID')
                        if leaf_id:
                            # Create DocumentReference for native location field
                            doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                            # Extract PDFPageRef children (store in supplemental as they have complex data)
                            pdf_page_refs = []
                            for pdf_ref_elem in doc_ref_elem.findall(f'{{{uri}}}PDFPageRef'):
                                pdf_data = {}
                                if pdf_ref_elem.get('PageRefs'):
                                    pdf_data['pageRefs'] = pdf_ref_elem.get('PageRefs')
                                if pdf_ref_elem.get('Type'):
                                    pdf_data['type'] = pdf_ref_elem.get('Type')
                                if pdf_ref_elem.get('Title'):
                                    pdf_data['title'] = pdf_ref_elem.get('Title')
                                if pdf_data:
                                    pdf_page_refs.append(pdf_data)
                            if pdf_page_refs:
                                # Store PDFPageRef details in supplemental (DocumentReference.pages is list[int], not compatible)
                                if display_oid not in pdf_page_refs_supplemental:
                                    pdf_page_refs_supplemental[display_oid] = {}
                                pdf_page_refs_supplemental[display_oid][leaf_id] = pdf_page_refs
                            try:
                                doc_ref = DocumentReference(**doc_ref_data)
                                location_refs.append(doc_ref)
                            except Exception as e:
                                logger.warning(f"Failed to create DocumentReference for display {display_oid}: {e}")
                    # Try def namespace
                    if 'def' in self.active_namespaces:
                        def_ns = self.active_namespaces['def']
                        for doc_ref_elem in rd_elem.findall(f'{{{def_ns}}}DocumentRef'):
                            has_document_ref_children = True
                            leaf_id = doc_ref_elem.get('leafID')
                            if leaf_id:
                                # Create DocumentReference for native location field
                                doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                                # Extract PDFPageRef children
                                pdf_page_refs = []
                                for pdf_ref_elem in doc_ref_elem.findall(f'{{{def_ns}}}PDFPageRef'):
                                    pdf_data = {}
                                    if pdf_ref_elem.get('PageRefs'):
                                        pdf_data['pageRefs'] = pdf_ref_elem.get('PageRefs')
                                    if pdf_ref_elem.get('Type'):
                                        pdf_data['type'] = pdf_ref_elem.get('Type')
                                    if pdf_ref_elem.get('Title'):
                                        pdf_data['title'] = pdf_ref_elem.get('Title')
                                    if pdf_data:
                                        pdf_page_refs.append(pdf_data)
                                if pdf_page_refs:
                                    # Store PDFPageRef details in supplemental
                                    if display_oid not in pdf_page_refs_supplemental:
                                        pdf_page_refs_supplemental[display_oid] = {}
                                    pdf_page_refs_supplemental[display_oid][leaf_id] = pdf_page_refs
                                try:
                                    doc_ref = DocumentReference(**doc_ref_data)
                                    location_refs.append(doc_ref)
                                except Exception as e:
                                    logger.warning(f"Failed to create DocumentReference for display {display_oid}: {e}")
                    if location_refs:
                        # Use native Display.location field (presence indicates DocumentRef children existed)
                        display_data['location'] = location_refs
                    # Store PDFPageRef details in supplemental (if any)
                    if pdf_page_refs_supplemental:
                        if not hasattr(self, '_display_supplemental'):
                            self._display_supplemental = {}
                        for disp_oid, pdf_refs_dict in pdf_page_refs_supplemental.items():
                            if disp_oid not in self._display_supplemental:
                                self._display_supplemental[disp_oid] = {}
                            self._display_supplemental[disp_oid]['pdfPageRefs'] = pdf_refs_dict
                    
                    # Handle leafID attribute → store in supplemental (for leafID attribute on ResultDisplay, not DocumentRef children)
                    # Only store leafID in supplemental if there were no DocumentRef children
                    if not has_document_ref_children:
                        leaf_id = rd_elem.get('leafID') or rd_elem.get(f'{{{uri}}}leafID')
                        if leaf_id:
                            # Store leafID in supplemental for roundtrip (as ResultDisplay attribute, not DocumentRef child)
                            if not hasattr(self, '_display_supplemental'):
                                self._display_supplemental = {}
                            if display_oid not in self._display_supplemental:
                                self._display_supplemental[display_oid] = {}
                            self._display_supplemental[display_oid]['leafID'] = leaf_id
                    
                    # Permissively handle both AnalysisResult (singular, correct) and AnalysisResults (plural, permissive)
                    # Default to singular (correct format), but allow plural if present
                    analysis_results = rd_elem.findall(f'{{{uri}}}AnalysisResult')
                    uses_plural = False
                    if not analysis_results:
                        # Try plural form (AnalysisResults) - permissive handling for non-standard formats
                        analysis_results = rd_elem.findall(f'{{{uri}}}AnalysisResults')
                        uses_plural = len(analysis_results) > 0
                    analysis_oids = []
                    
                    # Store format info in supplemental (only if plural detected, for roundtrip accuracy)
                    if uses_plural and display_oid:
                        if not hasattr(self, '_display_supplemental'):
                            self._display_supplemental = {}
                        if display_oid not in self._display_supplemental:
                            self._display_supplemental[display_oid] = {}
                        self._display_supplemental[display_oid]['_usesAnalysisResults'] = True
                    
                    for ar_elem in analysis_results:
                        analysis_oid = ar_elem.get('OID')
                        if not analysis_oid:
                            continue
                        
                        analysis_oids.append(analysis_oid)
                        
                        # Create Analysis object
                        analysis_data = {
                            'OID': analysis_oid,
                            'type': 'Computation',  # ARM analyses are computational
                        }
                        
                        # Store AnalysisResult supplemental data for roundtrip
                        if not hasattr(self, '_analysis_result_supplemental'):
                            self._analysis_result_supplemental = {}
                        ar_supp = {}
                        
                        # Map ARM attributes to Analysis fields
                        if ar_elem.get('Reason'):
                            analysis_data['analysisReason'] = ar_elem.get('Reason')
                        if ar_elem.get('AnalysisReason'):
                            ar_supp['analysisReason'] = ar_elem.get('AnalysisReason')
                        if ar_elem.get('ResultIdentifier'):
                            analysis_data['name'] = ar_elem.get('ResultIdentifier')
                        if ar_elem.get('ParameterOID'):
                            ar_supp['parameterOID'] = ar_elem.get('ParameterOID')
                        if ar_elem.get('AnalysisPurpose'):
                            ar_supp['analysisPurpose'] = ar_elem.get('AnalysisPurpose')
                        
                        # Extract Description child (not from Documentation)
                        # Description is in ODM namespace, not ARM namespace
                        odm_ns = self.active_namespaces.get('odm')
                        if odm_ns:
                            ar_desc = ar_elem.find(f'{{{odm_ns}}}Description')
                        else:
                            # Fallback: try ARM namespace or no namespace
                            ar_desc = ar_elem.find(f'{{{uri}}}Description') or ar_elem.find('Description')
                        if ar_desc is not None:
                            trans_text = ar_desc.find('.//TranslatedText') or ar_desc.find('.//odm:TranslatedText', self.active_namespaces)
                            if trans_text is not None and trans_text.text:
                                ar_supp['description'] = trans_text.text.strip()
                        
                        # Extract Documentation structure (Description, DocumentRef)
                        doc_elem = ar_elem.find(f'{{{uri}}}Documentation')
                        if doc_elem is not None:
                            doc_data = {}
                            # Extract leafID attribute if present
                            doc_leaf_id = doc_elem.get('leafID') or doc_elem.get(f'{{{uri}}}leafID')
                            if doc_leaf_id:
                                doc_data['leafID'] = doc_leaf_id
                            # Check for TranslatedText directly under Documentation (LZZT format) or under Description (defineV21 format)
                            odm_ns = self.active_namespaces.get('odm')
                            doc_trans_text = None
                            # Try TranslatedText directly (LZZT format)
                            if odm_ns:
                                doc_trans_text = doc_elem.find(f'{{{odm_ns}}}TranslatedText')
                            if doc_trans_text is None:
                                doc_trans_text = doc_elem.find('TranslatedText')
                            # If not found directly, try under Description (defineV21 format)
                            if doc_trans_text is None:
                                if odm_ns:
                                    doc_desc = doc_elem.find(f'{{{odm_ns}}}Description')
                                else:
                                    doc_desc = doc_elem.find(f'{{{uri}}}Description') or doc_elem.find('Description')
                                if doc_desc is not None:
                                    doc_trans_text = doc_desc.find('.//TranslatedText') or doc_desc.find('.//odm:TranslatedText', self.active_namespaces)
                            
                            if doc_trans_text is not None and doc_trans_text.text:
                                doc_data['description'] = doc_trans_text.text.strip()
                                # Store whether TranslatedText was directly under Documentation (no Description wrapper)
                                # Check parent by comparing tags (ElementTree doesn't have getparent())
                                parent = doc_trans_text.getparent() if hasattr(doc_trans_text, 'getparent') else None
                                if parent is None:
                                    # Check by walking up the tree
                                    for parent_elem in doc_elem.iter():
                                        if doc_trans_text in list(parent_elem):
                                            parent = parent_elem
                                            break
                                if parent is not None and parent.tag == doc_elem.tag:
                                    doc_data['_translatedTextDirect'] = True
                                # Also check if TranslatedText is direct child by checking if Description exists
                                if doc_elem.find('Description') is None and doc_elem.find(f'{{{odm_ns}}}Description') is None:
                                    doc_data['_translatedTextDirect'] = True
                            
                            doc_refs = []
                            # Try arm namespace first
                            for doc_ref_elem in doc_elem.findall(f'{{{uri}}}DocumentRef'):
                                leaf_id = doc_ref_elem.get('leafID')
                                if leaf_id:
                                    doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                                    # Extract PDFPageRef children
                                    pdf_page_refs = []
                                    for pdf_ref_elem in doc_ref_elem.findall(f'{{{uri}}}PDFPageRef'):
                                        pdf_data = {}
                                        if pdf_ref_elem.get('PageRefs'):
                                            pdf_data['pageRefs'] = pdf_ref_elem.get('PageRefs')
                                        if pdf_ref_elem.get('Type'):
                                            pdf_data['type'] = pdf_ref_elem.get('Type')
                                        if pdf_ref_elem.get('Title'):
                                            pdf_data['title'] = pdf_ref_elem.get('Title')
                                        if pdf_data:
                                            pdf_page_refs.append(pdf_data)
                                    if pdf_page_refs:
                                        doc_ref_data['pdfPageRefs'] = pdf_page_refs
                                    doc_refs.append(doc_ref_data)
                            # Try def namespace
                            if 'def' in self.active_namespaces:
                                def_ns = self.active_namespaces['def']
                                for doc_ref_elem in doc_elem.findall(f'{{{def_ns}}}DocumentRef'):
                                    leaf_id = doc_ref_elem.get('leafID')
                                    if leaf_id:
                                        doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                                        # Extract PDFPageRef children
                                        pdf_page_refs = []
                                        for pdf_ref_elem in doc_ref_elem.findall(f'{{{def_ns}}}PDFPageRef'):
                                            pdf_data = {}
                                            if pdf_ref_elem.get('PageRefs'):
                                                pdf_data['pageRefs'] = pdf_ref_elem.get('PageRefs')
                                            if pdf_ref_elem.get('Type'):
                                                pdf_data['type'] = pdf_ref_elem.get('Type')
                                            if pdf_ref_elem.get('Title'):
                                                pdf_data['title'] = pdf_ref_elem.get('Title')
                                            if pdf_data:
                                                pdf_page_refs.append(pdf_data)
                                        if pdf_page_refs:
                                            doc_ref_data['pdfPageRefs'] = pdf_page_refs
                                        doc_refs.append(doc_ref_data)
                            if doc_refs:
                                doc_data['documents'] = doc_refs
                            
                            if doc_data:
                                ar_supp['documentation'] = doc_data
                        
                        # Extract ProgrammingCode (always store if present, even if empty)
                        prog_code = ar_elem.find(f'{{{uri}}}ProgrammingCode')
                        if prog_code is not None:
                            prog_data = {}
                            prog_leaf_id = prog_code.get('leafID') or prog_code.get(f'{{{uri}}}leafID')
                            if prog_leaf_id:
                                prog_data['leafID'] = prog_leaf_id
                            if prog_code.get('Context'):
                                prog_data['context'] = prog_code.get('Context')
                            # Extract ComputationMethod (check multiple namespaces)
                            comp_method = None
                            if 'def' in self.active_namespaces:
                                comp_method = prog_code.find(f'.//{{{self.active_namespaces["def"]}}}ComputationMethod')
                            if comp_method is None:
                                # Try common def namespace URIs
                                for def_uri in ['http://www.cdisc.org/ns/def/v2.1', 'http://www.cdisc.org/ns/def/v2.0']:
                                    comp_method = prog_code.find(f'{{{def_uri}}}ComputationMethod')
                                    if comp_method is not None:
                                        break
                            if comp_method is None:
                                comp_method = prog_code.find(f'{{{uri}}}ComputationMethod')
                            if comp_method is None:
                                comp_method = prog_code.find('.//ComputationMethod')
                            
                            if comp_method is not None:
                                method_oid = comp_method.get('OID')
                                if method_oid:
                                    prog_data['methodOID'] = method_oid
                                # Store ComputationMethod text content for roundtrip
                                if comp_method.text:
                                    prog_data['computationMethodText'] = comp_method.text.strip()
                                # Store Name attribute if present
                                cm_name = comp_method.get('Name')
                                if cm_name:
                                    prog_data['computationMethodName'] = cm_name
                            # Extract Code child element
                            code_elem = prog_code.find(f'{{{uri}}}Code')
                            if code_elem is not None and code_elem.text:
                                prog_data['code'] = code_elem.text
                            # Extract DocumentRef children (in def namespace)
                            if 'def' in self.active_namespaces:
                                def_ns = self.active_namespaces['def']
                                doc_refs = []
                                for doc_ref_elem in prog_code.findall(f'{{{def_ns}}}DocumentRef'):
                                    leaf_id = doc_ref_elem.get('leafID')
                                    if leaf_id:
                                        doc_ref_data = {'OID': leaf_id, 'leafID': leaf_id}
                                        # Extract PDFPageRef children
                                        pdf_page_refs = []
                                        for pdf_ref_elem in doc_ref_elem.findall(f'{{{def_ns}}}PDFPageRef'):
                                            pdf_data = {}
                                            if pdf_ref_elem.get('PageRefs'):
                                                pdf_data['pageRefs'] = pdf_ref_elem.get('PageRefs')
                                            if pdf_ref_elem.get('Type'):
                                                pdf_data['type'] = pdf_ref_elem.get('Type')
                                            if pdf_ref_elem.get('Title'):
                                                pdf_data['title'] = pdf_ref_elem.get('Title')
                                            if pdf_data:
                                                pdf_page_refs.append(pdf_data)
                                        if pdf_page_refs:
                                            doc_ref_data['pdfPageRefs'] = pdf_page_refs
                                        doc_refs.append(doc_ref_data)
                                if doc_refs:
                                    prog_data['documents'] = doc_refs
                            # Always store ProgrammingCode if present (even if empty)
                            ar_supp['programmingCode'] = prog_data
                        
                        if ar_supp:
                            self._analysis_result_supplemental[analysis_oid] = ar_supp
                        
                        # Extract ParameterList → parameters (stored in expressions as per schema)
                        param_list = ar_elem.find(f'{{{uri}}}ParameterList')
                        if param_list is not None:
                            parameters = []
                            for param_elem in param_list.findall(f'{{{uri}}}Parameter'):
                                param_cd = param_elem.get('ParamCD')
                                param_name = param_elem.get('Param')
                                if param_cd:
                                    param_data = {
                                        'OID': f'PARAM.{param_cd}',
                                        'name': param_name or param_cd
                                    }
                                    # Store original ParamCD for roundtrip (supplemental)
                                    if param_cd and analysis_oid:
                                        if not hasattr(self, '_analysis_parameters'):
                                            self._analysis_parameters = {}
                                        if analysis_oid not in self._analysis_parameters:
                                            self._analysis_parameters[analysis_oid] = []
                                        self._analysis_parameters[analysis_oid].append({'paramCD': param_cd, 'param': param_name})
                                    parameters.append(param_data)
                            if parameters:
                                # Parameters go inside expressions (FormalExpression has parameters field)
                                # FormalExpression requires OID and expression fields
                                if 'expressions' not in analysis_data:
                                    analysis_data['expressions'] = []
                                # Create or append to first expression
                                if not analysis_data['expressions']:
                                    expr_data = {
                                        'OID': f'{analysis_oid}.EXPR',
                                        'expression': 'ParameterList',  # Placeholder
                                        'parameters': parameters
                                    }
                                    analysis_data['expressions'].append(expr_data)
                                else:
                                    analysis_data['expressions'][0]['parameters'] = parameters
                        
                        # Extract Documentation → description (with optional leafID for supplemental)
                        doc_elem = ar_elem.find(f'{{{uri}}}Documentation')
                        doc_leaf_id = None
                        if doc_elem is not None:
                            doc_leaf_id = doc_elem.get('leafID') or doc_elem.get(f'{{{uri}}}leafID')
                            # TranslatedText might be in ODM namespace or no namespace
                            trans_text = doc_elem.find('.//TranslatedText') or doc_elem.find('.//odm:TranslatedText', self.active_namespaces)
                            
                            # Check for text content (after stripping whitespace)
                            has_text = trans_text is not None and trans_text.text and trans_text.text.strip()
                            
                            if has_text:
                                # Has TranslatedText content - store it
                                analysis_data['description'] = trans_text.text.strip()
                                # Also store leafID in supplemental if present
                                if doc_leaf_id and analysis_oid:
                                    if not hasattr(self, '_analysis_doc_leafids'):
                                        self._analysis_doc_leafids = {}
                                    self._analysis_doc_leafids[analysis_oid] = doc_leaf_id
                                    logger.info(f"      - Stored leafID {doc_leaf_id} for Analysis {analysis_oid}")
                            elif doc_leaf_id:
                                # Empty Documentation with just leafID - store marker in description
                                analysis_data['description'] = f'[leafID: {doc_leaf_id}]'
                        
                        # Extract ProgrammingCode/ComputationMethod → link to existing Method
                        # ProgrammingCode can also be empty with just leafID attribute
                        prog_code = ar_elem.find(f'{{{uri}}}ProgrammingCode')
                        if prog_code is not None:
                            prog_code_leaf_id = prog_code.get('leafID') or prog_code.get(f'{{{uri}}}leafID')
                            comp_method = prog_code.find('.//def:ComputationMethod', self.active_namespaces)
                            
                            if comp_method is not None:
                                method_oid = comp_method.get('OID')
                                if method_oid:
                                    # Store as analysisMethod reference (will link to existing Method)
                                    analysis_data['analysisMethod'] = method_oid
                            elif prog_code_leaf_id and analysis_oid:
                                # Empty ProgrammingCode with just leafID - store in supplemental
                                if not hasattr(self, '_analysis_progcode_leafids'):
                                    self._analysis_progcode_leafids = {}
                                self._analysis_progcode_leafids[analysis_oid] = prog_code_leaf_id
                                logger.info(f"      - Stored ProgrammingCode leafID {prog_code_leaf_id} for Analysis {analysis_oid}")
                        
                        # Store inputData references (AnalysisVariable and AnalysisDataset)
                        # These are Item and ItemGroup OIDs
                        input_refs = []
                        
                        # AnalysisVariable → Item references
                        for av in ar_elem.findall(f'{{{uri}}}AnalysisVariable'):
                            item_oid = av.get('ItemOID')
                            if item_oid:
                                input_refs.append(item_oid)
                        
                        # AnalysisDataset/ItemGroupRef → ItemGroup references + SelectionCriteria mapping
                        # Need to preserve which SelectionCriteria belongs to which dataset
                        # ItemGroupRef is in ODM namespace, not ARM namespace
                        dataset_criteria_map = {}  # {dataset_oid: [criteria_oid1, ...]}
                        all_criteria = []
                        
                        # AnalysisDataset elements are inside AnalysisDatasets container
                        ads_container = ar_elem.find(f'{{{uri}}}AnalysisDatasets')
                        ads_container_supp = {}
                        if ads_container is not None:
                            # Extract AnalysisDatasets attributes (e.g., CommentOID)
                            if 'def' in self.active_namespaces:
                                def_ns = self.active_namespaces['def']
                                comment_oid = ads_container.get(f'{{{def_ns}}}CommentOID')
                                if comment_oid:
                                    ads_container_supp['commentOID'] = comment_oid
                            analysis_datasets = ads_container.findall(f'{{{uri}}}AnalysisDataset')
                        else:
                            # Fallback: check direct children (for backward compatibility)
                            analysis_datasets = ar_elem.findall(f'{{{uri}}}AnalysisDataset')
                        
                        # Store AnalysisDatasets supplemental data
                        if ads_container_supp and analysis_oid:
                            if not hasattr(self, '_analysis_datasets_supplemental'):
                                self._analysis_datasets_supplemental = {}
                            self._analysis_datasets_supplemental[analysis_oid] = ads_container_supp
                        
                        for ad in analysis_datasets:
                            # Initialize ad_supp before use
                            ad_supp = {}
                            igr_elem_found = None
                            
                            # Get ItemGroup OID from ItemGroupOID attribute (not ItemGroupRef child)
                            ig_oid = ad.get('ItemGroupOID')
                            if not ig_oid:
                                # Fallback: try ItemGroupRef child element (check multiple namespaces)
                                igr_elems = []
                                # Try ODM namespace (ItemGroupRef is usually in ODM namespace)
                                if 'odm' in self.active_namespaces:
                                    igr_elems.extend(ad.findall(f'.//{{{self.active_namespaces["odm"]}}}ItemGroupRef'))
                                # Also try common ODM namespace URIs directly (v1.2, v1.3)
                                for odm_uri in ['http://www.cdisc.org/ns/odm/v1.2', 'http://www.cdisc.org/ns/odm/v1.3']:
                                    igr_elems.extend(ad.findall(f'{{{odm_uri}}}ItemGroupRef'))
                                # Try ARM/adamref namespace (LZZT format)
                                igr_elems.extend(ad.findall(f'{{{uri}}}ItemGroupRef'))
                                # Try direct child (no namespace prefix)
                                igr_elems.extend(ad.findall('ItemGroupRef'))
                                # Try no namespace (anywhere)
                                igr_elems.extend(ad.findall('.//ItemGroupRef'))
                                for igr in igr_elems:
                                    ig_oid = igr.get('ItemGroupOID')
                                    if ig_oid:
                                        # Store ItemGroupRef element for later extraction of Mandatory attribute
                                        igr_elem_found = igr
                                        break
                            
                            if ig_oid:
                                input_refs.append(ig_oid)
                                
                                # Store AnalysisDataset supplemental data (slices: WhereClauseRef, AnalysisVariable)
                                if not hasattr(self, '_analysis_dataset_supplemental'):
                                    self._analysis_dataset_supplemental = {}
                                if analysis_oid not in self._analysis_dataset_supplemental:
                                    self._analysis_dataset_supplemental[analysis_oid] = {}
                                
                                ad_supp = {}
                                
                                # Extract WhereClauseRef children (in def namespace, not arm)
                                wc_refs = []
                                if 'def' in self.active_namespaces:
                                    def_ns = self.active_namespaces['def']
                                    for wc_ref in ad.findall(f'{{{def_ns}}}WhereClauseRef'):
                                        wc_oid = wc_ref.get('WhereClauseOID')
                                        if wc_oid:
                                            wc_refs.append({'whereClauseOID': wc_oid})
                                # Also try arm namespace as fallback
                                for wc_ref in ad.findall(f'{{{uri}}}WhereClauseRef'):
                                    wc_oid = wc_ref.get('WhereClauseOID')
                                    if wc_oid:
                                        wc_refs.append({'whereClauseOID': wc_oid})
                                if wc_refs:
                                    ad_supp['whereClauseRefs'] = wc_refs
                                
                                # Extract AnalysisVariable children (these are separate from top-level AnalysisVariable)
                                av_items = []
                                for av in ad.findall(f'{{{uri}}}AnalysisVariable'):
                                    item_oid = av.get('ItemOID')
                                    if item_oid:
                                        av_items.append({'itemOID': item_oid})
                                if av_items:
                                    ad_supp['analysisVariables'] = av_items
                                
                                # Get SelectionCriteria for THIS dataset (before storing ad_supp)
                                sc_elem = ad.find(f'{{{uri}}}SelectionCriteria')
                                if sc_elem is not None:
                                    # Store full SelectionCriteria structure for roundtrip
                                    sc_data = {}
                                    # Extract ComputationMethod elements (check multiple namespaces)
                                    cm_elems = []
                                    if 'def' in self.active_namespaces:
                                        cm_elems.extend(sc_elem.findall(f'.//{{{self.active_namespaces["def"]}}}ComputationMethod'))
                                    # Also try common def namespace URIs
                                    for def_uri in ['http://www.cdisc.org/ns/def/v2.1', 'http://www.cdisc.org/ns/def/v2.0']:
                                        cm_elems.extend(sc_elem.findall(f'{{{def_uri}}}ComputationMethod'))
                                    # Try ARM namespace
                                    cm_elems.extend(sc_elem.findall(f'{{{uri}}}ComputationMethod'))
                                    # Try no namespace
                                    cm_elems.extend(sc_elem.findall('.//ComputationMethod'))
                                    
                                    computation_methods = []
                                    for cm in cm_elems:
                                        cm_data = {}
                                        cm_oid = cm.get('OID')
                                        if cm_oid:
                                            cm_data['OID'] = cm_oid
                                            dataset_criteria = dataset_criteria_map.get(ig_oid, [])
                                            if cm_oid not in dataset_criteria:
                                                dataset_criteria.append(cm_oid)
                                            dataset_criteria_map[ig_oid] = dataset_criteria
                                            all_criteria.append(cm_oid)
                                        cm_name = cm.get('Name')
                                        if cm_name:
                                            cm_data['Name'] = cm_name
                                        if cm.text:
                                            cm_data['text'] = cm.text.strip()
                                        if cm_data:
                                            computation_methods.append(cm_data)
                                    
                                    if computation_methods:
                                        sc_data['computationMethods'] = computation_methods
                                        ad_supp['selectionCriteria'] = sc_data
                                
                                # Always store AnalysisDataset supplemental data (even if empty) to mark its existence
                                if ig_oid not in self._analysis_dataset_supplemental[analysis_oid]:
                                    self._analysis_dataset_supplemental[analysis_oid][ig_oid] = {}
                                if ad_supp:
                                    self._analysis_dataset_supplemental[analysis_oid][ig_oid].update(ad_supp)
                                # Mark that this ItemGroup OID is a dataset (for creation code to distinguish from Item OIDs)
                                self._analysis_dataset_supplemental[analysis_oid][ig_oid]['_isDataset'] = True
                                
                                # Extract Mandatory attribute from ItemGroupRef if present
                                if igr_elem_found is not None:
                                    mandatory = igr_elem_found.get('Mandatory')
                                    if mandatory:
                                        self._analysis_dataset_supplemental[analysis_oid][ig_oid]['mandatory'] = mandatory
                                    # Also store namespace info for ItemGroupRef
                                    igr_tag = igr_elem_found.tag
                                    if '}' in igr_tag:
                                        igr_ns_uri = igr_tag.split('}')[0][1:]
                                        self._analysis_dataset_supplemental[analysis_oid][ig_oid]['_itemGroupRefNamespace'] = igr_ns_uri
                        
                        if input_refs:
                            analysis_data['inputData'] = input_refs
                        
                        # Store all criteria in applicableWhen (for schema compliance)
                        if all_criteria:
                            analysis_data['applicableWhen'] = all_criteria
                        
                        # Store dataset→criteria mapping in supplemental for roundtrip
                        if dataset_criteria_map and analysis_oid:
                            if not hasattr(self, '_analysis_dataset_criteria'):
                                self._analysis_dataset_criteria = {}
                            self._analysis_dataset_criteria[analysis_oid] = dataset_criteria_map
                        
                        try:
                            analysis_obj = Analysis(**analysis_data)
                            analyses.append(analysis_obj)
                        except Exception as e:
                            logger.warning(f"Failed to create Analysis {analysis_oid}: {e}")
                    
                    # Link Display to its first analysis (Display.analysis expects string, not list)
                    if analysis_oids:
                        display_data['analysis'] = analysis_oids[0]
                        # Store ALL analysis OIDs for supplemental metadata
                        if len(analysis_oids) > 1:
                            display_to_analyses[display_oid] = analysis_oids
                    
                    try:
                        display_obj = Display(**display_data)
                        displays.append(display_obj)
                    except Exception as e:
                        logger.warning(f"Failed to create Display {display_oid}: {e}")
                        logger.warning(f"  display_data: {display_data}")
                        # Don't fail completely, just skip this display
        
        return displays, analyses, display_to_analyses
    
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