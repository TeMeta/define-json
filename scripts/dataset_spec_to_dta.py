#!/usr/bin/env python3
"""Generate a draft Data Transfer Agreement (DTA) from a dataset specification.

A DTA is modelled as a standalone ``ProvisionAgreement`` (define.yaml): an
agreement between a ``DataProvider`` and a consumer covering a ``Dataflow``
whose ``structure`` is a ``DataStructureDefinition`` carrying the variable-level
``Item`` specification.

Design decisions (see commentary in the accompanying notes):
- The agreement is a *separate* document that references the source spec by
  ``fileOID``/``href``. The schema's tree_root (MetaDataVersion) has no slot that
  contains a ProvisionAgreement, so a DTA cannot be embedded in a define file.
- Nothing is invented. Everything in the output is either copied from the source
  spec or supplied by the caller. Fields that a DTA needs but a dataset spec does
  not carry (legal party identities, permitted purpose, transfer mechanism) are
  emitted as explicit ``TODO_PLACEHOLDER`` markers for a human to complete.

Usage:
    python scripts/dataset_spec_to_dta.py SOURCE_DEFINE.json DOMAIN [options]

Example:
    python scripts/dataset_spec_to_dta.py data/defineV21-SDTM.json LB \\
        --out generated/dta_LB.provisionagreement.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Valid DataType enum members used when inferring types from raw data.
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ].*)?$")

# Map common source dataType aliases (ODM/Dataset-JSON) onto data-definition-spec DataType.
_DTYPE_ALIAS = {"string": "text", "char": "text", "decimal": "float",
                "number": "float", "int": "integer"}


def _norm_dtype(dt: str | None) -> str:
    dt = dt or "text"
    return _DTYPE_ALIAS.get(dt.lower(), dt)

PLACEHOLDER = "TODO_PLACEHOLDER"

# Item slots that are meaningful in a transfer spec and are copied verbatim from
# the source ItemGroup. Anything not in this list is dropped to keep the
# agreement focused on what is being transferred.
ITEM_SLOTS = (
    "OID", "name", "description", "label", "mandatory",
    "dataType", "length", "codeList", "applicableWhen", "origin",
)


def _infer_type(values: list[str]) -> str:
    """Infer a data-definition-spec DataType from sampled string values."""
    vals = [v for v in values if v not in ("", None)]
    if not vals:
        return "text"

    def all_int() -> bool:
        try:
            for v in vals:
                int(v)
            return True
        except ValueError:
            return False

    def all_float() -> bool:
        try:
            for v in vals:
                float(v)
            return True
        except ValueError:
            return False

    if all_int():
        return "integer"
    if all_float():
        return "float"
    if all(_ISO_DATE.match(str(v)) for v in vals):
        return "datetime"
    return "text"


def _spec_from_csv(path: Path) -> dict[str, Any]:
    """Build a minimal data-definition-spec spec from a CSV: one ItemGroup, inferred types."""
    with path.open(newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        raise SystemExit(f"CSV is empty: {path}")
    header, data = rows[0], rows[1:]
    domain = re.sub(r"[^A-Za-z0-9]", "", path.stem).upper()[:8] or "DATASET"
    items = []
    for i, name in enumerate(header):
        col = [r[i] for r in data if i < len(r)]
        dtype = _infer_type(col)
        item = {"OID": f"IT.{domain}.{name}", "name": name,
                "description": name, "dataType": dtype}
        if dtype == "text":
            item["length"] = max((len(str(v)) for v in col), default=1)
        items.append(item)
    return {"itemGroups": [{
        "OID": f"IG.{domain}", "name": domain, "domain": domain,
        "structure": "One record per row", "items": items,
    }]}


def _spec_from_dataset_json(data: dict[str, Any]) -> dict[str, Any]:
    """Build a data-definition-spec spec from a Dataset-JSON file (clinicalData.itemGroupData)."""
    cd = data["clinicalData"]
    groups = []
    for ig_oid, ig in cd.get("itemGroupData", {}).items():
        name = ig_oid.split(".")[-1]
        items = []
        for c in ig.get("columns", []):
            item = {"OID": c.get("itemOID") or f"IT.{name}.{c['name']}",
                    "name": c["name"],
                    "description": c.get("label", c["name"]),
                    "dataType": _norm_dtype(c.get("dataType"))}
            if c.get("length"):
                item["length"] = c["length"]
            items.append(item)
        groups.append({"OID": ig_oid, "name": name, "domain": name,
                       "structure": "One record per row", "items": items})
    spec: dict[str, Any] = {"itemGroups": groups}
    if cd.get("studyOID"):
        spec["studyOID"] = spec["studyName"] = cd["studyOID"]
    return spec


def load_spec(path: Path) -> dict[str, Any]:
    """Load any supported spec/dataset and normalise to a data-definition-spec dict.

    Supported: data-definition-spec (.json with 'itemGroups'), Dataset-JSON (.json with
    'clinicalData'), CSV (.csv), and data-definition-spec-as-YAML (.yaml/.yml). Define-XML
    must be converted first (the message says how).
    """
    if not path.exists():
        raise SystemExit(f"Source spec not found: {path}")
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return _spec_from_csv(path)
    if suffix == ".xml":
        raise SystemExit(
            "Define-XML detected. Convert it first, then pass the JSON:\n"
            "  python -m data_definition_spec xml2json <input.xml> <output.json>"
        )
    if suffix in (".yaml", ".yml"):
        data = yaml.safe_load(path.read_text())
        if isinstance(data, dict) and "itemGroups" in data:
            return data
        raise SystemExit("YAML spec must be data-definition-spec shaped (contain 'itemGroups').")
    if suffix == ".json":
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Source is not valid JSON ({path}): {exc}")
        if "itemGroups" in data:
            return data                          # data-definition-spec
        if "clinicalData" in data:
            return _spec_from_dataset_json(data)  # Dataset-JSON
        raise SystemExit(
            "Unrecognised JSON: expected data-definition-spec ('itemGroups') or "
            "Dataset-JSON ('clinicalData')."
        )
    raise SystemExit(
        f"Unsupported input type {suffix!r}. Use data-definition-spec/Dataset-JSON (.json), "
        "CSV (.csv), or data-definition-spec YAML (.yaml)."
    )


def find_item_group(spec: dict[str, Any], domain: str) -> dict[str, Any]:
    """Return the ItemGroup for ``domain``, matching on domain or name.

    Raises with the list of available domains if not found, so the caller is not
    left guessing.
    """
    groups = spec.get("itemGroups") or []
    if not groups:
        raise SystemExit("No itemGroups found in source spec.")
    available = [g.get("domain") or g.get("name") or g.get("OID") for g in groups]
    if not domain:
        if len(groups) == 1:
            return groups[0]
        raise SystemExit(
            "Multiple domains present; specify one with the DOMAIN argument: "
            f"{', '.join(str(a) for a in available)}"
        )
    for group in groups:
        if group.get("domain") == domain or group.get("name") == domain:
            return group
    raise SystemExit(
        f"Domain {domain!r} not found in source spec. "
        f"Available: {', '.join(str(a) for a in available)}"
    )


def collect_items(item_group: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect top-level items plus any items nested in slices (e.g. ValueLists).

    Slice items are value-level specialisations; a transfer spec needs them too,
    so they are flattened into the agreed structure.
    """
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    def take(raw_items: list[dict[str, Any]]) -> None:
        for item in raw_items or []:
            oid = item.get("OID")
            if oid in seen:
                continue
            seen.add(oid)
            items.append({k: item[k] for k in ITEM_SLOTS if k in item})

    take(item_group.get("items", []))
    for slice_ in item_group.get("slices", []):
        take(slice_.get("items", []))
    return items


def apply_mappings(dsd: dict[str, Any], items: list[dict[str, Any]],
                   mappings: dict[str, Any]) -> None:
    """Merge multi-standard (FHIR/OMOP/...) codings into items by variable name,
    and attach the canonical concept reference. Mutates dsd/items in place.

    Codings are appended to any existing item codings rather than replacing them.
    """
    concept = mappings.get("implementsConcept")
    if concept:
        dsd["implementsConcept"] = concept  # OID reference into the Registry

    by_name = mappings.get("variables", {})
    for item in items:
        spec = by_name.get(item.get("name"))
        if not spec or not spec.get("coding"):
            continue
        item.setdefault("coding", []).extend(spec["coding"])


def build_dta(
    spec: dict[str, Any],
    item_group: dict[str, Any],
    *,
    provider_name: str,
    provider_type: str,
    consumer_name: str,
    cadence: str | None = None,
    permitted_purpose: str | None = None,
    mappings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble a ProvisionAgreement dict from the source spec and party inputs."""
    domain = item_group.get("domain") or item_group.get("name")
    study = spec.get("studyName") or spec.get("studyOID") or PLACEHOLDER
    protocol = spec.get("protocolName") or PLACEHOLDER
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    items = collect_items(item_group)

    dsd = {
        "OID": f"DSD.{domain}",
        "name": domain,
        "description": item_group.get("description"),
        "domain": domain,
        "structure": item_group.get("structure"),
        # Carry the source ItemGroupType only if present; do not invent one.
        "type": item_group.get("type"),
        # keySequence references Item OIDs in the structure; carried verbatim.
        "keySequence": item_group.get("keySequence", []),
        "items": items,
    }
    dsd = {k: v for k, v in dsd.items() if v is not None}

    if mappings:
        apply_mappings(dsd, items, mappings)

    dataflow = {
        "OID": f"DF.{domain}",
        "name": f"{domain}_transfer",
        "label": f"{domain} data transfer",
        "version": "0.1-draft",
        "structure": dsd,
    }

    # Agreement-level delivery schedule (Dataflow.deliverySchedule). Emitted as a
    # domain-neutral ISO-8601 recurrence string (no clinical Timing semantics).
    # Only emitted when the caller supplies a cadence; never invented.
    if cadence:
        dataflow["deliverySchedule"] = [cadence]  # e.g. "R/2025-01-01/P1M"

    provider = {
        "OID": f"DP.{domain}",
        "name": provider_name,
        "type": provider_type,
        "role": "Data Provider",
        "providesDataFor": [dataflow["OID"]],
    }

    # Provenance back to the source spec (the "Definition" the data travels with).
    source = {
        "OID": f"RES.SRC.{domain}",
        "name": spec.get("fileOID") or spec.get("OID") or PLACEHOLDER,
        "resourceType": spec.get("fileType", "Data Definition Specification"),
        "version": spec.get("defineVersion") or spec.get("odmVersion"),
        "href": PLACEHOLDER,  # URI of the source define document
    }
    source = {k: v for k, v in source.items() if v is not None}

    dta = {
        "OID": f"PA.DTA.{domain}",
        "name": f"DTA-{domain}-{protocol}",
        "label": f"Data Transfer Agreement — {domain} — {study}",
        "description": (
            f"Draft Data Transfer Agreement for supply of {domain} domain data "
            f"for study {study} (protocol {protocol}). Structure and provenance "
            f"derived from the source dataset specification; commercial and legal "
            f"terms to be completed."
        ),
        "version": "0.1-draft",
        "mandatory": True,
        "lastUpdated": now,
        "purpose": (
            "Bilateral agreement specifying the structure, content and provenance "
            "of data transferred from provider to consumer."
        ),
        "provider": provider,
        "consumer": consumer_name,
        "dataFlow": dataflow,
        "source": source,
    }

    # ODRL Agreement policy. Only emitted when the caller supplies a permitted
    # purpose; legal terms are never invented from the spec.
    if permitted_purpose:
        dta["hasPolicy"] = [{
            "OID": f"POL.{domain}",
            "name": f"{domain}_terms",
            "policyType": "Agreement",
            "assigner": provider_name,
            "assignee": consumer_name,
            "permission": [{
                "OID": f"RULE.{domain}.USE",
                "action": "use",
                "target": dataflow["OID"],
                "constraint": [{
                    "OID": f"CON.{domain}.PURPOSE",
                    "leftOperand": "purpose",
                    "operator": "eq",
                    "rightOperand": permitted_purpose,
                }],
            }],
        }]
    return dta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path,
                        help="Source spec/dataset: data-definition-spec or Dataset-JSON (.json), "
                             "CSV (.csv), or data-definition-spec YAML (.yaml)")
    parser.add_argument("domain", nargs="?", default=None,
                        help="Domain / ItemGroup to put under agreement (e.g. LB). "
                             "Optional when the source has a single group.")
    parser.add_argument("--provider-name", default=PLACEHOLDER,
                        help="Legal entity of the data provider (not in the spec)")
    parser.add_argument("--provider-type", default="Lab",
                        choices=["Sponsor", "Site", "CRO", "Lab", "TechnologyProvider", "Other"],
                        help="OrganizationType of the provider")
    parser.add_argument("--consumer-name", default=PLACEHOLDER,
                        help="Legal entity of the data consumer / sponsor (not in the spec)")
    parser.add_argument("--cadence", default=None,
                        help="Delivery cadence as an ISO-8601 repeating interval "
                             "(e.g. 'R/2025-01-01/P1M'). Not derivable from the spec.")
    parser.add_argument("--permitted-purpose", default=None,
                        help="Permitted-purpose constraint for an ODRL Agreement "
                             "policy (e.g. 'safety-reporting'). Not derivable from the spec.")
    parser.add_argument("--mappings", type=Path, default=None,
                        help="YAML/JSON file of multi-standard codings (FHIR/OMOP/...) "
                             "and a canonical implementsConcept OID, merged into the structure.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output path (default: stdout)")
    args = parser.parse_args()

    spec = load_spec(args.source)
    item_group = find_item_group(spec, args.domain)
    mappings = yaml.safe_load(args.mappings.read_text()) if args.mappings else None
    dta = build_dta(
        spec, item_group,
        provider_name=args.provider_name,
        provider_type=args.provider_type,
        consumer_name=args.consumer_name,
        cadence=args.cadence,
        permitted_purpose=args.permitted_purpose,
        mappings=mappings,
    )

    text = json.dumps(dta, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n")
        n_items = len(dta["dataFlow"]["structure"].get("items", []))
        print(f"Wrote {args.out} ({n_items} items under agreement)")
    else:
        print(text)


if __name__ == "__main__":
    main()
