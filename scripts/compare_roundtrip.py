#!/usr/bin/env python3
"""
Compare original JSON with roundtrip JSON to identify data loss during conversion.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from collections import defaultdict


def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON file and return parsed data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def compare_structures(original: Dict[str, Any], roundtrip: Dict[str, Any], path: str = "") -> List[str]:
    """Recursively compare two JSON structures and return differences."""
    differences = []
    
    # Check for missing keys in roundtrip
    for key, value in original.items():
        current_path = f"{path}.{key}" if path else key
        
        if key not in roundtrip:
            differences.append(f"MISSING KEY: {current_path} (value: {value})")
        elif isinstance(value, dict) and isinstance(roundtrip[key], dict):
            differences.extend(compare_structures(value, roundtrip[key], current_path))
        elif isinstance(value, list) and isinstance(roundtrip[key], list):
            differences.extend(compare_lists(value, roundtrip[key], current_path))
        elif value != roundtrip[key]:
            differences.append(f"VALUE DIFFERENCE: {current_path} - Original: {value}, Roundtrip: {roundtrip[key]}")
    
    # Check for extra keys in roundtrip
    for key in roundtrip:
        if key not in original:
            current_path = f"{path}.{key}" if path else key
            differences.append(f"EXTRA KEY: {current_path} (value: {roundtrip[key]})")
    
    return differences


def compare_lists(original: List[Any], roundtrip: List[Any], path: str) -> List[str]:
    """Compare two lists and return differences."""
    differences = []
    
    if len(original) != len(roundtrip):
        differences.append(f"LIST LENGTH DIFFERENCE: {path} - Original: {len(original)}, Roundtrip: {len(roundtrip)}")
    
    # Compare each item
    for i, (orig_item, roundtrip_item) in enumerate(zip(original, roundtrip)):
        current_path = f"{path}[{i}]"
        
        if isinstance(orig_item, dict) and isinstance(roundtrip_item, dict):
            differences.extend(compare_structures(orig_item, roundtrip_item, current_path))
        elif isinstance(orig_item, list) and isinstance(roundtrip_item, list):
            differences.extend(compare_lists(orig_item, roundtrip_item, current_path))
        elif orig_item != roundtrip_item:
            differences.append(f"LIST ITEM DIFFERENCE: {current_path} - Original: {orig_item}, Roundtrip: {roundtrip_item}")
    
    return differences


def analyze_data_loss(differences: List[str]) -> Dict[str, List[str]]:
    """Categorise differences by type of data loss."""
    categories = {
        "missing_keys": [],
        "missing_values": [],
        "value_changes": [],
        "extra_keys": [],
        "list_length_changes": [],
        "other": []
    }
    
    for diff in differences:
        if "MISSING KEY" in diff:
            categories["missing_keys"].append(diff)
        elif "VALUE DIFFERENCE" in diff:
            categories["value_changes"].append(diff)
        elif "EXTRA KEY" in diff:
            categories["extra_keys"].append(diff)
        elif "LIST LENGTH DIFFERENCE" in diff:
            categories["list_length_changes"].append(diff)
        else:
            categories["other"].append(diff)
    
    return categories


def get_file_stats(file_path: str) -> Dict[str, Any]:
    """Get basic statistics about a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    def count_items(obj, path=""):
        """Recursively count items in the JSON structure."""
        if isinstance(obj, dict):
            return sum(count_items(v, f"{path}.{k}" if path else k) for k, v in obj.items())
        elif isinstance(obj, list):
            return sum(count_items(item, f"{path}[{i}]") for i, item in enumerate(obj))
        else:
            return 1
    
    return {
        "file_size": Path(file_path).stat().st_size,
        "total_items": count_items(data),
        "structure": data
    }


def main():
    """Main comparison function."""
    if len(sys.argv) != 3:
        print("Usage: python compare_roundtrip.py <original.json> <roundtrip.json>")
        sys.exit(1)
    
    original_file = sys.argv[1]
    roundtrip_file = sys.argv[2]
    
    print("=" * 80)
    print("DEFINE-JSON ROUNDTRIP COMPARISON ANALYSIS")
    print("=" * 80)
    print()
    
    # Load files
    print("Loading files...")
    original = load_json(original_file)
    roundtrip = load_json(roundtrip_file)
    
    # Get file statistics
    print("Analysing file statistics...")
    orig_stats = get_file_stats(original_file)
    roundtrip_stats = get_file_stats(roundtrip_file)
    
    print(f"Original file: {orig_stats['file_size']:,} bytes, {orig_stats['total_items']:,} items")
    print(f"Roundtrip file: {roundtrip_stats['file_size']:,} bytes, {roundtrip_stats['total_items']:,} items")
    print(f"Size difference: {roundtrip_stats['file_size'] - orig_stats['file_size']:,} bytes")
    print(f"Item difference: {roundtrip_stats['total_items'] - orig_stats['total_items']:,} items")
    print()
    
    # Compare structures
    print("Comparing structures...")
    differences = compare_structures(original, roundtrip)
    
    print(f"Total differences found: {len(differences)}")
    print()
    
    # Categorise differences
    categories = analyze_data_loss(differences)
    
    # Report findings
    print("=" * 80)
    print("DATA LOSS ANALYSIS")
    print("=" * 80)
    
    for category, items in categories.items():
        if items:
            print(f"\n{category.upper().replace('_', ' ')} ({len(items)} items):")
            print("-" * 50)
            for item in items[:20]:  # Show first 20 items
                print(f"  {item}")
            if len(items) > 20:
                print(f"  ... and {len(items) - 20} more items")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Missing keys: {len(categories['missing_keys'])}")
    print(f"Value changes: {len(categories['value_changes'])}")
    print(f"Extra keys: {len(categories['extra_keys'])}")
    print(f"List length changes: {len(categories['list_length_changes'])}")
    print(f"Other differences: {len(categories['other'])}")
    
    # Save detailed report
    report_file = "roundtrip_analysis_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("DEFINE-JSON ROUNDTRIP ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Original file: {original_file}\n")
        f.write(f"Roundtrip file: {roundtrip_file}\n")
        f.write(f"Original size: {orig_stats['file_size']:,} bytes\n")
        f.write(f"Roundtrip size: {roundtrip_stats['file_size']:,} bytes\n")
        f.write(f"Size difference: {roundtrip_stats['file_size'] - orig_stats['file_size']:,} bytes\n\n")
        
        f.write("ALL DIFFERENCES:\n")
        f.write("-" * 30 + "\n")
        for i, diff in enumerate(differences, 1):
            f.write(f"{i:4d}. {diff}\n")
    
    print(f"\nDetailed report saved to: {report_file}")


if __name__ == "__main__":
    main()
