# Define-JSON: Data Implementation Definition

Fixing Clinical Data Contracts at the Root

> “send us the Define too so we know what's going on”

`define-json` is a description of data implementation, it can be used for both:

1. **Demand**: Data Contract for what a particular analysis or data transfer requires (e.g. describe end-to-end transformations when planning a Clinical Trial)
2. **Supply**: Data Contract for what a particular provider promises to deliver (e.g. Data Transfer Agreements with each supplier)

It is being designed in a Clinical Trial context to supplement the CDISC Unified Study Definitions ([USDM](https://github.com/cdisc-org/DDF-RA)) and [Dataset-JSON](https://github.com/cdisc-org/DataExchange-DatasetJson), providing a way to describe datasets and how they link causally to their context

[Documentation Site](https://temeta.github.io/define-json)

## 🔄 Quick Start: XML ↔ JSON Conversion

```bash
# Install dependencies
poetry install

# Convert Define-XML to Define-JSON
poetry run python -m define_json xml2json data/define.xml data/output.json

# Convert Define-JSON to Define-XML
poetry run python -m define_json json2xml data/input.json data/output.xml

# Convert to HTML (no CORS issues)
poetry run python -m define_json json2html input.json output.html
```

For complete documentation, see:

- **[CONVERSION_README.md](CONVERSION_README.md)** - Complete conversion guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference

**Example files**:

- `examples/minimal_define.json` - Minimal example with Conditions, WhereClauses, and ValueLists
- `examples/sample_dataset_*.json` - Dataset-JSON files for reverse engineering
- `data/defineV21-*.json` - Full real-world Define-JSON examples

## Reverse Engineering: Data → Metadata

Generate Define-JSON metadata from Dataset-JSON data files:

```bash
python scripts/reverse_engineer_define.py examples/sample_dataset_lb.json
```

**Outputs**:

- `define_metadata.json` - Define-JSON structures
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

`define-json` element definitions are context-specific by design. Every `Item` belongs to an `ItemGroup`, which can act as nested slices, enabling granular reusable definitions across contexts:

- CDISC Dataset Specification
- CDISC Dataset Specialisation (Biomedical Concept-specific slice templates)
- FHIR Profiles
- Clinical eSource Data Specs (Data Transfer Agreements)
- OMOP-CDM mappings
- Regulatory submissions (Define-XML)
- Dataset transformation specifications

Define-JSON links to `Coding`, `ReifiedConcept` and `ConceptProperty` for structured semantic connections, enabling each data element to be mapped unambiguously to standard dictionaries/ontologies and abstract concepts.

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

**Data Transfer Agreements**: Bilateral agreements between research organizations and suppliers, specifying data structure, timing, and content.

**Demand Data Contracts**: Analysis requests specifying how target datasets are derived from sources and expected structure.

**Data Product Catalog**: Enhanced metadata for data products including lineage, semantics, and derivations.

**Provenance Tracking**:

- `SourceItem` - Direct links to source documents, CRF forms, or datasets
- `wasDerivedFrom` - Template reuse (PROV-O based), independent instances

## Semantic Bridging

Define-JSON bridges implementation and meaning through:

- **`Coding`** - Semantic tags against known ontologies
- **`ReifiedConcept`** - Links to abstract concepts (e.g., CDISC Biomedical Concepts)
- **`ConceptProperty`** - Properties of concepts in context

This enables comparison across implementations and links disparate structures to shared meaning.
