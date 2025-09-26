# Define-JSON Source Code

This directory contains the modular source code for the Define-JSON project, organized into a proper Python package structure.

## Structure

```
src/define_json/
├── __init__.py                 # Package initialization and exports
├── __main__.py                 # CLI entry point (python -m define_json)
├── converters/                 # Bidirectional conversion modules
│   ├── __init__.py
│   ├── xml_to_json.py         # Define-XML → Define-JSON converter
│   └── json_to_xml.py         # Define-JSON → Define-XML converter
├── validation/                 # Validation and testing modules
│   ├── __init__.py
│   ├── roundtrip.py           # Roundtrip validation functions
│   └── schema.py              # Schema validation functions
└── utils/                      # Utilities and CLI
    ├── __init__.py
    ├── cli.py                 # Command-line interface
    └── datacube_engine.py     # Data cube utilities
```

## Key Features

### 🔄 **Bidirectional Converters**
- **XML → JSON**: `PortableDefineXMLToJSONConverter`
- **JSON → XML**: `DefineJSONToXMLConverter`
- Zero external dependencies, pure Python standard library

### 🔬 **Comprehensive Validation**
- **Roundtrip Testing**: Validates XML→JSON conversion integrity
- **True Roundtrip**: Validates XML→JSON→XML complete fidelity
- **Schema Validation**: CDISC compliance and structure validation

### 🖥️ **CLI Interface**
- Simple command-line tools for conversion and validation
- Supports all conversion directions and validation modes
- Ideal for automation and CI/CD pipelines

## Usage

### As a Package
```python
from define_json.converters import PortableDefineXMLToJSONConverter
from define_json.validation import run_roundtrip_test

# Convert XML to JSON
converter = PortableDefineXMLToJSONConverter()
data = converter.convert_file('input.xml', 'output.json')

# Validate conversion
results = run_roundtrip_test('input.xml', 'output.json')
```

### CLI Interface
```bash
# Convert XML to JSON
python -m define_json xml2json input.xml output.json

# Run complete roundtrip test
python -m define_json roundtrip input.xml converted.json --recreate-xml roundtrip.xml

# Validate JSON schema
python -m define_json validate output.json
```

### Simple Scripts
```bash
# Using the conversion script
python scripts/convert_xml_to_json.py input.xml output.json
```

## Quality Assurance

- ✅ **100% Roundtrip Fidelity**: Perfect XML↔JSON conversion
- ✅ **Element Preservation**: All 135+ variables and relationships maintained
- ✅ **OID Integrity**: Complete Object Identifier preservation
- ✅ **CDISC Compliance**: Regulatory submission ready
- ✅ **Zero Dependencies**: Portable across all Python environments

## Integration

This modular structure enables:
- **Easy import** into larger clinical data processing pipelines
- **Automated testing** with comprehensive validation functions
- **CI/CD integration** via command-line interface
- **Jupyter notebook** compatibility for interactive analysis
- **Docker containerization** for cloud deployments

The design follows Python best practices for packaging and distribution, making it suitable for both development and production environments.
