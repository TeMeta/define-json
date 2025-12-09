# Define-JSON Tests

Comprehensive test suite for Define-JSON schema validation and datacube functionality.

## Running Tests

```bash
# Run schema tests only
python -m unittest tests.test_schema

# Run datacube tests only  
python -m unittest tests.test_datacube

# Run all tests with linting
make test
```

## Test Coverage

### Schema Tests (`test_schema.py`)
- **`test_schema_loads`** - Schema file loads and has expected structure
- **`test_mixin_consistency`** - Mixins referenced in classes actually exist
- **`test_linkml_schema_loading`** - LinkML can load the schema (requires LinkML)

### Conversion Tests (`test_conversion.py`)
- **`test_xml_to_json_conversion`** - XML → JSON conversion with structure validation
- **`test_json_to_xml_conversion`** - JSON → XML conversion with XML structure validation
- **`test_roundtrip_validation`** - Complete XML → JSON → XML roundtrip validation
- **`test_xml_to_json_validation`** - XML → JSON semantic equivalence validation
- **`test_reference_based_structure`** - Reference-based ItemGroup slices validation
- **`test_schema_compliance`** - Generated JSON schema compliance validation
- **`test_clinical_data_preservation`** - Clinical metadata preservation validation

### DataCube Tests (`test_datacube.py`)
- **`test_vital_signs_datacube_transformation`** - Complete vital signs SDTM→datacube transformation
- **`test_laboratory_datacube_transformation`** - Complete laboratory SDTM→datacube transformation
- **`test_schema_item_component_relationship`** - Validates Item-Component relationships
- **`test_clinical_data_quality_assessment`** - Clinical data quality analysis

## Visual Outputs

DataCube tests generate clinical visualizations in `test_outputs/`:
- `vital_signs_analysis.png` - Blood pressure analysis by sex, age distribution, test frequency
- `laboratory_analysis.png` - Lab values by test, age correlation, result distribution
- `data_quality_dashboard.png` - Data completeness, validity, missing data analysis

## Clinical Features

- **Hypertension Detection** - Flags readings ≥140/90 mmHg
- **Reference Range Analysis** - Identifies out-of-range lab values
- **Demographic Analysis** - Age, sex, race distribution
- **Data Quality Metrics** - Completeness and validity scoring

## Notes

- LinkML tests are skipped if LinkML not installed
- DataCube tests require matplotlib and seaborn
- All tests demonstrate real clinical scenarios with SDTM data 