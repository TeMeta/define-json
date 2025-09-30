#!/usr/bin/env python3
"""
Simple script for XML to JSON conversion using the define_json package.

Example usage:
    python scripts/convert_xml_to_json.py define-360i.xml define-360i.json
"""

import sys
from pathlib import Path

# Add src to path for development
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from define_json.converters import DefineXMLToJSONConverter
from define_json.validation import run_roundtrip_test, validate_define_json


def main():
    """Main conversion function."""
    if len(sys.argv) != 3:
        print("Usage: python convert_xml_to_json.py <input.xml> <output.json>")
        sys.exit(1)
    
    xml_path = Path(sys.argv[1])
    json_path = Path(sys.argv[2])
    
    if not xml_path.exists():
        print(f"Error: Input file {xml_path} not found")
        sys.exit(1)
    
    print("🔄 Converting Define-XML to Define-JSON...")
    print("=" * 50)
    
    try:
        # Convert XML to JSON
        converter = DefineXMLToJSONConverter()
        data = converter.convert_file(xml_path, json_path)
        
        print(f"✅ Converted: {xml_path.name} → {json_path.name}")
        print(f"📁 Size: {json_path.stat().st_size:,} bytes")
        
        # Show summary
        datasets = data.get('Datasets', [])
        variables = data.get('Variables', [])
        print(f"\n📊 Study: {data.get('studyName')}")
        print(f"📊 Datasets: {len(datasets)}")
        print(f"📊 Variables: {len(variables)}")
        print(f"📊 ValueLists: {len(data.get('ValueLists', []))}")
        print(f"📊 CodeLists: {len(data.get('CodeLists', []))}")
        
        # Validate conversion
        print("\n🔄 Validating conversion...")
        roundtrip_results = run_roundtrip_test(xml_path, json_path)
        
        if roundtrip_results['passed']:
            print("✅ Validation: PASSED")
        else:
            print("❌ Validation: FAILED")
            for error in roundtrip_results['errors']:
                print(f"   • {error}")
        
        # Schema validation
        schema_results = validate_define_json(data)
        if schema_results['valid']:
            print("✅ Schema: VALID")
        else:
            print("❌ Schema: INVALID")
            for error in schema_results['errors']:
                print(f"   • {error}")
        
        print("\n✅ Conversion complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
