# Portable Define-XML to Define-JSON Converter

## Features

✅ **Completely Self-Contained** - No external dependencies  
✅ **Portable** - Runs anywhere with Python + Jupyter  
✅ **Zero Setup** - Just open and run  
✅ **Standard Library Only** - Uses only built-in Python modules  

## Usage

1. Place your Define-XML file as `define-360i.xml`
2. Open `define_xml_to_json_converter.ipynb`
3. Run all cells
4. Output: `define-360i.json`

## What It Does

- **Conversion**: Define-XML → Define-JSON with full structure preservation
- **Content Analysis**: Counts datasets, variables, ValueLists, CodeLists, WhereClauses
- **ItemRef Tracking**: Critical for roundtrip validation
- **Basic Validation**: CDISC OID pattern checking and structure validation

## Requirements

- Python 3.7+
- Jupyter Notebook
- **No external packages needed!**

## Output Structure

```json
{
  "studyOID": "ODM.LZZT",
  "studyName": "LZZT", 
  "Datasets": [...],
  "Variables": [...],
  "ValueLists": [...],
  "CodeLists": [...],
  "WhereClauses": [...],
  "Methods": [...]
}
```

## Portability

This notebook is completely portable - copy it anywhere and it will work as long as you have:
- Python with standard library
- Jupyter notebook support
- Your Define-XML file

No path dependencies, no external libraries, no setup required!
