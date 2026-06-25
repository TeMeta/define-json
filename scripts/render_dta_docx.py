#!/usr/bin/env python3
"""Render a draft DTA (ProvisionAgreement JSON) to a human-readable Word document.

Reads the JSON produced by ``dataset_spec_to_dta.py`` and lays it out as a draft
agreement: parties, study context, scope, the variable-level specification table,
provenance, and a governance/legal section.

The governance section is intentionally a set of headed placeholders. Those terms
are not derivable from a dataset specification and the model has no structured slot
for them (see notes); a human completes them.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

PLACEHOLDER = "TODO_PLACEHOLDER"
SHOWN = "⟪ TO BE COMPLETED ⟫"

# DTA terms that a dataset spec does not carry and the model has no slot for.
GOVERNANCE_TERMS = [
    ("Permitted purpose", "The specific purpose(s) for which the transferred data may be used."),
    ("Confidentiality", "Confidentiality obligations and exceptions."),
    ("Data protection / personal data", "PII handling, lawful basis, pseudonymisation, cross-border transfer."),
    ("Transfer mechanism", "Channel, format, encryption, and access controls for each transfer."),
    ("Retention and destruction", "How long data is held and how it is destroyed."),
    ("Liability and term", "Liability, indemnities, effective date, and termination."),
]


def shown(value: Any) -> str:
    """Replace the placeholder sentinel with a readable marker."""
    return SHOWN if value == PLACEHOLDER else str(value)


def text_of(value: Any) -> str:
    """Flatten a value that may be a plain string or a TranslatedText object."""
    if isinstance(value, dict):
        return value.get("value") or value.get("content") or json.dumps(value)
    return "" if value is None else str(value)


def add_kv_table(doc: Document, rows: list[tuple[str, str]]) -> None:
    table = doc.add_table(rows=0, cols=2)
    table.style = "Light Grid Accent 1"
    for key, val in rows:
        cells = table.add_row().cells
        cells[0].paragraphs[0].add_run(key).bold = True
        cells[1].text = val


def build_doc(dta: dict[str, Any], source_path: str) -> Document:
    flow = dta.get("dataFlow", {})
    dsd = flow.get("structure", {})
    items = dsd.get("items", [])
    provider = dta.get("provider", {})

    doc = Document()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("DATA TRANSFER AGREEMENT")
    run.bold = True
    run.font.size = Pt(20)
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub.add_run(f"DRAFT {dta.get('version', '')}".strip())
    sub_run.bold = True
    sub_run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    doc.add_paragraph(text_of(dta.get("label")))

    note = doc.add_paragraph()
    note.add_run(
        "This draft was generated from a dataset specification. Structure, "
        "variables and provenance are derived from the source spec. Items marked "
        f"{SHOWN} are not present in the spec and must be completed by a human."
    ).italic = True

    doc.add_heading("1. Parties", level=1)
    add_kv_table(doc, [
        ("Data Provider", shown(provider.get("name"))),
        ("Provider type", str(provider.get("type", ""))),
        ("Data Consumer", shown(dta.get("consumer"))),
    ])

    doc.add_heading("2. Study context", level=1)
    add_kv_table(doc, [
        ("Agreement ID", str(dta.get("OID", ""))),
        ("Agreement name", str(dta.get("name", ""))),
        ("Source specification", str(Path(source_path).name)),
    ])
    doc.add_paragraph(text_of(dta.get("description")))

    doc.add_heading("3. Scope of transfer", level=1)
    add_kv_table(doc, [
        ("Domain", str(dsd.get("domain", ""))),
        ("Dataset structure", text_of(dsd.get("structure"))),
        ("Variables under agreement", str(len(items))),
        ("Key structure", ", ".join(dsd.get("keySequence", [])) or "—"),
    ])

    schedule = flow.get("deliverySchedule") or []
    doc.add_heading("4. Transfer schedule", level=1)
    if schedule:
        rows = []
        for t in schedule:
            if isinstance(t, dict):  # Timing object (clinical anchoring)
                rows.append((t.get("name") or t.get("OID") or "Schedule",
                             f"{t.get('value', '')} ({t.get('type', '')})"))
            else:  # neutral ISO-8601 recurrence string
                rows.append(("Cadence (ISO-8601)", str(t)))
        add_kv_table(doc, rows)
    else:
        p = doc.add_paragraph()
        p.add_run(f"{SHOWN} ").bold = True
        p.add_run("Delivery cadence, first/last delivery and turnaround. Model "
                  "slot Dataflow.deliverySchedule (ISO-8601 in Timing.value).").italic = True

    doc.add_heading("5. Variable specification", level=1)
    concept = dsd.get("implementsConcept")
    if concept:
        p = doc.add_paragraph()
        p.add_run("Canonical concept: ").bold = True
        p.add_run(f"{concept} (Registry) — cross-standard codings shown per variable.")
    cols = ["#", "Name", "Description", "Type", "Len", "Mand.", "Codelist", "Standards (FHIR/OMOP/…)"]
    table = doc.add_table(rows=1, cols=len(cols))
    table.style = "Light Grid Accent 1"
    for i, head in enumerate(cols):
        table.rows[0].cells[i].paragraphs[0].add_run(head).bold = True
    for idx, item in enumerate(items, start=1):
        codings = "; ".join(
            f"{c.get('codeSystem')}:{c.get('code')}"
            for c in (item.get("coding") or [])
        )
        values = [
            str(idx),
            text_of(item.get("name")),
            text_of(item.get("description")),
            str(item.get("dataType", "")),
            str(item.get("length", "")),
            "Y" if item.get("mandatory") else "",
            str(item.get("codeList", "")),
            codings,
        ]
        cells = table.add_row().cells
        for i, val in enumerate(values):
            cells[i].text = val

    doc.add_heading("6. Provenance", level=1)
    src = dta.get("source", {})
    add_kv_table(doc, [
        ("Source document", shown(src.get("name"))),
        ("Source type", str(src.get("resourceType", ""))),
        ("Source version", str(src.get("version", ""))),
        ("Source URI", shown(src.get("href"))),
    ])

    doc.add_heading("7. Governance and legal terms", level=1)
    policies = dta.get("hasPolicy") or []
    if policies:
        for pol in policies:
            doc.add_paragraph(
                f"ODRL {pol.get('policyType', 'Policy')} — assigner: "
                f"{shown(pol.get('assigner'))}, assignee: {shown(pol.get('assignee'))}"
            )
            for kind in ("permission", "prohibition", "obligation"):
                for rule in pol.get(kind, []):
                    cons = "; ".join(
                        f"{c.get('leftOperand')} {c.get('operator')} {c.get('rightOperand')}"
                        for c in rule.get("constraint", [])
                    )
                    p = doc.add_paragraph(style="List Bullet")
                    p.add_run(f"{kind}: ").bold = True
                    text = f"{rule.get('action')} → {rule.get('target', '')}"
                    if cons:
                        text += f" [{cons}]"
                    p.add_run(text)
    doc.add_paragraph(
        "Terms below are not derivable from a dataset specification; complete "
        "before execution (model: ProvisionAgreement.hasPolicy → ODRL Policy)."
    )
    for term, hint in GOVERNANCE_TERMS:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(f"{term}: ").bold = True
        p.add_run(f"{SHOWN} — {hint}").italic = True

    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = f"Draft generated from {Path(source_path).name} · define-json model"
    return doc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dta_json", type=Path, help="ProvisionAgreement JSON file")
    parser.add_argument("--source", default="(source spec)",
                        help="Name/path of the source spec, for provenance display")
    parser.add_argument("--out", type=Path, required=True, help="Output .docx path")
    args = parser.parse_args()

    dta = json.loads(args.dta_json.read_text())
    doc = build_doc(dta, args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(args.out))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
