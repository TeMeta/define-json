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


def _canonical_where_payload(where: WhereClause, mdv: Optional[MetaDataVersion] = None) -> Dict[str, Any]:
    """
    Build canonical payload for WhereClause.
    
    Handles both string OID references and Condition objects.
    """
    conditions = where.conditions or []
    canon_conditions: List[Dict[str, Any]] = []
    
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
        
        checks = cond.rangeChecks or []
        canon_checks: List[Dict[str, Any]] = []
        for rc in checks:
            comparator = getattr(rc, "comparator", None)
            values = [ _normalise_check_value(v) for v in (rc.checkValues or []) ]
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
        canon_conditions.append({"checks": canon_checks})
    canon_conditions.sort(key=lambda d: json.dumps(d, sort_keys=True))
    return {"conditions": canon_conditions}


def canonicalise_whereclause(where: WhereClause, mdv: Optional[MetaDataVersion] = None) -> str:
    """
    Create canonical hash ID for WhereClause.
    
    Args:
        where: WhereClause to canonicalise
        mdv: Optional MetaDataVersion to resolve Condition OID references
    """
    payload = _canonical_where_payload(where, mdv)
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"WC.{hashlib.sha256(data).hexdigest()[:16]}"


def build_where_registry(mdv: MetaDataVersion) -> Dict[str, WhereClause]:
    """Build canonical WhereClause registry and remap all references to canonical hashes."""
    registry: Dict[str, WhereClause] = {}
    old_to_canonical: Dict[str, str] = {}
    
    # Canonicalise all WhereClauses and build mapping from old OID -> canonical hash
    for wc in (mdv.whereClauses or []):
        old_oid = wc.OID
        canonical_wid = canonicalise_whereclause(wc, mdv)
        
        if canonical_wid not in registry:
            # First WhereClause with this canonical hash - keep it
            wc.OID = canonical_wid
            registry[canonical_wid] = wc
        
        # Map old OID to canonical hash (for remapping applicableWhen)
        if old_oid:
            old_to_canonical[old_oid] = canonical_wid
    
    # Remap all applicableWhen to use canonical hashes
    def _remap_oids(obj: Any) -> None:
        """Remap applicableWhen OIDs to canonical hashes."""
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
    
    # Remove duplicate WhereClauses from the list
    mdv.whereClauses = list(registry.values())
    
    return registry


def _is_slice(ig: ItemGroup) -> bool:
    return str(getattr(ig, "type", "")) == "DataSpecialization"


def _domain_name_of_ig(ig: ItemGroup) -> str:
    return getattr(ig, "domain", None) or getattr(ig, "name", None) or ""


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

