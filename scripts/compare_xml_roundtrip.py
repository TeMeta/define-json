"""
Roundtrip Testing and Validation Script

Tests the XML → JSON → XML roundtrip for complete fidelity.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict
import sys


class RoundtripValidator:
    """Validates XML roundtrip fidelity."""
    
    def __init__(self):
        self.differences = []
        self.stats_original = {}
        self.stats_roundtrip = {}
    
    def validate_files(self, original_path: Path, roundtrip_path: Path) -> Dict:
        """
        Validate that original and roundtrip XML are semantically equivalent.
        
        Returns a report dictionary with statistics and differences.
        """
        print(f"\nValidating roundtrip:")
        print(f"  Original: {original_path}")
        print(f"  Roundtrip: {roundtrip_path}")
        
        # Parse both files
        orig_tree = ET.parse(original_path)
        rt_tree = ET.parse(roundtrip_path)
        
        orig_root = orig_tree.getroot()
        rt_root = rt_tree.getroot()
        
        # Collect statistics
        self.stats_original = self._collect_stats(orig_root)
        self.stats_roundtrip = self._collect_stats(rt_root)
        
        # Compare structures
        self._compare_elements(orig_root, rt_root, "ODM")
        
        # Generate report
        report = {
            'original_file': str(original_path),
            'roundtrip_file': str(roundtrip_path),
            'original_size': original_path.stat().st_size,
            'roundtrip_size': roundtrip_path.stat().st_size,
            'size_diff': roundtrip_path.stat().st_size - original_path.stat().st_size,
            'stats_original': self.stats_original,
            'stats_roundtrip': self.stats_roundtrip,
            'differences': self.differences,
            'difference_count': len(self.differences),
            'is_valid': len(self.differences) == 0
        }
        
        return report
    
    def _collect_stats(self, root: ET.Element) -> Dict:
        """Collect statistics about an XML document."""
        stats = {
            'elements': Counter(),
            'attributes': Counter(),
            'total_elements': 0,
            'total_attributes': 0,
            'total_text_nodes': 0,
            'namespaces': set()
        }
        
        for elem in root.iter():
            # Count element type
            tag = self._clean_tag(elem.tag)
            stats['elements'][tag] += 1
            stats['total_elements'] += 1
            
            # Collect namespace
            if elem.tag.startswith('{'):
                ns_end = elem.tag.find('}')
                ns = elem.tag[1:ns_end]
                stats['namespaces'].add(ns)
            
            # Count attributes
            for attr_name in elem.attrib.keys():
                attr_tag = self._clean_tag(attr_name)
                stats['attributes'][attr_tag] += 1
                stats['total_attributes'] += 1
            
            # Count text nodes
            if elem.text and elem.text.strip():
                stats['total_text_nodes'] += 1
        
        return stats
    
    def _clean_tag(self, tag: str) -> str:
        """Remove namespace from tag for comparison."""
        if tag.startswith('{'):
            return tag[tag.find('}')+1:]
        return tag
    
    def _compare_elements(self, orig: ET.Element, rt: ET.Element, path: str):
        """Recursively compare two elements."""
        # Compare attributes
        self._compare_attributes(orig, rt, path)
        
        # Compare text content
        self._compare_text(orig, rt, path)
        
        # Compare children
        self._compare_children(orig, rt, path)
    
    def _compare_attributes(self, orig: ET.Element, rt: ET.Element, path: str):
        """Compare attributes between two elements."""
        orig_attrs = {}
        rt_attrs = {}
        
        # Normalize attributes (remove namespaces for comparison)
        for key, value in orig.attrib.items():
            clean_key = self._clean_tag(key)
            # Store with namespace info for accurate reporting
            orig_attrs[key] = value
        
        for key, value in rt.attrib.items():
            clean_key = self._clean_tag(key)
            rt_attrs[key] = value
        
        # Find missing and different attributes
        for key, value in orig_attrs.items():
            if key not in rt_attrs:
                # Check if it exists under a different namespace
                clean_key = self._clean_tag(key)
                found = False
                for rt_key in rt_attrs.keys():
                    if self._clean_tag(rt_key) == clean_key:
                        # Same attribute, different namespace
                        if rt_attrs[rt_key] != value:
                            self.differences.append({
                                'type': 'DIFFERENT_ATTRIBUTE_VALUE',
                                'path': path,
                                'attribute': clean_key,
                                'original': value,
                                'roundtrip': rt_attrs[rt_key],
                                'original_namespace': key,
                                'roundtrip_namespace': rt_key
                            })
                        found = True
                        break
                
                if not found:
                    self.differences.append({
                        'type': 'MISSING_ATTRIBUTE',
                        'path': path,
                        'attribute': key,
                        'value': value
                    })
            elif orig_attrs[key] != rt_attrs[key]:
                self.differences.append({
                    'type': 'DIFFERENT_ATTRIBUTE_VALUE',
                    'path': path,
                    'attribute': key,
                    'original': orig_attrs[key],
                    'roundtrip': rt_attrs[key]
                })
        
        # Find extra attributes in roundtrip
        for key, value in rt_attrs.items():
            if key not in orig_attrs:
                # Check if it exists under a different namespace
                clean_key = self._clean_tag(key)
                found = False
                for orig_key in orig_attrs.keys():
                    if self._clean_tag(orig_key) == clean_key:
                        found = True
                        break
                
                if not found:
                    self.differences.append({
                        'type': 'EXTRA_ATTRIBUTE',
                        'path': path,
                        'attribute': key,
                        'value': value
                    })
    
    def _compare_text(self, orig: ET.Element, rt: ET.Element, path: str):
        """Compare text content."""
        orig_text = (orig.text or '').strip()
        rt_text = (rt.text or '').strip()
        
        if orig_text != rt_text:
            self.differences.append({
                'type': 'DIFFERENT_TEXT',
                'path': path,
                'original': orig_text[:100],  # Truncate for readability
                'roundtrip': rt_text[:100]
            })
    
    def _compare_children(self, orig: ET.Element, rt: ET.Element, path: str):
        """Compare child elements."""
        # Group children by tag
        orig_children = defaultdict(list)
        rt_children = defaultdict(list)
        
        for child in orig:
            tag = self._clean_tag(child.tag)
            orig_children[tag].append(child)
        
        for child in rt:
            tag = self._clean_tag(child.tag)
            rt_children[tag].append(child)
        
        # Compare counts
        all_tags = set(orig_children.keys()) | set(rt_children.keys())
        
        for tag in all_tags:
            orig_count = len(orig_children[tag])
            rt_count = len(rt_children[tag])
            
            if orig_count != rt_count:
                self.differences.append({
                    'type': 'DIFFERENT_ELEMENT_COUNT',
                    'path': f"{path}/{tag}",
                    'original_count': orig_count,
                    'roundtrip_count': rt_count
                })
            
            # Recursively compare matching children
            for i in range(min(orig_count, rt_count)):
                orig_child = orig_children[tag][i]
                rt_child = rt_children[tag][i]
                self._compare_elements(orig_child, rt_child, f"{path}/{tag}[{i}]")
    
    def print_report(self, report: Dict):
        """Print a human-readable validation report."""
        print("\n" + "="*80)
        print("ROUNDTRIP VALIDATION REPORT")
        print("="*80)
        
        print(f"\nFile Sizes:")
        print(f"  Original:  {report['original_size']:,} bytes")
        print(f"  Roundtrip: {report['roundtrip_size']:,} bytes")
        print(f"  Difference: {report['size_diff']:+,} bytes ({report['size_diff']/report['original_size']*100:+.1f}%)")
        
        print(f"\nElement Statistics:")
        print(f"  Original:  {report['stats_original']['total_elements']:,} elements")
        print(f"  Roundtrip: {report['stats_roundtrip']['total_elements']:,} elements")
        print(f"  Difference: {report['stats_roundtrip']['total_elements'] - report['stats_original']['total_elements']:+,}")
        
        print(f"\nAttribute Statistics:")
        print(f"  Original:  {report['stats_original']['total_attributes']:,} attributes")
        print(f"  Roundtrip: {report['stats_roundtrip']['total_attributes']:,} attributes")
        print(f"  Difference: {report['stats_roundtrip']['total_attributes'] - report['stats_original']['total_attributes']:+,}")
        
        print(f"\nText Node Statistics:")
        print(f"  Original:  {report['stats_original']['total_text_nodes']:,} text nodes")
        print(f"  Roundtrip: {report['stats_roundtrip']['total_text_nodes']:,} text nodes")
        print(f"  Difference: {report['stats_roundtrip']['total_text_nodes'] - report['stats_original']['total_text_nodes']:+,}")
        
        print(f"\nDifferences Found: {report['difference_count']}")
        
        if report['difference_count'] > 0:
            print("\nFirst 50 Differences:")
            for i, diff in enumerate(report['differences'][:50], 1):
                print(f"\n{i}. {diff['type']}: {diff['path']}")
                if diff['type'] == 'MISSING_ATTRIBUTE':
                    print(f"   Missing: {diff['attribute']} = {diff['value']}")
                elif diff['type'] == 'EXTRA_ATTRIBUTE':
                    print(f"   Extra: {diff['attribute']} = {diff['value']}")
                elif diff['type'] == 'DIFFERENT_ATTRIBUTE_VALUE':
                    print(f"   Attribute: {diff['attribute']}")
                    print(f"   Original: {diff.get('original', 'N/A')}")
                    print(f"   Roundtrip: {diff.get('roundtrip', 'N/A')}")
                elif diff['type'] == 'DIFFERENT_ELEMENT_COUNT':
                    print(f"   Original: {diff['original_count']} elements")
                    print(f"   Roundtrip: {diff['roundtrip_count']} elements")
        
        print("\n" + "="*80)
        if report['is_valid']:
            print("✓ VALIDATION PASSED - No differences found")
        else:
            print(f"✗ VALIDATION FAILED - {report['difference_count']} differences found")
        print("="*80)
        
        return report['is_valid']


def test_roundtrip(original_xml: Path, json_output: Path, roundtrip_xml: Path):
    """Test the complete roundtrip process."""
    from xml_to_json import DefineXMLToJSONConverter
    from json_to_xml import DefineJSONToXMLConverter
    
    print("\n" + "="*80)
    print("DEFINE-XML ROUNDTRIP TEST")
    print("="*80)
    
    # Step 1: XML → JSON
    print("\nStep 1: Converting XML to JSON...")
    xml_converter = DefineXMLToJSONConverter()
    try:
        json_data = xml_converter.convert_file(original_xml, json_output)
        print(f"✓ XML → JSON conversion complete")
        print(f"  Output: {json_output}")
    except Exception as e:
        print(f"✗ XML → JSON conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: JSON → XML
    print("\nStep 2: Converting JSON back to XML...")
    json_converter = DefineJSONToXMLConverter()
    try:
        xml_root = json_converter.convert_file(json_output, roundtrip_xml)
        print(f"✓ JSON → XML conversion complete")
        print(f"  Output: {roundtrip_xml}")
    except Exception as e:
        print(f"✗ JSON → XML conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Validate
    print("\nStep 3: Validating roundtrip...")
    validator = RoundtripValidator()
    report = validator.validate_files(original_xml, roundtrip_xml)
    is_valid = validator.print_report(report)
    
    return is_valid


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Test roundtrip:  python test_roundtrip.py <original.xml>")
        print("  Validate only:   python test_roundtrip.py <original.xml> <roundtrip.xml> --validate-only")
        sys.exit(1)
    
    original_xml = Path(sys.argv[1])
    
    if not original_xml.exists():
        print(f"Error: File not found: {original_xml}")
        sys.exit(1)
    
    if len(sys.argv) >= 3 and '--validate-only' in sys.argv:
        # Validation only mode
        roundtrip_xml = Path(sys.argv[2])
        validator = RoundtripValidator()
        report = validator.validate_files(original_xml, roundtrip_xml)
        is_valid = validator.print_report(report)
        sys.exit(0 if is_valid else 1)
    else:
        # Full roundtrip test
        json_output = original_xml.parent / f"{original_xml.stem}_converted.json"
        roundtrip_xml = original_xml.parent / f"{original_xml.stem}_roundtrip.xml"
        
        success = test_roundtrip(original_xml, json_output, roundtrip_xml)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
