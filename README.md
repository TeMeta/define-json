# Data Definition Specification

> [!NOTE]
> **CDISC has forked this project** — see
> [cdisc-org/DataExchange-DDS](https://github.com/cdisc-org/DataExchange-DDS).
>
> This project began life as **Define-JSON**. The previous
> [`TeMeta/define-json`](https://github.com/TeMeta/define-json) repository URL
> redirects here (GitHub preserves redirects when a repository is renamed).

Fixing Clinical Data Contracts at the Root

> “send us the DDS too so we know what's going on”

`data-definition-spec` (DDS) is a **standards-agnostic canonical model** for the meaning, structure, and governance of clinical data. The model is defined once (in LinkML) and **projects to** the standards you actually exchange in — CDISC (SDTM/ADaM/Define-XML), FHIR, OMOP, and SDMX — so no single standard owns it.

It describes data implementation and serves as a Data Contract for both:

1. **Demand**: Data Contract for what a particular analysis or data transfer requires (e.g. describe end-to-end transformations when planning a Clinical Trial)
2. **Supply**: Data Contract for what a particular provider promises to deliver (e.g. Data Transfer Agreements with each supplier)

In a clinical-trial context it complements the CDISC Unified Study Definitions ([USDM](https://github.com/cdisc-org/DDF-RA)) and [Dataset-JSON](https://github.com/cdisc-org/DataExchange-DatasetJson) — describing datasets and how they link causally to their context — but the model itself is not CDISC-derived.

[Documentation Site](https://temeta.github.io/data-definition-spec)

## How It's Built

DDS is a **single source of truth** with everything else generated from it:

- **LinkML schema** (`dds.yaml`) — the canonical model: classes, slots, enums, and cross-standard mappings in one place.
- **Neutral identity** — the `https://w3id.org/dds` namespace (`dds` prefix), independent of any single standards body.
- **Linked-data foundations** — reuses established vocabularies instead of reinventing them: SKOS (semantics), PROV-O (provenance), DCAT/DPROD (data products), ODRL (governance/policy), RDF Data Cube + SDMX (statistical structure), plus FHIR/OMOP/CDISC mappings carried on each element.
- **Generated artifacts** — JSON Schema, Pydantic models, and the documentation site are all produced from `dds.yaml` via LinkML generators; JSON-LD/OWL/SHACL are natural further outputs.

Because the model is defined once and projected outward, adding a new target standard is a mapping exercise, not a re-modelling one.

## 🚀 Quick Start

```bash
# Install dependencies
poetry install
```

The canonical model lives in **`dds.yaml`** (LinkML). Generate downstream artifacts from it:

```bash
make generate-json-schema     # -> generated/data-definition-spec-schema.json (JSON Schema)
make generate-pydantic        # -> generated/define.py (Pydantic models)
make docs                     # -> documentation site
```

**Define-XML is just one serialization facet** (alongside the FHIR/OMOP/SDMX projections), reached through the converter:

```bash
# Define-XML <-> DDS
poetry run python -m data_definition_spec xml2json data/define.xml data/output.json
poetry run python -m data_definition_spec json2xml data/input.json data/output.xml

# Render DDS as HTML (no CORS issues)
poetry run python -m data_definition_spec json2html input.json output.html
```

For complete documentation, see:

- **[CONVERSION_README.md](CONVERSION_README.md)** - Complete conversion guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference

**Example files**:

- `examples/minimal_define.json` - Minimal example with Conditions, WhereClauses, and ValueLists
- `examples/sample_dataset_*.json` - Dataset-JSON files for reverse engineering
- `data/defineV21-*.json` - Full real-world Data Definition Specification examples

## Reverse Engineering: Data → Metadata

Generate Data Definition Specification metadata from Dataset-JSON data files:

```bash
python scripts/reverse_engineer_define.py examples/sample_dataset_lb.json
```

**Outputs**:

- `define_metadata.json` - Data Definition Specification structures
- `sdmx_policy_suggestion.yaml` - SDMX policy suggestions
- `analysis_summary.json` - Statistics and confidence scores
- `reverse_engineering_report.md` - Analysis report

## Interactive Data Cube Pipeline

End-to-end demonstration notebook:

```bash
cd notebooks
jupyter lab datacube_end_to_end.ipynb
```

Demonstrates reverse engineering, schema validation, data cube construction, and interactive visualization.

## Context-Specific Definitions

> "Don't provide values without units"

`data-definition-spec` element definitions are context-specific by design. Every `Item` belongs to an `ItemGroup`, which can act as nested slices, enabling granular reusable definitions across contexts:

- CDISC Dataset Specification
- CDISC Dataset Specialisation (Biomedical Concept-specific slice templates)
- FHIR Profiles
- Clinical eSource Data Specs (Data Transfer Agreements)
- OMOP-CDM mappings
- Regulatory submissions (Define-XML)
- Dataset transformation specifications

Data Definition Specification links to `Coding`, `Concept` and `ConceptProperty` for structured semantic connections, enabling each data element to be mapped unambiguously to standard dictionaries/ontologies and abstract concepts.

> "Don't define derivation/origin for a field without knowing what the Biomedical Concept is being implemented"

## The Problem

> "Don't send data without its Definition"

<img src="images/throwing_vase_over_wall.png" alt="The status quo of silos, files and documents" width="350"/>

Clinical trial data exchange needs fixing. We need to be able to simultaneously speak in nuanced concepts and understand in specific self-explanatory structure. _The first step is agreeing on that structure_.

## Use Cases

This project started as part of CDISC 360i project, extending the current structure such that data specs to be drivers rather than simply descriptors of data transformations and transfer in clinical trials.

Any gaps that emerged during the project (e.g. linking abstract analysis concepts to data, granularity) could quickly be addressed by adapting this model.

**Dataset Transformation**: Represent source and target datasets in the same framework, with explicit transformation mappings.

**Regulatory Submissions**: Metadata manifest accompanying Dataset-JSON, specifying what was provided, its origins, and derivations.

**Data Transfer Agreements**: Bilateral agreements between research organizations and suppliers, specifying data structure, timing, and content. A DTA is a standalone `ProvisionAgreement` (provider, consumer, `dataFlow`) that embeds an agreed snapshot of the dataset spec and references the live spec for provenance. Delivery cadence is carried by `Dataflow.deliverySchedule` (ISO-8601 recurrence string by default, or a `Timing` object for clinical anchoring), and legal terms by `hasPolicy` (ODRL `Policy`/`Rule`/`Constraint`). The agreement/governance layer (`ProvisionAgreement`, `DataProvider`/`DataConsumer`, ODRL `Policy`) is domain-neutral; the transferred structure can be ODM `Item`s (CDISC) or, for non-clinical payloads, SDMX components / an `IsProfile.profile` URI with PROV-O `wasDerivedFrom` provenance. Generate a draft from any spec:

```bash
python scripts/dataset_spec_to_dta.py data/defineV21-SDTM.json LB \
  --provider-type Lab --cadence "R/2025-01-01/P1M" --permitted-purpose safety-reporting \
  --mappings examples/dta_mappings_LB.yaml \
  --out generated/dta_LB.provisionagreement.json
python scripts/render_dta_docx.py generated/dta_LB.provisionagreement.json \
  --source data/defineV21-SDTM.json --out generated/DTA_LB_draft.docx
```

`--mappings` merges multi-standard codings onto each variable (the same element carries CDISC + FHIR `Observation` + OMOP `MEASUREMENT` representations) and references a canonical `Concept` (`examples/concept_LABRESULT.reifiedconcept.json`) that bridges the three — the "model fabric" horizontal. `Coding` maps to `fhir:Coding`/`omop:Concept`, so no schema change is needed.

**Demand Data Contracts**: Analysis requests specifying how target datasets are derived from sources and expected structure.

**Data Product Catalog**: Enhanced metadata for data products including lineage, semantics, and derivations.

**Provenance Tracking**:

- `SourceItem` - Direct links to source documents, CRF forms, or datasets
- `wasDerivedFrom` - Template reuse (PROV-O based), independent instances

## Semantic Bridging

Data Definition Specification bridges implementation and meaning through:

- **`Coding`** - Semantic tags against known ontologies
- **`Concept`** - Links to abstract concepts (e.g., CDISC Biomedical Concepts)
- **`ConceptProperty`** - Properties of concepts in context

This enables comparison across implementations and links disparate structures to shared meaning.
