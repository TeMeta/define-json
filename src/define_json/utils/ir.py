"""
IR utilities: canonical WhereClause registry, slice canon, ValueList projection,
canonical serialiser, and minimal Define-XML exporters — using generated/define.py only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from xml.etree import ElementTree as ET

try:
    from ..schema.define import (
        MetaDataVersion,
        ItemGroup,
        Item,
        WhereClause,
        Condition,
        RangeCheck,
        CodeList,
        CodeListItem,
        ItemGroupType,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError("define_json.schema.define not available") from exc


def load_mdv(json_path: Path) -> MetaDataVersion:
    """
    Load MetaDataVersion from JSON file.
    
    Args:
        json_path: Path to JSON file containing MetaDataVersion data
        
    Returns:
        MetaDataVersion instance
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle wrapped structure with metaDataVersion key
    if isinstance(data, dict) and "metaDataVersion" in data:
        mdv_list = data["metaDataVersion"]
        if isinstance(mdv_list, list) and len(mdv_list) > 0:
            return MetaDataVersion.model_validate(mdv_list[0])
        elif isinstance(mdv_list, dict):
            return MetaDataVersion.model_validate(mdv_list)
    
    # Handle direct MetaDataVersion object
    if isinstance(data, dict):
        return MetaDataVersion.model_validate(data)
    
    raise ValueError(f"Unexpected JSON structure in {json_path}")


def _normalise_check_value(v: Any) -> Any:
    return v.strip() if isinstance(v, str) else v


def _ref_to_string(ref: Any) -> str:
    if ref is None:
        return ""
    # Handle string OIDs directly
    if isinstance(ref, str):
        return ref
    # Handle objects with OID/uuid/name attributes
    for attr in ("OID", "uuid", "name"):
        val = getattr(ref, attr, None)
        if isinstance(val, str) and val:
            return f"{attr.upper()}:{val}"
    return f"OBJ:{ref.__class__.__name__}:{id(ref)}"


def _canonical_condition_payload(cond: Condition, mdv: Optional[MetaDataVersion] = None) -> Dict[str, Any]:
    """
    Build canonical payload for Condition.
    
    Handles rangeChecks and nested condition references.
    """
    payload: Dict[str, Any] = {}
    
    # Process rangeChecks
    checks = cond.rangeChecks or []
    canon_checks: List[Dict[str, Any]] = []
    for rc in checks:
        comparator = getattr(rc, "comparator", None)
        values = [_normalise_check_value(v) for v in (rc.checkValues or [])]
        try:
            values = sorted(values)
        except TypeError:
            values = sorted(map(lambda x: json.dumps(x, sort_keys=True), values))
        canon_checks.append({
            "item": _ref_to_string(getattr(rc, "item", None)),
            "comparator": comparator,
            "values": values,
        })
    canon_checks.sort(key=lambda d: (d["item"], str(d["comparator"]), json.dumps(d["values"])))
    if canon_checks:
        payload["rangeChecks"] = canon_checks
    
    # Process nested conditions (OID references)
    nested_conditions = cond.conditions or []
    if nested_conditions:
        # Sort condition OIDs for determinism
        payload["conditions"] = sorted(nested_conditions)
    
    # Include operator if present
    operator = getattr(cond, "operator", None)
    if operator:
        payload["operator"] = operator
    
    return payload


def _canonical_where_payload(where: WhereClause, mdv: Optional[MetaDataVersion] = None) -> Dict[str, Any]:
    """
    Build canonical payload for WhereClause based on actual RangeCheck content.
    
    This function extracts all RangeChecks from all Conditions in the WhereClause
    and creates a canonical representation based on the actual content, not Condition OIDs.
    This ensures that WhereClauses with identical RangeCheck content are properly consolidated.
    
    Handles both string OID references and Condition objects.
    """
    conditions = where.conditions or []
    all_range_checks: List[Dict[str, Any]] = []
    
    for cond_ref in conditions:
        # Resolve condition if it's a string OID
        if isinstance(cond_ref, str):
            if mdv and mdv.conditions:
                cond = next((c for c in mdv.conditions if c.OID == cond_ref), None)
                if not cond:
                    # If condition not found, skip (or use empty)
                    continue
            else:
                # Can't resolve, skip
                continue
        else:
            # Already a Condition object
            cond = cond_ref
        
        # Extract RangeChecks from this Condition
        checks = cond.rangeChecks or []
        for rc in checks:
            comparator = getattr(rc, "comparator", None)
            values = [_normalise_check_value(v) for v in (rc.checkValues or [])]
            try:
                values = sorted(values)
            except TypeError:
                values = sorted(map(lambda x: json.dumps(x, sort_keys=True), values))
            all_range_checks.append({
                "item": _ref_to_string(getattr(rc, "item", None)),
                "comparator": comparator,
                "values": values,
                "softHard": getattr(rc, "softHard", None),
            })
    
    # Sort range checks for determinism
    all_range_checks.sort(key=lambda d: (
        d.get("item", ""),
        str(d.get("comparator", "")),
        json.dumps(d.get("values", []), sort_keys=True)
    ))
    
    # Return canonical payload based on actual RangeCheck content
    # This ensures WhereClauses with identical RangeChecks are considered equal
    return {"rangeChecks": all_range_checks}


def _extract_meaningful_oid(where: WhereClause, mdv: Optional[MetaDataVersion] = None) -> Optional[str]:
    """
    Extract meaningful OID from WhereClause structure if possible.
    
    Attempts to create human-readable OID like WC.{domain}.{test_code} from the
    WhereClause structure. Falls back to None if structure is too complex.
    
    Args:
        where: WhereClause to extract OID from
        mdv: Optional MetaDataVersion to resolve Condition OID references
        
    Returns:
        Meaningful OID string (e.g., "WC.VS.TEMP") or None if structure too complex
    """
    payload = _canonical_where_payload(where, mdv)
    range_checks = payload.get('rangeChecks', [])
    
    if not range_checks:
        return None
    
    # Extract domain and test codes from rangeChecks
    domains = set()
    all_checks = []
    
    for rc in range_checks:
        item = rc.get('item', '')
        values = rc.get('values', [])
        
        # Parse domain from item OID (e.g., IT.VS.VSTESTCD -> VS)
        if item.startswith('IT.'):
            parts = item.split('.')
            if len(parts) >= 2:
                domains.add(parts[1])
        
        # Collect checks with their item and values
        for val in values:
            if isinstance(val, str):
                all_checks.append((item, val))
    
    # Must have exactly one domain
    if len(domains) != 1:
        return None
    
    domain = list(domains)[0]
    
    # Extract test codes (checkValues) - sort for determinism
    test_codes = sorted([val for _, val in all_checks])
    
    if not test_codes:
        return None
    
    # Build OID: WC.{domain}.{test_code} or WC.{domain}.{test_code1}_{test_code2}...
    if len(test_codes) == 1:
        test_code = test_codes[0]
        return f"WC.{domain}.{test_code}"
    else:
        # Multiple test codes - join with underscore, already sorted
        test_code = '_'.join(test_codes)
        return f"WC.{domain}.{test_code}"


def canonicalise_whereclause(where: WhereClause, mdv: Optional[MetaDataVersion] = None) -> str:
    """
    Create canonical ID for WhereClause.
    
    Attempts to extract meaningful OID (e.g., WC.VS.TEMP) from structure.
    Falls back to hash-based OID if structure is too complex.
    
    Args:
        where: WhereClause to canonicalise
        mdv: Optional MetaDataVersion to resolve Condition OID references
        
    Returns:
        Canonical OID string (meaningful if possible, otherwise hash-based)
    """
    # Try to extract meaningful OID first
    meaningful_oid = _extract_meaningful_oid(where, mdv)
    if meaningful_oid:
        return meaningful_oid
    
    # Fallback to hash-based OID for complex structures
    payload = _canonical_where_payload(where, mdv)
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"WC.{hashlib.sha256(data).hexdigest()[:16]}"


def _canonical_condition_oid(cond: Condition, mdv: Optional[MetaDataVersion] = None) -> str:
    """
    Create canonical OID for Condition based on its structure.
    
    Attempts to extract meaningful OID (e.g., COND.VS.TEMP) from structure,
    falls back to hash-based OID for complex structures.
    """
    payload = _canonical_condition_payload(cond, mdv)
    return _canonical_condition_oid_from_payload(payload)


def _canonical_condition_oid_from_payload(payload: Dict[str, Any]) -> str:
    """
    Create canonical OID for Condition from its payload.
    
    Attempts to extract meaningful OID (e.g., COND.VS.TEMP, COND.VS.DIABP_SITTING) 
    from structure, falls back to hash-based OID for complex structures.
    """
    range_checks = payload.get("rangeChecks", [])
    if not range_checks:
        # Fallback to hash-based OID
        data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return f"COND.{hashlib.sha256(data).hexdigest()[:16]}"
    
    # Extract domain and values from all RangeChecks
    domains = set()
    all_values = []
    
    for rc in range_checks:
        item = rc.get("item", "")
        values = rc.get("values", [])
        
        # Parse domain from item OID (e.g., IT.VS.VSTESTCD -> VS)
        if item.startswith("IT."):
            parts = item.split(".")
            if len(parts) >= 2:
                domains.add(parts[1])
        
        # Collect all string values
        for val in values:
            if isinstance(val, str):
                all_values.append(val)
    
    # Must have exactly one domain
    if len(domains) != 1:
        # Fallback to hash-based OID
        data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return f"COND.{hashlib.sha256(data).hexdigest()[:16]}"
    
    domain = list(domains)[0]
    
    # Sort values for determinism
    sorted_values = sorted(set(all_values))
    
    if not sorted_values:
        # Fallback to hash-based OID
        data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return f"COND.{hashlib.sha256(data).hexdigest()[:16]}"
    
    # Build meaningful OID: COND.{domain}.{value1} or COND.{domain}.{value1}_{value2}...
    if len(sorted_values) == 1:
        return f"COND.{domain}.{sorted_values[0]}"
    else:
        # Multiple values - join with underscore
        value_str = '_'.join(sorted_values)
        return f"COND.{domain}.{value_str}"


def _canonical_condition_oid_from_range_checks(range_checks: List[Dict[str, Any]], mdv: Optional[MetaDataVersion] = None) -> str:
    """
    Create canonical OID for Condition from a list of RangeCheck dictionaries.
    
    Attempts to extract meaningful OID (e.g., COND.VS.TEMP) from structure,
    falls back to hash-based OID for complex structures.
    """
    # Build payload from range checks
    payload: Dict[str, Any] = {}
    canon_checks: List[Dict[str, Any]] = []
    for rc_data in range_checks:
        canon_checks.append({
            "item": rc_data.get("item", ""),
            "comparator": rc_data.get("comparator"),
            "values": rc_data.get("values", []),
        })
    canon_checks.sort(key=lambda d: (d["item"], str(d["comparator"]), json.dumps(d["values"])))
    if canon_checks:
        payload["rangeChecks"] = canon_checks
    
    return _canonical_condition_oid_from_payload(payload)


def build_condition_registry(mdv: MetaDataVersion) -> Dict[str, Condition]:
    """
    Build canonical Condition registry and remap all references to canonical OIDs.
    
    This should be called BEFORE build_where_registry since WhereClauses reference Conditions.
    """
    registry: Dict[str, Condition] = {}
    old_to_canonical: Dict[str, str] = {}
    
    # Canonicalise all Conditions and build mapping from old OID -> canonical OID
    for cond in (mdv.conditions or []):
        old_oid = cond.OID
        canonical_oid = _canonical_condition_oid(cond, mdv)
        
        if canonical_oid not in registry:
            # First Condition with this canonical OID - keep it
            cond.OID = canonical_oid
            registry[canonical_oid] = cond
        
        # Map old OID to canonical OID (for remapping references)
        if old_oid:
            old_to_canonical[old_oid] = canonical_oid
    
    # Remap all Condition references in WhereClauses
    for wc in (mdv.whereClauses or []):
        if wc.conditions:
            wc.conditions = [
                old_to_canonical.get(oid, oid) for oid in wc.conditions
            ]
    
    # Remap nested Condition references in other Conditions
    for cond in (mdv.conditions or []):
        if cond.conditions:
            cond.conditions = [
                old_to_canonical.get(oid, oid) for oid in cond.conditions
            ]
    
    # Remove duplicate Conditions from the list
    mdv.conditions = list(registry.values())
    
    return registry


def build_where_registry(mdv: MetaDataVersion) -> Dict[str, WhereClause]:
    """
    Build canonical WhereClause registry and remap all references to canonical OIDs.
    
    Consolidates WhereClauses based on their actual RangeCheck content (not Condition OIDs).
    Each consolidated WhereClause will have exactly one Condition containing all RangeChecks.
    
    Note: Conditions should be consolidated first via build_condition_registry().
    """
    # First, collect all RangeChecks from each WhereClause to identify unique content
    whereclause_payloads: Dict[str, Dict[str, Any]] = {}
    old_to_payload: Dict[str, Dict[str, Any]] = {}
    
    for wc in (mdv.whereClauses or []):
        payload = _canonical_where_payload(wc, mdv)
        payload_key = json.dumps(payload, sort_keys=True)
        old_to_payload[wc.OID] = payload
        whereclause_payloads[payload_key] = payload
    
    # Build registry: one WhereClause per unique payload
    registry: Dict[str, WhereClause] = {}
    payload_to_canonical_oid: Dict[str, str] = {}
    old_to_canonical: Dict[str, str] = {}
    
    # Create consolidated WhereClauses and Conditions
    for wc in (mdv.whereClauses or []):
        old_oid = wc.OID
        payload = old_to_payload[old_oid]
        payload_key = json.dumps(payload, sort_keys=True)
        
        # Get or create canonical OID for this payload
        if payload_key not in payload_to_canonical_oid:
            canonical_wid = canonicalise_whereclause(wc, mdv)
            payload_to_canonical_oid[payload_key] = canonical_wid
            
            # Create a single Condition containing all RangeChecks from this WhereClause
            range_checks = payload.get("rangeChecks", [])
            if range_checks:
                # Create Condition with all RangeChecks
                condition_oid = _canonical_condition_oid_from_range_checks(range_checks, mdv)
                
                # Check if Condition already exists, if not create it
                existing_cond = next((c for c in (mdv.conditions or []) if c.OID == condition_oid), None)
                if not existing_cond:
                    # Create new Condition with all RangeChecks
                    new_range_checks = []
                    for rc_data in range_checks:
                        rc = RangeCheck.model_construct(
                            item=rc_data.get("item"),
                            comparator=rc_data.get("comparator"),
                            checkValues=rc_data.get("values", []),
                            softHard=rc_data.get("softHard"),
                        )
                        new_range_checks.append(rc)
                    
                    new_cond = Condition.model_construct(
                        OID=condition_oid,
                        rangeChecks=new_range_checks,
                    )
                    if mdv.conditions is None:
                        mdv.conditions = []
                    mdv.conditions.append(new_cond)
                
                # Create consolidated WhereClause with single Condition reference
                consolidated_wc = WhereClause.model_construct(
                    OID=canonical_wid,
                    conditions=[condition_oid],
                )
                registry[canonical_wid] = consolidated_wc
        
        # Map old OID to canonical OID (for remapping applicableWhen)
        canonical_wid = payload_to_canonical_oid[payload_key]
        if old_oid:
            old_to_canonical[old_oid] = canonical_wid
    
    # Remap all applicableWhen to use canonical OIDs
    def _remap_oids(obj: Any) -> None:
        """Remap applicableWhen OIDs to canonical OIDs."""
        if hasattr(obj, "applicableWhen") and obj.applicableWhen:
            obj.applicableWhen = [
                old_to_canonical.get(oid, oid) for oid in obj.applicableWhen
            ]
    
    # Remap all ItemGroups
    for ig in (mdv.itemGroups or []):
        _remap_oids(ig)
        # Remap Items within ItemGroup
        for it in (ig.items or []):
            _remap_oids(it)
    
    # Remap top-level Items
    for it in (mdv.items or []):
        _remap_oids(it)
    
    # Replace WhereClauses with consolidated ones
    mdv.whereClauses = list(registry.values())
    
    return registry


def _is_slice(ig: ItemGroup) -> bool:
    """Check if ItemGroup is a DataSpecialization slice."""
    ig_type = getattr(ig, "type", None)
    return ig_type == ItemGroupType.DataSpecialization


def _domain_name_of_ig(ig: ItemGroup) -> str:
    return getattr(ig, "domain", None) or getattr(ig, "name", None) or ""


def _is_value_list(ig: ItemGroup) -> bool:
    """Check if ItemGroup is a ValueList (type="ValueList" or ItemGroupType.ValueList)."""
    ig_type = getattr(ig, "type", None)
    if ig_type == ItemGroupType.ValueList:
        return True
    return str(ig_type) == "ValueList"


def transform_value_lists_to_specialisation(mdv: MetaDataVersion) -> None:
    """
    Transform ValueList-based structure to Dataset Specialisation shape.
    
    Converts ItemGroups with type="ValueList" (containing items grouped by variable name)
    into canonical ItemGroups with type="DataSpecialization" (slices) where each shared
    WhereClause gets its own ItemGroup containing ALL items that apply when that WhereClause is true.
    
    This transformation creates canonical slices:
    1. Consolidates unique WhereClauses based on their structure (conditions/RangeChecks)
    2. Identifies all ValueList ItemGroups (type="ValueList")
    3. Extracts items from each ValueList, preserving all item properties
    4. Groups items by their applicableWhen WhereClause OID(s) - canonical: one slice per WhereClause
    5. Creates new DataSpecialization ItemGroups for each unique WhereClause (not per domain+WhereClause)
    6. Removes the original ValueList ItemGroups
    7. Updates domain ItemGroup children to reference canonical slice OIDs (removes ValueList references)
    
    Capabilities:
    - Consolidates unique WhereClauses: deduplicates WhereClauses with identical structure (conditions)
    - Canonical grouping: one slice per shared WhereClause (all items with same WhereClause in one slice)
    - Handles items with single or multiple applicableWhen WhereClauses
    - Preserves domain information from items (slice domain set from items' domains)
    - Maintains all item properties (dataType, origin, codeList, etc.)
    - Creates canonical slice OIDs following pattern: IG.{WhereClauseOID}
    - Merges items from multiple ValueLists/domains that share the same WhereClause into one slice
    - Updates domain ItemGroup children to reference slice OIDs (not ValueLists)
    
    This is the inverse transformation of _create_value_lists_from_slices in
    json_to_xml.py, which projects DataSpecialization slices back to ValueLists.
    
    Args:
        mdv: MetaDataVersion to transform in-place
        
    Modifies:
        mdv.whereClauses - Duplicate WhereClauses consolidated, references updated
        mdv.itemGroups - ValueLists are removed, replaced with canonical DataSpecialization slices
        Domain ItemGroup children - ValueList references removed, slice OID references added
    
    Example:
        Before: ValueList VL.VS.VSORRES contains items for TEMP, WEIGHT, HEIGHT, etc.
                each with applicableWhen=["WC.VS.VSORRES.TEMP"], etc.
                IG.VS has children=[VL.VS.VSORRES, VL.VS.VSORRESU]
                WhereClauses: WC.VS.VSORRES.TEMP, WC.VS.VSORRESU.TEMP (duplicate structures)
        
        After:  ItemGroup IG.WC.VS.VSORRES.TEMP (type="DataSpecialization", canonical OID)
                with applicableWhen=["WC.{canonical_hash}"] (consolidated WhereClause)
                containing ALL items with this WhereClause (e.g., IT.VS.VSORRES.TEMP, IT.VS.VSORRESU.TEMP)
                IG.VS has children=["IG.WC.{canonical_hash}", ...]
                WhereClauses: Consolidated to unique structures only
    
    Note:
        Items without applicableWhen are not included in the transformation.
        Domain ItemGroups (non-ValueList, non-slice) are preserved unchanged.
        If items from multiple domains share the same WhereClause, they all go into one slice.
    """
    if not mdv.itemGroups:
        return
    
    # First, consolidate unique Conditions based on their structure
    # This deduplicates Conditions with identical rangeChecks/conditions
    build_condition_registry(mdv)
    
    # Then, consolidate unique WhereClauses based on their structure
    # This deduplicates WhereClauses with identical conditions (now using consolidated Condition OIDs)
    build_where_registry(mdv)
    
    # Track slices by WhereClause OID only (canonical: one slice per shared WhereClause)
    wc_oid_to_slice: Dict[str, ItemGroup] = {}
    value_list_oids_to_remove: Set[str] = set()
    # Track which domain ItemGroups need their children updated
    domain_to_slice_oids: Dict[str, List[str]] = {}
    # Track domains for each WhereClause (for slice domain assignment)
    wc_oid_to_domains: Dict[str, Set[str]] = {}
    
    # Process all ValueLists
    for vl_ig in list(mdv.itemGroups or []):
        if not _is_value_list(vl_ig):
            continue
        
        domain = _domain_name_of_ig(vl_ig)
        if not domain:
            # Try to infer domain from OID pattern (e.g., VL.VS.VSORRES -> VS)
            oid_parts = vl_ig.OID.split('.')
            if len(oid_parts) >= 2 and oid_parts[0] == 'VL':
                domain = oid_parts[1]
        
        if not domain:
            # Skip ValueLists without domain information
            continue
        
        # Extract items from ValueList
        items = vl_ig.items or []
        if not items:
            # Mark empty ValueList for removal
            value_list_oids_to_remove.add(vl_ig.OID)
            continue
        
        # Group items by their applicableWhen WhereClause OIDs
        for item in items:
            applicable_whens = item.applicableWhen or []
            if not applicable_whens:
                # Skip items without applicableWhen
                continue
            
            # Create or update slices for each applicableWhen WhereClause
            for wc_oid in applicable_whens:
                if not isinstance(wc_oid, str):
                    wc_oid = str(wc_oid)
                
                # Track domain for this WhereClause
                if wc_oid not in wc_oid_to_domains:
                    wc_oid_to_domains[wc_oid] = set()
                wc_oid_to_domains[wc_oid].add(domain)
                
                # Create or get slice for this WhereClause (canonical: one per WhereClause)
                if wc_oid not in wc_oid_to_slice:
                    # Determine slice domain: use first domain, or None if multiple domains share this WhereClause
                    slice_domain = domain if len(wc_oid_to_domains[wc_oid]) == 1 else None
                    
                    # Create canonical DataSpecialization slice
                    # OID pattern: IG.{WhereClauseOID} (canonical, based purely on WhereClause)
                    slice_oid = f"IG.{wc_oid}"
                    slice_name = wc_oid.replace('.', '_')
                    
                    new_slice = ItemGroup.model_construct(
                        OID=slice_oid,
                        name=slice_name,
                        domain=slice_domain,
                        type=ItemGroupType.DataSpecialization
                    )
                    new_slice.applicableWhen = [wc_oid]
                    new_slice.items = []
                    new_slice.children = None  # Slices are leaf nodes, no children
                    wc_oid_to_slice[wc_oid] = new_slice
                    mdv.itemGroups.append(new_slice)
                    
                    # Track slice OID for domain's children (all domains that use this WhereClause)
                    for wc_domain in wc_oid_to_domains[wc_oid]:
                        if wc_domain not in domain_to_slice_oids:
                            domain_to_slice_oids[wc_domain] = []
                        domain_to_slice_oids[wc_domain].append(slice_oid)
                
                # Add item to slice if not already present
                # Items with multiple applicableWhen values will appear in multiple slices,
                # which is correct - each slice represents one WhereClause context
                if wc_oid_to_slice[wc_oid].items is None:
                    wc_oid_to_slice[wc_oid].items = []
                if item not in wc_oid_to_slice[wc_oid].items:
                    wc_oid_to_slice[wc_oid].items.append(item)
        
        # Mark ValueList for removal after processing
        value_list_oids_to_remove.add(vl_ig.OID)
    
    # Remove processed ValueLists
    if value_list_oids_to_remove:
        mdv.itemGroups = [
            ig for ig in mdv.itemGroups 
            if ig.OID not in value_list_oids_to_remove
        ]
    
    # Update domain ItemGroups: replace ValueList children with slice OID references
    # Slices are top-level ItemGroups, so we reference them as string OIDs (not inline objects)
    for domain_ig in mdv.itemGroups or []:
        if _is_slice(domain_ig) or _is_value_list(domain_ig):
            continue  # Skip slices (leaf nodes) and ValueLists (already removed)
        
        domain = _domain_name_of_ig(domain_ig)
        if domain in domain_to_slice_oids:
            # Replace children with slice OID string references
            domain_ig.children = sorted(domain_to_slice_oids[domain]) or None
        else:
            # No slices for this domain - clear any ValueList references
            domain_ig.children = None


def build_canonical_slices(mdv: MetaDataVersion) -> None:
    """Build canonical slices: one ItemGroup per (domain, whereId)."""
    key_to_slice: Dict[Tuple[str, str], ItemGroup] = {}
    slice_oids_to_remove: Set[str] = set()
    
    # Merge pre-existing slices by (domain, whereId)
    for ig in list(mdv.itemGroups or []):
        if _is_slice(ig):
            w = (ig.applicableWhen or [])
            if len(w) != 1:
                raise ValueError("Slice must have exactly one applicableWhereClause")
            # w[0] is now a string OID
            wid = w[0] if isinstance(w[0], str) else str(w[0])
            key = (_domain_name_of_ig(ig), wid)
            if key in key_to_slice:
                # Merge items into existing slice
                key_to_slice[key].items = (key_to_slice[key].items or []) + (ig.items or [])
                # Mark this duplicate slice for removal (by OID)
                slice_oids_to_remove.add(ig.OID)
            else:
                key_to_slice[key] = ig

    # Remove merged/empty slices
    if slice_oids_to_remove:
        mdv.itemGroups = [ig for ig in mdv.itemGroups if ig.OID not in slice_oids_to_remove]

    # Place contextual items into slices
    for ig in (mdv.itemGroups or []):
        if _is_slice(ig):
            continue
        dom = _domain_name_of_ig(ig)
        for it in (ig.items or []):
            for wid in (it.applicableWhen or []):
                # wid is now a string OID
                if not isinstance(wid, str):
                    wid = str(wid)
                key = (dom, wid)
                if key not in key_to_slice:
                    # Create new slice
                    new_ig = ItemGroup.model_construct(
                        OID=f"IG.{dom}.{wid}",
                        name=f"{dom}_{wid}",
                        domain=dom,
                        type="DataSpecialization"
                    )
                    new_ig.applicableWhen = [wid]
                    new_ig.items = []
                    key_to_slice[key] = new_ig
                    mdv.itemGroups.append(new_ig)
                key_to_slice[key].items.append(it)


def enforce_slice_invariants(mdv: MetaDataVersion) -> None:
    """Validate slice invariants: non-empty, single WhereClause, no duplicates."""
    seen: Set[Tuple[str, str]] = set()
    for ig in (mdv.itemGroups or []):
        if not _is_slice(ig):
            continue
        w = ig.applicableWhen or []
        if len(w) != 1:
            raise ValueError("Slice must have exactly one applicableWhereClause")
        wid = w[0] if isinstance(w[0], str) else str(w[0])
        items = ig.items or []
        if not items:
            raise ValueError("Slice is empty")
        for it in items:
            for iw_oid in (it.applicableWhen or []):
                iw_oid = iw_oid if isinstance(iw_oid, str) else str(iw_oid)
                if iw_oid != wid:
                    raise ValueError("Item within slice has conflicting applicableWhereClause")
            key = (getattr(it, "name", ""), wid)
            if key in seen:
                raise ValueError(f"Duplicate contextual variable {key[0]}@{wid}")
            seen.add(key)


def register_variables(mdv: MetaDataVersion) -> Dict[str, Set[str]]:
    """Register all variables with their contexts (whereIds)."""
    mapping: Dict[str, Set[str]] = {}
    for ig in (mdv.itemGroups or []):
        dom = _domain_name_of_ig(ig)
        if _is_slice(ig):
            wid = (ig.applicableWhen or [""])[0]
            wid = wid if isinstance(wid, str) else str(wid)
            for it in (ig.items or []):
                key = f"{dom}.{getattr(it, 'name', '')}"
                mapping.setdefault(key, set()).add(wid)
        else:
            for it in (ig.items or []):
                key = f"{dom}.{getattr(it, 'name', '')}"
                mapping.setdefault(key, set())
                if not (it.applicableWhen or []):
                    mapping[key].add("__DEFAULT__")
    return mapping


def project_valuelist_for_domain(mdv: MetaDataVersion, domain: str) -> Dict[str, List[Item]]:
    """Project variable-first view: each variable with its contexts ordered by whereId."""
    parents: Dict[str, Item] = {}
    for ig in (mdv.itemGroups or []):
        if _is_slice(ig) or _domain_name_of_ig(ig) != domain:
            continue
        for it in (ig.items or []):
            parents[getattr(it, "name", "")] = it
    var_to_items: Dict[str, List[Item]] = {k: [] for k in parents.keys()}
    for ig in (mdv.itemGroups or []):
        if not _is_slice(ig) or _domain_name_of_ig(ig) != domain:
            continue
        wid = (ig.applicableWhen or [""])[0]
        wid = wid if isinstance(wid, str) else str(wid)
        for it in (ig.items or []):
            if not getattr(it, "applicableWhen", None):
                it.applicableWhen = [wid]
            var_to_items.setdefault(getattr(it, "name", ""), []).append(it)
    for var, items in var_to_items.items():
        items.sort(key=lambda x: (x.applicableWhen or [""])[0] if x.applicableWhen else "")
    return var_to_items


def _sort_code_list_items(cl: CodeList) -> None:
    if getattr(cl, "codeListItems", None) is not None:
        cl.codeListItems.sort(key=lambda x: getattr(x, "codedValue", ""))


def _sort_itemgroup_items(ig: ItemGroup) -> None:
    if getattr(ig, "items", None) is not None:
        ig.items.sort(key=lambda x: getattr(x, "name", ""))


def _sort_where_clauses(mdv: MetaDataVersion) -> None:
    if getattr(mdv, "whereClauses", None) is not None:
        mdv.whereClauses.sort(key=lambda x: getattr(x, "OID", ""))


def serialize_canonical(mdv: MetaDataVersion) -> bytes:
    for ig in (mdv.itemGroups or []):
        _sort_itemgroup_items(ig)
    if getattr(mdv, "itemGroups", None) is not None:
        mdv.itemGroups.sort(key=lambda g: (_domain_name_of_ig(g), getattr(g, "name", ""), str(getattr(g, "type", ""))))
    if getattr(mdv, "items", None) is not None:
        mdv.items.sort(key=lambda x: getattr(x, "name", ""))
    for cl in (mdv.codeLists or []):
        _sort_code_list_items(cl)
    if getattr(mdv, "codeLists", None) is not None:
        mdv.codeLists.sort(key=lambda x: getattr(x, "OID", ""))
    _sort_where_clauses(mdv)

    def _default(o: Any):
        if hasattr(o, "__dict__"):
            return {k: v for k, v in o.__dict__.items() if not k.startswith("_")}
        return str(o)

    return json.dumps(mdv, default=_default, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def export_define_xml_21(mdv: MetaDataVersion, domains: Optional[List[str]] = None) -> str:
    root = ET.Element("Define")
    wcd = ET.SubElement(root, "WhereClauseDefs")
    
    # Build condition lookup
    condition_lookup = {}
    if mdv.conditions:
        for cond in mdv.conditions:
            condition_lookup[cond.OID] = cond
    
    for wc in (mdv.whereClauses or []):
        wc_el = ET.SubElement(wcd, "WhereClauseDef", {"OID": wc.OID or ""})
        for cond_ref in (wc.conditions or []):
            # Resolve condition if it's a string OID
            if isinstance(cond_ref, str):
                cond = condition_lookup.get(cond_ref)
                if not cond:
                    continue
            else:
                cond = cond_ref
            
            cond_el = ET.SubElement(wc_el, "Condition")
            for rc in (cond.rangeChecks or []):
                rc_el = ET.SubElement(cond_el, "RangeCheck", {"Comparator": str(getattr(rc, "comparator", ""))})
                for val in (rc.checkValues or []):
                    ET.SubElement(rc_el, "CheckValue").text = str(val)

    cld = ET.SubElement(root, "CodeListDefs")
    for cl in (mdv.codeLists or []):
        cl_el = ET.SubElement(cld, "CodeListDef", {"OID": getattr(cl, "OID", "")})
        for cli in (cl.codeListItems or []):
            ET.SubElement(cl_el, "CodeListItem", {"CodedValue": str(getattr(cli, "codedValue", ""))}).text = str(getattr(cli, "decode", ""))

    idd = ET.SubElement(root, "ItemDefs")
    domains_set = set(domains or [])
    for ig in (mdv.itemGroups or []):
        if _is_slice(ig):
            continue
        dom = _domain_name_of_ig(ig)
        if domains_set and dom not in domains_set:
            continue
        for it in (ig.items or []):
            ET.SubElement(idd, "ItemDef", {
                "Name": getattr(it, "name", ""),
                "Domain": dom,
                "DataType": str(getattr(it, "dataType", "")),
                "CodeListRef": getattr(getattr(it, "codeList", None), "OID", ""),
            })

    vld = ET.SubElement(root, "ValueListDefs")
    for ig in (mdv.itemGroups or []):
        if _is_slice(ig):
            continue
        dom = _domain_name_of_ig(ig)
        if domains_set and dom not in domains_set:
            continue
        projection = project_valuelist_for_domain(mdv, dom)
        for var, entries in projection.items():
            if not entries:
                continue
            vl_el = ET.SubElement(vld, "ValueListDef", {"Domain": dom, "ItemName": var})
            for entry in entries:
                wc_oid = (entry.applicableWhen or [""])[0] if entry.applicableWhen else ""
                ET.SubElement(vl_el, "ValueListItemRef", {"WhereClauseRef": wc_oid})
    return ET.tostring(root, encoding="unicode")


def export_define_xml_10(mdv: MetaDataVersion, domains: Optional[List[str]] = None) -> str:
    root = ET.Element("Define10")
    cld = ET.SubElement(root, "CodeListDefs")
    for cl in (mdv.codeLists or []):
        cl_el = ET.SubElement(cld, "CodeListDef", {"OID": getattr(cl, "OID", "")})
        for cli in (cl.codeListItems or []):
            ET.SubElement(cl_el, "CodeListItem", {"CodedValue": str(getattr(cli, "codedValue", ""))}).text = str(getattr(cli, "decode", ""))
    idd = ET.SubElement(root, "ItemDefs")
    domains_set = set(domains or [])
    for ig in (mdv.itemGroups or []):
        if _is_slice(ig):
            continue
        dom = _domain_name_of_ig(ig)
        if domains_set and dom not in domains_set:
            continue
        for it in (ig.items or []):
            ET.SubElement(idd, "ItemDef", {
                "Name": getattr(it, "name", ""),
                "Domain": dom,
                "DataType": str(getattr(it, "dataType", "")),
                "CodeListRef": getattr(getattr(it, "codeList", None), "OID", ""),
            })
    return ET.tostring(root, encoding="unicode")


__all__ = [
    "load_mdv",
    "canonicalise_whereclause",
    "build_where_registry",
    "build_canonical_slices",
    "enforce_slice_invariants",
    "register_variables",
    "project_valuelist_for_domain",
    "serialize_canonical",
    "export_define_xml_21",
    "export_define_xml_10",
]

