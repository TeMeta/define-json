"""
Command-line interface for Define-JSON converters.

Provides a clean CLI for XML ↔ JSON conversion and validation.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..converters.xml_to_json import PortableDefineXMLToJSONConverter
from ..converters.json_to_xml import DefineJSONToXMLConverter
from ..validation.roundtrip import run_roundtrip_test, validate_true_roundtrip
from ..validation.schema import validate_define_json


def create_cli_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Define-JSON: Bidirectional XML ↔ JSON converter for clinical data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert XML to JSON
  define-json xml2json define.xml output.json
  
  # Convert JSON to XML  
  define-json json2xml define.json output.xml
  
  # Run roundtrip test
  define-json roundtrip define.xml define.json
  
  # Validate JSON schema
  define-json validate define.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # XML to JSON conversion
    xml2json_parser = subparsers.add_parser('xml2json', help='Convert Define-XML to Define-JSON')
    xml2json_parser.add_argument('input', type=Path, help='Input Define-XML file')
    xml2json_parser.add_argument('output', type=Path, help='Output Define-JSON file')
    
    # JSON to XML conversion
    json2xml_parser = subparsers.add_parser('json2xml', help='Convert Define-JSON to Define-XML')
    json2xml_parser.add_argument('input', type=Path, help='Input Define-JSON file')
    json2xml_parser.add_argument('output', type=Path, help='Output Define-XML file')
    
    # Roundtrip validation
    roundtrip_parser = subparsers.add_parser('roundtrip', help='Run complete roundtrip validation')
    roundtrip_parser.add_argument('xml_file', type=Path, help='Original Define-XML file')
    roundtrip_parser.add_argument('json_file', type=Path, help='Define-JSON file')
    roundtrip_parser.add_argument('--recreate-xml', type=Path, help='Path for recreated XML file')
    
    # Schema validation
    validate_parser = subparsers.add_parser('validate', help='Validate Define-JSON schema')
    validate_parser.add_argument('input', type=Path, help='Define-JSON file to validate')
    
    return parser


def cmd_xml2json(args) -> int:
    """Convert XML to JSON."""
    try:
        converter = PortableDefineXMLToJSONConverter()
        data = converter.convert_file(args.input, args.output)
        
        print(f"✅ Converted: {args.input} → {args.output}")
        print(f"📊 Datasets: {len(data.get('Datasets', []))}")
        print(f"📊 Variables: {len(data.get('Variables', []))}")
        print(f"📁 Size: {args.output.stat().st_size:,} bytes")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_json2xml(args) -> int:
    """Convert JSON to XML."""
    try:
        converter = DefineJSONToXMLConverter()
        root = converter.convert_file(args.input, args.output)
        
        print(f"✅ Converted: {args.input} → {args.output}")
        print(f"📁 Size: {args.output.stat().st_size:,} bytes")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_roundtrip(args) -> int:
    """Run roundtrip validation."""
    try:
        # Test XML → JSON
        print("🔄 Testing XML → JSON conversion...")
        results = run_roundtrip_test(args.xml_file, args.json_file)
        
        if results['passed']:
            print("✅ XML → JSON: PASSED")
        else:
            print("❌ XML → JSON: FAILED")
            for error in results['errors']:
                print(f"   • {error}")
        
        # Test JSON → XML if recreate path provided
        if args.recreate_xml:
            print("\n🔄 Testing JSON → XML conversion...")
            converter = DefineJSONToXMLConverter()
            converter.convert_file(args.json_file, args.recreate_xml)
            
            roundtrip_results = validate_true_roundtrip(args.xml_file, args.recreate_xml)
            
            if roundtrip_results['passed']:
                print("✅ JSON → XML: PASSED")
                print("🎉 PERFECT ROUNDTRIP: XML ↔ JSON conversion is LOSSLESS!")
            else:
                print("❌ JSON → XML: FAILED")
                for error in roundtrip_results['errors']:
                    print(f"   • {error}")
        
        return 0 if results['passed'] else 1
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_validate(args) -> int:
    """Validate Define-JSON schema."""
    try:
        import json
        
        with open(args.input, 'r') as f:
            data = json.load(f)
        
        results = validate_define_json(data)
        
        if results['valid']:
            print("✅ Validation: PASSED")
        else:
            print("❌ Validation: FAILED")
            for error in results['errors']:
                print(f"   Error: {error}")
        
        if results['warnings']:
            print(f"⚠️  Warnings: {len(results['warnings'])}")
            for warning in results['warnings'][:5]:  # Show first 5
                print(f"   Warning: {warning}")
        
        return 0 if results['valid'] else 1
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = create_cli_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Dispatch to command handlers
    if args.command == 'xml2json':
        return cmd_xml2json(args)
    elif args.command == 'json2xml':
        return cmd_json2xml(args)
    elif args.command == 'roundtrip':
        return cmd_roundtrip(args)
    elif args.command == 'validate':
        return cmd_validate(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
