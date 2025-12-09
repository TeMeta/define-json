# Examples Directory

This directory contains example files demonstrating different aspects of Define-JSON.

## Define-JSON Examples

### `minimal_define.json`
**Purpose**: Minimal, readable example showing core Define-JSON concepts

**Demonstrates**:
- ✅ **Conditions** as separate objects with RangeChecks
- ✅ **WhereClauses** referencing Conditions by OID string
- ✅ **ValueLists** nested in `slices` arrays (not top-level)
- ✅ **Items** with `applicableWhen` references to WhereClauses
- ✅ **CodeLists** with CodeListItems
- ✅ Basic ItemGroup structure

**Key Concepts**:
- Conditions define logical checks (e.g., `VSTESTCD EQ "SYSBP"`)
- WhereClauses combine Conditions (using AND logic)
- Items reference WhereClauses via `applicableWhen` (using OR logic)
- ValueLists group context-specific items and are nested in parent ItemGroup's `slices`

**Usage**:
```python
from define_json.utils.ir import load_mdv
from pathlib import Path

mdv = load_mdv(Path('examples/minimal_define.json'))
print(f"Loaded {len(mdv.itemGroups)} ItemGroup(s)")
```

### `concept_method_example.json`
**Purpose**: Example demonstrating ReifiedConcepts, Methods with FormalExpressions, and derived Items

**Demonstrates**:
- ✅ **ReifiedConcepts** with ConceptProperties (stored in `_reifiedConcepts` for demonstration)
- ✅ **Methods** with `implementsConcept` references
- ✅ **FormalExpressions** with Parameters and returnValue
- ✅ **Parameters** referencing ConceptProperties and source Items
- ✅ **Derived Items** using Methods and referencing ConceptProperties
- ✅ **Origin** with `sourceItems` for derived data

**Key Concepts**:
- ReifiedConcepts define abstract concepts (e.g., "Body Mass Index") with properties
- Methods implement concepts using FormalExpressions (e.g., Python code)
- Parameters map expression variables to ConceptProperties and source Items
- Items can reference Methods via `method` field and ConceptProperties via `conceptProperty`
- Derived Items use `origin.type: "Derived"` with `sourceItems` to show provenance

**Note**: The `_reifiedConcepts` field is a custom addition for demonstration. In the actual schema, `MetaDataVersion.concepts` stores only string OID references. The full ReifiedConcept objects would typically be stored separately or referenced externally.

**Usage**:
```python
from define_json.utils.ir import load_mdv
from pathlib import Path

mdv = load_mdv(Path('examples/concept_method_example.json'))
print(f"Concepts: {mdv.concepts}")
print(f"Methods: {len(mdv.methods or [])}")
print(f"Derived items: {[it.name for it in (mdv.items or []) if it.method]}")
```

## Dataset-JSON Examples (for Reverse Engineering)

### `sample_dataset_lb.json`
**Purpose**: Laboratory test results in Dataset-JSON format

**Use Case**: Input for reverse engineering tool
```bash
python scripts/reverse_engineer_define.py examples/sample_dataset_lb.json
```

### `sample_dataset_vs.json`
**Purpose**: Vital signs measurements in Dataset-JSON format

**Use Case**: Input for reverse engineering tool
```bash
python scripts/reverse_engineer_define.py examples/sample_dataset_vs.json
```

## Data Files (for Data Cube Pipeline)

### `laboratory_data.csv` / `laboratory_data.yaml`
**Purpose**: Raw SDTM laboratory data

**Use Case**: Input for dataset deconstructor and data cube pipeline

### `vital_signs_data.csv` / `vital_signs_data.yaml`
**Purpose**: Raw SDTM vital signs data

**Use Case**: Input for dataset deconstructor and data cube pipeline

### `sdtm_sample_data.yaml`
**Purpose**: Combined SDTM sample data (DM + VS domains)

**Use Case**: Comprehensive data cube demonstration

## Full Examples

For complete, real-world Define-JSON examples, see the `data/` directory:
- `data/defineV21-SDTM.json` - Full SDTM Define-JSON
- `data/defineV21-ADaM.json` - Full ADaM Define-JSON
- `data/define-360i.json` - 360i Define-JSON example

