# Cube Configuration Files

These YAML files define data cube structures using **SDMX conventions** for analyzing clinical trial data.

## Quick Start

```python
from define_json.utils.cube_config_converter import CubeConfigConverter

# Load and validate a cube config
items, components, dsd = CubeConfigConverter.validate_and_convert(
    'configs/laboratory_cube.yaml'
)

# Now you have validated schema objects
print(f"DSD: {dsd.name}")
print(f"Dimensions: {len(dsd.dimensions)}")
print(f"Measures: {len(dsd.measures)}")
```

## Available Configurations

### `laboratory_cube.yaml`
**Purpose**: Analyzing laboratory test results  
**Domains**: DM (Demographics) + LB (Laboratory)  
**Dimensions**: Subject, Age, Sex, Visit, Test Category  
**Measures**: Hemoglobin, WBC Count, Platelet Count  
**Use Cases**: 
- Hematology analysis by demographics
- Lab safety monitoring
- Test result trends over visits

### `vital_signs_cube.yaml`
**Purpose**: Analyzing vital signs measurements  
**Domains**: DM (Demographics) + VS (Vital Signs)  
**Dimensions**: Subject, Age, Sex, Visit  
**Measures**: Systolic BP, Diastolic BP  
**Use Cases**:
- Blood pressure analysis
- Vital signs trends
- Safety monitoring

## Structure

Each cube config follows this pattern:

```yaml
name: "Cube Name"
description: "What this cube analyzes"

# Data source
data_source:
  type: "sdtm"
  domains: ["DM", "LB"]

# Items: Reusable variable definitions
items:
  IT001:
    id: IT001
    name: "Subject ID"
    dataType: string
    length: 20
    # ... more fields

# Components: Items with structural roles
components:
  DIM001:
    id: DIM001
    name: "Subject Dimension"
    item: IT001
    role: dimension  # or measure, attribute
    
# Data Structure Definition: How components organize the cube
data_structure_definition:
  id: DSD001
  name: "Cube Structure"
  dimensions: [DIM001, DIM002]
  measures: [MEAS001]
  attributes: [ATTR001]

# Data mapping: How to map from SDTM to cube
data_mapping:
  DM:
    USUBJID: IT001  # DM.USUBJID → Item IT001
```

## Component Roles

- **Dimension**: Categorical/hierarchical properties (Subject, Visit, Test)
- **Measure**: Quantitative observations (Lab values, Blood pressure)
- **Attribute**: Contextual metadata (Race, Treatment Arm)

## Using with DataCubeEngine

```python
from define_json.utils.datacube_engine import DataCubeEngine

# Load config and data
engine = DataCubeEngine()
engine.load_config('configs/laboratory_cube.yaml')
engine.load_example_data('examples/laboratory_data.yaml')

# Build the cube
cube_df = engine.build_datacube()

# Analyze
summary = engine.get_analysis_summary()
print(f"Total observations: {summary['total_observations']}")
```

## Schema Validation

The converter automatically validates configs against the define-json schema:

```python
# This will raise ValidationError if config is invalid
items, components, dsd = CubeConfigConverter.validate_and_convert(
    'my_cube.yaml'
)
```

**Common validation errors:**
- Invalid `dataType` (must be: string, integer, float, date, etc.)
- Missing required fields (`id`, `name`)
- Invalid component `role` (must be: dimension, measure, attribute)
- Broken item references

## Documentation

- **Complete Demo**: `notebooks/datacube_end_to_end.ipynb` - Interactive end-to-end pipeline demonstration
- **Tests**: `tests/test_cube_converter.py` - Comprehensive test suite
- **CLI Example**: `src/dataset_deconstructor/example.py` - Command-line usage

## SDMX Background

These configs follow **SDMX (Statistical Data and Metadata eXchange)** conventions:

- **Items** ≈ SDMX Concepts (reusable variable definitions)
- **Components** ≈ SDMX Component Specifications (roles)
- **DSD** ≈ SDMX Data Structure Definition (cube organization)

See `SDMX_UNIFICATION_ANALYSIS.md` for architectural details.

