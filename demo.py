#!/usr/bin/env python3
"""
Define-JSON Demo: Complete XML ↔ JSON conversion pipeline

Demonstrates the modular define_json package functionality.
"""

import sys
from pathlib import Path

# Add src to path for development
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from define_json.converters import PortableDefineXMLToJSONConverter, DefineJSONToXMLConverter
from define_json.validation import run_roundtrip_test, validate_true_roundtrip, validate_define_json


def main():
    """Run the complete Define-JSON demo."""
    print("🚀 Define-JSON Complete Demo")
    print("=" * 60)
    
    # Define paths
    data_dir = Path(__file__).parent / 'data'
    xml_path = data_dir / 'define-360i.xml'
    json_path = data_dir / 'define-360i-demo.json'
    roundtrip_xml_path = data_dir / 'define-360i-demo-roundtrip.xml'
    
    if not xml_path.exists():
        print(f"❌ Error: {xml_path} not found")
        return 1
    
    print(f"📁 Input XML: {xml_path.name}")
    print(f"📁 Output JSON: {json_path.name}")
    print(f"📁 Roundtrip XML: {roundtrip_xml_path.name}")
    
    try:
        # Step 1: XML → JSON Conversion
        print(f"\n🔄 Step 1: Converting XML → JSON...")
        converter = PortableDefineXMLToJSONConverter()
        data = converter.convert_file(xml_path, json_path)
        
        print(f"✅ Converted: {xml_path.name} → {json_path.name}")
        
        # Extract from metadata section
        metadata = data.get('metadata', {})
        print(f"📊 Study: {metadata.get('studyName')} ({metadata.get('studyOID')})")
        print(f"📊 Datasets: {len(data.get('Datasets', []))}")
        print(f"📊 Variables: {len(data.get('Variables', []))}")
        print(f"📊 Standards: {len(data.get('Standards', []))}")
        print(f"📊 AnnotatedCRF: {len(data.get('AnnotatedCRF', []))}")
        
        # Step 2: Validate XML → JSON
        print(f"\n🔄 Step 2: Validating XML → JSON conversion...")
        validation_results = run_roundtrip_test(xml_path, json_path)
        
        if validation_results['passed']:
            print("✅ XML → JSON validation: PASSED")
        else:
            print("❌ XML → JSON validation: FAILED")
            for error in validation_results['errors']:
                print(f"   • {error}")
        
        # Step 3: Schema Validation
        print(f"\n🔄 Step 3: Validating JSON schema...")
        schema_results = validate_define_json(data)
        
        if schema_results['valid']:
            print("✅ Schema validation: PASSED")
        else:
            print("❌ Schema validation: FAILED")
            for error in schema_results['errors']:
                print(f"   • {error}")
        
        # Step 4: JSON → XML Conversion
        print(f"\n🔄 Step 4: Converting JSON → XML...")
        json_to_xml_converter = DefineJSONToXMLConverter()
        json_to_xml_converter.convert_file(json_path, roundtrip_xml_path)
        
        print(f"✅ Converted: {json_path.name} → {roundtrip_xml_path.name}")
        print(f"📁 Size: {roundtrip_xml_path.stat().st_size:,} bytes")
        
        # Step 5: True Roundtrip Validation
        print(f"\n🔄 Step 5: Validating complete roundtrip...")
        roundtrip_results = validate_true_roundtrip(xml_path, roundtrip_xml_path)
        
        if roundtrip_results['passed']:
            print("🏆 TRUE ROUNDTRIP: PASSED")
            print("🎯 Perfect bidirectional conversion achieved!")
            print("   XML → JSON → XML maintains 100% semantic fidelity")
        else:
            print("❌ TRUE ROUNDTRIP: FAILED")
            for error in roundtrip_results['errors']:
                print(f"   • {error}")
        
        # Summary Statistics
        print(f"\n📊 FINAL STATISTICS:")
        print("-" * 40)
        orig_stats = roundtrip_results['stats']['original']
        round_stats = roundtrip_results['stats']['roundtrip']
        
        for element_type in orig_stats:
            orig_count = orig_stats[element_type]
            round_count = round_stats[element_type]
            status = "✅" if orig_count == round_count else "❌"
            print(f"   {status} {element_type:15s}: {orig_count:3d} → {round_count:3d}")
        
        print(f"\n" + "=" * 60)
        if validation_results['passed'] and schema_results['valid'] and roundtrip_results['passed']:
            print("🎉 PERFECT CONVERSION: All tests passed!")
            print("🚀 Ready for production clinical data processing")
        else:
            print("⚠️  Some validation issues detected")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
