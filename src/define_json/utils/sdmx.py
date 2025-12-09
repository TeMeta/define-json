"""
SDMX data cube utilities for Define-JSON IR.

Provides:
- Policy-driven classification of Items into Dimension/Measure/Attribute roles
- DataStructureDefinition building
- WhereClause → GroupKey derivation
- Attribute relationship inference
"""

from pathlib import Path
from typing import Dict, Any, Tuple, List, Set, Optional
from datetime import datetime
import yaml
import logging

from ..schema.define import (
    MetaDataVersion,
    ItemGroup,
    Item,
    Dimension,
    Measure,
    DataAttribute,
    ItemGroupType,
    WhereClause,
    Condition,
    RangeCheck,
    GroupKey,
    Comparator,
)

logger = logging.getLogger(__name__)


def load_data_cube_config(path: Path) -> Dict[str, Any]:
    """
    Load and validate data cube configuration file.
    
    Configuration file structure:
    ```yaml
    domain: LB
    dimensions: [USUBJID, LBTEST, VISITNUM, LBSEQ]
    measures: [LBSTRESN, LBSTRESC]
    attributes:
      dataset_level: [STUDYID, DOMAIN]
      dimension_level:
        - variable: LBCAT
          attached_to: [LBTEST]
      measure_level:
        - variable: LBSTRESU
          attached_to: [LBSTRESN]
    dimension_order: [USUBJID, LBTEST, VISITNUM, LBSEQ]
    ```
    
    Args:
        path: Path to YAML configuration file
        
    Returns:
        Parsed configuration dictionary
        
    Raises:
        ValueError: If configuration is malformed or missing required fields
    """
    if not path.exists():
        raise ValueError(f"Data cube configuration file not found: {path}")
    
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate required fields
    if "domain" not in config:
        raise ValueError("Configuration must specify 'domain'")
    if "dimensions" not in config:
        raise ValueError("Configuration must specify 'dimensions' list")
    if "measures" not in config:
        raise ValueError("Configuration must specify 'measures' list")
    
    return config


# Backward compatibility alias
def load_sdmx_policy(path: Path) -> Dict[str, Any]:
    """
    Deprecated: Use load_data_cube_config() instead.
    
    This function is kept for backward compatibility with existing tests.
    """
    return load_data_cube_config(path)


def classify_item_role(variable_name: str, config: Dict[str, Any]) -> str:
    """
    Classify a variable into Dimension/Measure/Attribute role based on data cube configuration.
    
    Args:
        variable_name: Name of the variable (e.g., "USUBJID")
        config: Loaded data cube configuration dictionary
        
    Returns:
        Role as string: "Dimension", "Measure", or "Attribute"
        
    Raises:
        ValueError: If variable is not classified in configuration (fail fast)
    """
    # Check dimensions
    if variable_name in config.get("dimensions", []):
        return "Dimension"
    
    # Check measures
    if variable_name in config.get("measures", []):
        return "Measure"
    
    # Check attributes (all levels)
    attributes = config.get("attributes", {})
    
    # Dataset-level attributes
    if variable_name in attributes.get("dataset_level", []):
        return "Attribute"
    
    # Dimension-level attributes
    for attr_spec in attributes.get("dimension_level", []):
        if isinstance(attr_spec, dict) and attr_spec.get("variable") == variable_name:
            return "Attribute"
    
    # Measure-level attributes
    for attr_spec in attributes.get("measure_level", []):
        if isinstance(attr_spec, dict) and attr_spec.get("variable") == variable_name:
            return "Attribute"
    
    # If we reach here, variable is not classified
    raise ValueError(
        f"Variable '{variable_name}' not classified in configuration. "
        f"Configuration must explicitly classify all variables as Dimension, Measure, or Attribute."
    )


def build_dsd_for_domain(
    mdv: MetaDataVersion,
    domain: str,
    config: Dict[str, Any]
) -> ItemGroup:
    """
    Build DataStructureDefinition for a domain using configuration-driven classification.
    
    Creates an ItemGroup with type="DataCube" containing:
    - Dimension components (from config.dimensions)
    - Measure components (from config.measures)
    - DataAttribute components (from config.attributes)
    
    Args:
        mdv: MetaDataVersion containing Items and ItemGroups
        domain: Domain code (e.g., "LB")
        config: Data cube configuration dictionary from load_data_cube_config()
        
    Returns:
        ItemGroup with itemGroupType="DataCube" representing the DSD
        
    Raises:
        ValueError: If domain not found or configuration doesn't match domain
    """
    if config["domain"] != domain:
        raise ValueError(
            f"Configuration domain '{config['domain']}' does not match requested domain '{domain}'"
        )
    
    # Find the domain ItemGroup
    domain_group = None
    for ig in mdv.itemGroups or []:
        if ig.domain == domain:
            domain_group = ig
            break
    
    if not domain_group:
        raise ValueError(f"Domain '{domain}' not found in MetaDataVersion")
    
    # Build DSD ItemGroup using model_construct to handle required fields
    dsd = ItemGroup.model_construct(
        OID=f"DSD.{domain}",
        name=f"{domain} Data Structure Definition",
        domain=domain,
        type=ItemGroupType.DataCube,  # Correct field name is 'type', not 'itemGroupType'
        purpose="Tabulation",
        lastUpdated=datetime.now(),  # Required field
        items=[]
    )
    
    # Helper: Find Item by name in MDV (check both top-level items and ItemGroup items)
    def find_item_by_name(name: str) -> Optional[Item]:
        # First check top-level items
        for item in mdv.items or []:
            if item.name == name:
                return item
        # Then check items in ItemGroups (especially the domain ItemGroup)
        for ig in mdv.itemGroups or []:
            if ig.items:
                for item in ig.items:
                    if isinstance(item, Item) and item.name == name:
                        return item
        return None
    
    # Add Dimension components
    for dim_name in config.get("dimensions", []):
        item = find_item_by_name(dim_name)
        if not item:
            logger.warning(f"Dimension '{dim_name}' not found in Items, skipping")
            continue
        
        dimension = Dimension.model_construct(
            OID=f"DIM.{domain}.{dim_name}",
            name=dim_name,
            label=item.label or dim_name,
            dataType=item.dataType,
            item=item.OID,  # Reference to the original Item (required)
            lastUpdated=datetime.now()  # Required field
        )
        # Add Dimension directly to DSD items (inlined)
        dsd.items.append(dimension)
        
        # Also add the Dimension to MDV top-level items for global access
        if not any(it.OID == dimension.OID for it in mdv.items or []):
            mdv.items.append(dimension)
    
    # Add Measure components
    for measure_name in config.get("measures", []):
        item = find_item_by_name(measure_name)
        if not item:
            logger.warning(f"Measure '{measure_name}' not found in Items, skipping")
            continue
        
        measure = Measure.model_construct(
            OID=f"MEAS.{domain}.{measure_name}",
            name=measure_name,
            label=item.label or measure_name,
            dataType=item.dataType,
            item=item.OID,  # Reference to the original Item (required)
            lastUpdated=datetime.now()  # Required field
        )
        # Add Measure directly to DSD items (inlined)
        dsd.items.append(measure)
        
        # Also add the Measure to MDV top-level items for global access
        if not any(it.OID == measure.OID for it in mdv.items or []):
            mdv.items.append(measure)
    
    # Add Attribute components
    attributes = config.get("attributes", {})
    
    # Dataset-level attributes
    for attr_name in attributes.get("dataset_level", []):
        item = find_item_by_name(attr_name)
        if not item:
            logger.warning(f"Attribute '{attr_name}' not found in Items, skipping")
            continue
        
        attribute = DataAttribute.model_construct(
            OID=f"ATTR.{domain}.{attr_name}",
            name=attr_name,
            label=item.label or attr_name,
            dataType=item.dataType,
            item=item.OID,  # Reference to the original Item (required)
            role="Dataset",  # Attachment level
            lastUpdated=datetime.now()  # Required field
        )
        # Add Attribute directly to DSD items (inlined)
        dsd.items.append(attribute)
        
        # Also add to MDV top-level items for global access
        if not any(it.OID == attribute.OID for it in mdv.items or []):
            mdv.items.append(attribute)
    
    # Dimension-level attributes
    for attr_spec in attributes.get("dimension_level", []):
        if not isinstance(attr_spec, dict):
            continue
        attr_name = attr_spec.get("variable")
        attached_to = attr_spec.get("attached_to", [])
        
        item = find_item_by_name(attr_name)
        if not item:
            logger.warning(f"Attribute '{attr_name}' not found in Items, skipping")
            continue
        
        attribute = DataAttribute.model_construct(
            OID=f"ATTR.{domain}.{attr_name}",
            name=attr_name,
            label=item.label or attr_name,
            dataType=item.dataType,
            item=item.OID,
            role=f"Dimension:{','.join(attached_to)}",  # Encode attachment info
            lastUpdated=datetime.now()  # Required field
        )
        # Add Attribute directly to DSD items (inlined)
        dsd.items.append(attribute)
        
        # Also add to MDV top-level items for global access
        if not any(it.OID == attribute.OID for it in mdv.items or []):
            mdv.items.append(attribute)
    
    # Measure-level attributes
    for attr_spec in attributes.get("measure_level", []):
        if not isinstance(attr_spec, dict):
            continue
        attr_name = attr_spec.get("variable")
        attached_to = attr_spec.get("attached_to", [])
        
        item = find_item_by_name(attr_name)
        if not item:
            logger.warning(f"Attribute '{attr_name}' not found in Items, skipping")
            continue
        
        attribute = DataAttribute.model_construct(
            OID=f"ATTR.{domain}.{attr_name}",
            name=attr_name,
            label=item.label or attr_name,
            dataType=item.dataType,
            item=item.OID,
            role=f"Measure:{','.join(attached_to)}",  # Encode attachment info
            lastUpdated=datetime.now()  # Required field
        )
        # Add Attribute directly to DSD items (inlined)
        dsd.items.append(attribute)
        
        # Also add to MDV top-level items for global access
        if not any(it.OID == attribute.OID for it in mdv.items or []):
            mdv.items.append(attribute)
    
    return dsd


def validate_dsd_completeness(
    dsd: ItemGroup,
    all_variable_oids: Set[str],
    mdv: MetaDataVersion
) -> Tuple[bool, List[str]]:
    """
    Validate that DSD classifies all variables in the domain.
    
    Args:
        dsd: DataStructureDefinition ItemGroup
        all_variable_oids: Set of all Item OIDs in the domain
        mdv: MetaDataVersion to resolve component references
        
    Returns:
        Tuple of (is_complete, missing_variables)
        - is_complete: True if all variables are classified
        - missing_variables: List of variable names not classified
    """
    # Extract all component Item references from DSD
    classified_oids = set()
    
    for component in dsd.items or []:
        # component is a Dimension/Measure/DataAttribute
        if hasattr(component, 'item') and component.item:
            # component.item is the OID of the original Item
            classified_oids.add(component.item)
    
    # Find missing variables
    missing_oids = all_variable_oids - classified_oids
    
    # Convert OIDs to names for better error messages
    missing_names = []
    for oid in missing_oids:
        for item in mdv.items or []:
            if item.OID == oid:
                missing_names.append(item.name or oid)
                break
    
    is_complete = len(missing_names) == 0
    return is_complete, missing_names


# Phase 2: WhereClause → GroupKey Derivation

def is_clean_whereclause(
    where_clause: WhereClause,
    dsd: ItemGroup,
    mdv: MetaDataVersion
) -> bool:
    """
    Check if a WhereClause is "clean" (derivable to GroupKey).
    
    A clean WhereClause:
    - Has exactly ONE condition (single AND group, no OR logic)
    - All RangeChecks use EQ comparator
    - All RangeChecks reference Dimension Items (not Measures/Attributes)
    - All RangeChecks have single checkValue (not multi-value)
    
    Args:
        where_clause: WhereClause to validate
        dsd: DataStructureDefinition to check dimension membership
        mdv: MetaDataVersion for Item lookups
        
    Returns:
        True if WhereClause is clean (derivable), False otherwise
    """
    if not where_clause.conditions:
        return False
    
    # Must have exactly one condition (no OR logic between conditions)
    if len(where_clause.conditions) > 1:
        logger.debug(f"WhereClause {where_clause.OID} has multiple conditions (OR logic), not derivable")
        return False
    
    # Resolve condition if it's a string OID
    cond_ref = where_clause.conditions[0]
    if isinstance(cond_ref, str):
        if mdv.conditions:
            condition = next((c for c in mdv.conditions if c.OID == cond_ref), None)
            if not condition:
                return False
        else:
            return False
    else:
        condition = cond_ref
    
    # Condition must not have nested conditions (no complex logic)
    if condition.conditions and len(condition.conditions) > 0:
        logger.debug(f"WhereClause {where_clause.OID} has nested conditions, not derivable")
        return False
    
    # Check all RangeChecks
    if not condition.rangeChecks:
        return False
    
    # Get dimension Item OIDs from DSD
    dimension_item_oids = set()
    for component in dsd.items or []:
        if isinstance(component, Dimension) and hasattr(component, 'item'):
            dimension_item_oids.add(component.item)
    
    for rc in condition.rangeChecks:
        # Must use EQ comparator
        if rc.comparator != Comparator.EQ:
            logger.debug(f"RangeCheck uses {rc.comparator}, not EQ - not derivable")
            return False
        
        # Must reference a Dimension Item
        if rc.item not in dimension_item_oids:
            logger.debug(f"RangeCheck references non-dimension item {rc.item} - not derivable")
            return False
        
        # Must have exactly one checkValue
        if not rc.checkValues or len(rc.checkValues) != 1:
            logger.debug(f"RangeCheck has multiple checkValues - not derivable")
            return False
    
    return True


def derive_groupkey_from_whereclause(
    where_clause: WhereClause,
    dsd: ItemGroup,
    mdv: MetaDataVersion
) -> Optional[GroupKey]:
    """
    Convert a clean WhereClause to a GroupKey.
    
    Only "clean" WhereClauses can be derived:
    - Single condition (AND logic only)
    - All RangeChecks use EQ comparator
    - All RangeChecks reference Dimensions
    - Single checkValue per RangeCheck
    
    Args:
        where_clause: WhereClause to derive from
        dsd: DataStructureDefinition defining the cube dimensions
        mdv: MetaDataVersion for Item lookups
        
    Returns:
        GroupKey instance if derivable, None if not clean
    """
    # Check if WhereClause is clean
    if not is_clean_whereclause(where_clause, dsd, mdv):
        return None
    
    # Resolve condition if it's a string OID
    cond_ref = where_clause.conditions[0]
    if isinstance(cond_ref, str):
        if mdv.conditions:
            condition = next((c for c in mdv.conditions if c.OID == cond_ref), None)
            if not condition:
                return None
        else:
            return None
    else:
        condition = cond_ref
    
    # Build map: Item OID → Dimension component
    item_to_dimension = {}
    for component in dsd.items or []:
        if isinstance(component, Dimension) and hasattr(component, 'item'):
            item_to_dimension[component.item] = component
    
    # Extract dimension values from RangeChecks
    # We need to maintain order according to DSD dimension order
    dimension_values = {}  # Dimension OID → value
    dimension_oids_used = []  # Track which dimensions are constrained
    
    for rc in condition.rangeChecks:
        if rc.item in item_to_dimension:
            dim_component = item_to_dimension[rc.item]
            dimension_values[dim_component.OID] = rc.checkValues[0]
            dimension_oids_used.append(dim_component.OID)
    
    # Build keyValues string: ordered by dimension order in DSD
    # Format: "value1.value2.value3"
    ordered_dimensions = [comp for comp in dsd.items if isinstance(comp, Dimension)]
    key_parts = []
    described_by_dims = []
    
    for dim in ordered_dimensions:
        if dim.OID in dimension_values:
            key_parts.append(dimension_values[dim.OID])
            described_by_dims.append(dim.OID)
    
    if not key_parts:
        logger.warning(f"No dimension values extracted from {where_clause.OID}")
        return None
    
    keyValues_str = ".".join(key_parts)
    
    # Create GroupKey
    # describedBy should reference the DSD itself (the DataStructureDefinition ItemGroup)
    # This associates the GroupKey with the cube structure
    describedBy_ref = dsd.OID
    
    groupkey = GroupKey.model_construct(
        keyValues=keyValues_str,
        describedBy=describedBy_ref  # Reference to DSD ItemGroup
    )
    
    return groupkey


# Phase 3: Attribute Relationship Inference

def analyze_attribute_variance(
    attribute_name: str,
    slices: List[ItemGroup],
    slice_data: Dict[str, Dict[str, str]],
    dsd: ItemGroup,
    mdv: MetaDataVersion
) -> Dict[str, Any]:
    """
    Analyze how an attribute varies across slices.
    
    Determines attachment level by checking if attribute values change
    when specific dimensions change.
    
    Args:
        attribute_name: Name of the attribute to analyze (e.g., "LBCAT")
        slices: List of ItemGroup slices (type=DatasetSpecialization)
        slice_data: Dict mapping WhereClause OID to attribute/dimension values
        dsd: DataStructureDefinition containing dimensions
        mdv: MetaDataVersion for lookups
        
    Returns:
        Dict with:
        - level: "dataset" | "dimension" | "observation"
        - varies_with: List of dimension names it varies with
        - constant_value: Value if constant (dataset-level)
    """
    # Get dimension names from DSD
    dimension_names = []
    for component in dsd.items or []:
        if isinstance(component, Dimension):
            dimension_names.append(component.name)
    
    # Collect attribute values across slices
    attribute_values = {}
    dimension_combos = {}
    
    for slice_ig in slices:
        if not slice_ig.applicableWhen or len(slice_ig.applicableWhen) == 0:
            continue
        
        wc_oid = slice_ig.applicableWhen[0]
        
        if wc_oid not in slice_data:
            continue
        
        data = slice_data[wc_oid]
        
        if attribute_name not in data:
            continue
        
        attr_value = data[attribute_name]
        attribute_values[wc_oid] = attr_value
        
        # Extract dimension values for this slice
        dim_values = {dim: data.get(dim) for dim in dimension_names if dim in data}
        dimension_combos[wc_oid] = dim_values
    
    if not attribute_values:
        logger.warning(f"No data found for attribute {attribute_name}")
        return {"level": "unknown", "varies_with": [], "reason": "no_data"}
    
    # Check if constant everywhere
    unique_values = set(attribute_values.values())
    if len(unique_values) == 1:
        return {
            "level": "dataset",
            "varies_with": [],
            "constant_value": list(unique_values)[0]
        }
    
    # Check which dimensions the attribute varies with
    varies_with = []
    
    for dim_name in dimension_names:
        # Group slices by this dimension value
        dim_groups = {}
        for wc_oid, dim_vals in dimension_combos.items():
            dim_val = dim_vals.get(dim_name)
            if dim_val is None:
                continue
            
            if dim_val not in dim_groups:
                dim_groups[dim_val] = []
            dim_groups[dim_val].append(wc_oid)
        
        # Check if attribute is constant within each dimension group
        varies_within_group = False
        varies_across_groups = False
        
        group_attr_values = {}
        for dim_val, wc_oids in dim_groups.items():
            attr_vals_in_group = [attribute_values[oid] for oid in wc_oids if oid in attribute_values]
            unique_in_group = set(attr_vals_in_group)
            
            if len(unique_in_group) > 1:
                varies_within_group = True
            
            # Store the values for this dimension value
            group_attr_values[dim_val] = unique_in_group
        
        # Check if attribute varies across dimension values
        all_group_values = set()
        for vals in group_attr_values.values():
            all_group_values.update(vals)
        
        if len(all_group_values) > 1:
            varies_across_groups = True
        
        # Attribute varies with this dimension if:
        # - Values differ across dimension groups AND
        # - Values are constant within groups (deterministic relationship)
        if varies_across_groups and not varies_within_group:
            varies_with.append(dim_name)
    
    if varies_with:
        return {
            "level": "dimension",
            "varies_with": varies_with
        }
    
    # If it varies but not cleanly with any dimension, it's observation-level
    return {
        "level": "observation",
        "varies_with": dimension_names,  # Varies with full key
        "reason": "no_clear_dimension_relationship"
    }


def infer_attribute_relationships(
    dsd: ItemGroup,
    slices: List[ItemGroup],
    slice_data: Dict[str, Dict[str, str]],
    mdv: MetaDataVersion
) -> Dict[str, Dict[str, Any]]:
    """
    Infer attribute attachment levels by analyzing variance across slices.
    
    Updates DataAttribute.role in the DSD with inferred attachment.
    
    Args:
        dsd: DataStructureDefinition ItemGroup
        slices: List of ItemGroup slices (type=DatasetSpecialization)
        slice_data: Dict mapping WhereClause OID to attribute/dimension values
        mdv: MetaDataVersion for lookups
        
    Returns:
        Report dict mapping attribute name to variance analysis
    """
    report = {}
    
    # Find all DataAttribute components in DSD
    attributes = [item for item in dsd.items or [] if isinstance(item, DataAttribute)]
    
    for attr in attributes:
        # Analyze variance for this attribute
        variance = analyze_attribute_variance(attr.name, slices, slice_data, dsd, mdv)
        
        report[attr.name] = variance
        
        # Update DataAttribute.role based on inference
        if variance["level"] == "dataset":
            attr.role = "Dataset"
            logger.info(f"Inferred {attr.name} as Dataset-level attribute")
        
        elif variance["level"] == "dimension":
            # Encode dimension attachment in role
            dims = ",".join(variance["varies_with"])
            attr.role = f"Dimension:{dims}"
            logger.info(f"Inferred {attr.name} as Dimension-level attribute attached to {dims}")
        
        elif variance["level"] == "observation":
            attr.role = "Observation"
            logger.info(f"Inferred {attr.name} as Observation-level attribute")
        
        else:
            # Unknown - keep existing role or set to None
            logger.warning(f"Could not infer attachment level for {attr.name}: {variance.get('reason')}")
    
    return report


__all__ = [
    "load_data_cube_config",
    "load_sdmx_policy",  # Backward compatibility alias
    "classify_item_role",
    "build_dsd_for_domain",
    "validate_dsd_completeness",
    "is_clean_whereclause",
    "derive_groupkey_from_whereclause",
    "analyze_attribute_variance",
    "infer_attribute_relationships",
]

