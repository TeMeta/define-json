## Data Implementation Definition: Fixing Clinical Data Contracts at the Root

> “send us the Define too so we know what's going on”

`define-json` is a description of data implementation, it can be used for both:

1. **Demand**: Data Contract for what a particular analysis or data transfer requires (e.g. describe end-to-end transformations when planning a Clinical Trial)
2. **Supply**: Data Contract for what a particular provider promises to deliver (e.g. Data Transfer Agreements with each supplier)

It is being designed in a Clinical Trial context to supplement the CDISC Unified Study Definitions ([USDM](https://github.com/cdisc-org/DDF-RA)) and [Dataset-JSON](https://github.com/cdisc-org/DataExchange-DatasetJson), providing a way to describe datasets and how they link causally to their context

[Documentation Site](https://temeta.github.io/define-json)

## 🔄 Quick Start: XML ↔ JSON Conversion

### IR Pipeline (slices + ValueList + XML exports)

Run the canonical IR pipeline using only the generated `define.py` classes:

```bash
# Install deps
poetry install

# Run on a Define-JSON file
poetry run define-ir path/to/input.json --domains CE AE

# Outputs (alongside input unless --out is provided):
# - input.canonical.json          (canonical ordering, registry applied)
# - input.valuelist_projection.json (diagnostic per-domain variable-first contexts)
# - input.define21.xml            (minimal Define-XML 2.1)
# - input.define10.xml            (flattened Define-XML 1.0)
```

For complete bidirectional conversion between Define-XML and Define-JSON, see:
- **[CONVERSION_README.md](CONVERSION_README.md)** - Complete guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet

### Basic Usage
```bash
# Recommended: Use Poetry (handles virtual environment automatically)
poetry run python -m define_json xml2json data/define.xml data/output.json
poetry run python -m define_json json2xml data/input.json data/output.xml

# Alternative: Set PYTHONPATH manually
PYTHONPATH=src python -m define_json xml2json data/define.xml data/output.json
PYTHONPATH=src python -m define_json json2xml data/input.json data/output.xml

# From any other directory
PYTHONPATH=/path/to/define-json/src python -m define_json xml2json data/define.xml data/output.json
```

### Viewing XML Files with Stylesheets

Generated XML files include an XSL stylesheet reference for proper rendering. Due to browser security policies, you may encounter CORS errors when opening XML files directly. Here are the solutions:

#### Option 1: Use a Local Web Server (Recommended)
```bash
# Navigate to your XML file directory
cd /path/to/your/xml/files
python -m http.server 8000

# Then open: http://localhost:8000/your-file.xml
```

#### Option 2: Generate HTML Directly (Recommended)
```bash
# Convert JSON directly to HTML (no CORS issues!)
poetry run python -m define_json json2html input.json output.html

# Convert existing XML to HTML
poetry run python -m define_json xml2html input.xml output.html

# Use custom XSL stylesheet
poetry run python -m define_json json2html input.json output.html --xsl ./custom-style.xsl
```

#### Option 3: Configure Stylesheet Path
```bash
# Use relative path (works when XSL is in same directory)
poetry run python -m define_json json2xml input.json output.xml --stylesheet "./define2-1.xsl"

# Use absolute URL (if you have XSL hosted online)
poetry run python -m define_json json2xml input.json output.xml --stylesheet "https://example.com/define2-1.xsl"
```

## 🆕 Reverse Engineering: Data → Metadata

> "Don't send data without its Define"

**New capability**: Automatically generate Define-JSON metadata from Dataset-JSON data files.

```bash
# Run on sample datasets
make reverse-engineer-lb  # Laboratory dataset
make reverse-engineer-vs  # Vital Signs dataset

# Or run directly
python scripts/reverse_engineer_define.py examples/sample_dataset_lb.json
```

**Outputs** (4 files):
1. `define_metadata.json` - Define-JSON ItemDef/ItemGroupDef structures
2. `sdmx_policy_suggestion.yaml` - Auto-suggested SDMX Dimension/Measure/Attribute policy  
3. `analysis_summary.json` - Statistics and confidence scores
4. `reverse_engineering_report.md` - Human-readable analysis report

**What it does**:
- ✅ Detects dataset structure (vertical vs horizontal)
- ✅ Classifies variables (IDENTIFIER, TIMING, TOPIC, RESULT, ATTRIBUTE)
- ✅ Suggests SDMX roles (Dimension, Measure, Attribute)
- ✅ Generates ItemGroups with WHERE clauses for topics
- ✅ Provides confidence scores for all classifications

**Use cases**:
- Bootstrap metadata for legacy datasets
- Validate metadata-data consistency
- Auto-generate SDMX policies
- Quick prototyping of new analyses

See **[REVERSE_ENGINEERING_SUMMARY.md](REVERSE_ENGINEERING_SUMMARY.md)** for complete guide.

## Context is everything

> "Don't provide values without units"

`define-json` element definitions are context-specific by design, only applicable to some defined local scope.

By being so strict about scope (every `Item` must belong to an `ItemGroup`, which can in turn can act as nested slices), granular reusable definitions can be created and applied to a wide variety of contexts.

> “Don't quote someone without knowing what else they were saying and why

The context that Define is implementing, i.e. _your_ context, is up to you - make sure to record the surrounding context on your end so that the definitions within can be used and reused accurately:

* CDISC Dataset Specification (actual data)
* CDISC Dataset Specialisation (template in the context of Biomedical Concept)
* OpenStudyBuilder Activity
* FHIR Profile or IG
* Clinical Recording Model
* Structured Data Collection forms / apps
* Clinical eSource Data Spec (a.k.a. Data Transfer Agreement, Data Contract)
* OMOP-CDM mappings
* Dataset Transformation Metaprogramming
* Define-JSON / Define-XML for regulatory submission
* AI model feature spec

> “Don't send data without its Define”

<img src="https://github.com/TeMeta/define-json/blob/gh-pages/images/throwing_vase_over_wall.png?raw=true" alt="The status quo of silos, files and documents" width="350"/>

Clinical trial data exchange needs fixing.  We need to be able to simultaneously speak in nuanced concepts and understand in specific self-explanatory structure. _The first step is agreeing on that structure_.

Being able to iterate rapidly is important to the early stages of development of this standard. _Fix what's broken. Improve what works. Repeat._

> “Don't define derivation/origin for a field without knowing what the Biomedical Concept is being implemented”

Define-JSON details implementation, but also links to `Coding`, `ReifiedConcept` and `ConceptProperty` for structured semantic connections, i.e. enabling each data element to be mapped unambiguously to standard dictionaries/ontologies, abstract concepts, and their properties.

The definition of [something] combines its abstract / template form with a context, then fleshes out that combined context.

* FHIR Profile is a implementation of a FHIR Resource template in the context of some healthcare or research authority
* A granular definition for some Biomedical Concept (BC) is an implementation of a property of that BC in context of the standard being implemented
* A Biomedical Concept Property is an implementation of some abstract Data Element Concept in context of a BC
* A dataset is an implementation of a specified demand data contract in the context of a specific transfer/timepoint
* Transformation code is the implementation of described transformation in the context of a specific environment

## Usages

### Dataset Transformation Program

Both source and target datasets represented in the same framework, with target referencing back to how the source is used explicitly

From this a full dataset transformation expression and/or executable program script can be generated.

### Regulatory Clinical Trial Submission (Supply Data Contract)

Metadata to accompany Dataset-JSON, a manifest of specifying precisely what has been provided as well as its origins and how it was derived

### DTA (bilateral agreement - Supply & Demand Data Contract)

Data Transfer Agreements are based on the demands specified by the research organisation, against which the supplier agrees to deliver specific data at specific times using a specific structure.

If the Supply has an opinionated structure it can promise to deliver that, or if they have no opinionated structure they can provide the precise structure demanded

### Demand Data Contracts

A search, analysis or data access request is entered

* specifying how target (including intermediate datasets) are derived from source
* specifying the expected content and structure

This allows us to specify e.g. a FHIR Data Contract, a promise to provide a particular Resource structure, and understand how it will be interpreted by analysis in tabular form

### Manifest

Contextual / semantic / derivation / dependency / traceability / structural metadata to supplement a data transfer

### Data Product Catalog

A given set of data products can be described using define-json to provide enhanced metadata around lineage, semantics and derivations.

In the context of a Clinical Data Fabric/Mesh/Lake, MDR, or Operational Data Store: define-json can be used as a means of recording granular value-level lineage within dataset, allowing tooling to show dependencies and impact analysis.

Define can even be used a psuedo 'MDR' with the way it tracks dependencies, provenance and impact analysis.

- `SourceItem` structure has detailed information about where the value came from, whether it's a document or CRF form or source dataset with its own referencable `Item`.
- `wasDerivedFrom` relationship is borrows from PROV-O (Provenance Ontology) exclusively to denote template reuse i.e. "I am reusing this definition from somewhere else and making it my own".
- `SourceItem` denotes a direct link. Changes to the source will impact the target. Conversely `wasDerivedFrom` relationship only provides provenance and lets you identify reuse without coupling the instances - you can modify each instance independently.

## Define bridges implementation and meaning

Because Define is implementation-agnostic, it can be used to compare across different implementations e.g. establishing changes between study-specific implementation and a standard template.

What relates both disparate implementations is explicit link to an independent meaning.

The `Coding` class semantically-tags all identifiable definitions against known ontologies.

We can also reference to compound 'concept' structures such as the CDISC Biomedical Concept, which [reifies](https://dictionary.cambridge.org/dictionary/english/reify) a clinical Observation topic and specifies a set of data properties in context of that topic, so that we can use them to define abstract constraints common to all implementations while staying granular to the topic.

These explicit links can be used to bridge the implementation to the meaningful thing that it is implementing