#!/usr/bin/env python3
"""
CLI tool for validating Define-JSON schema.
"""

import click
import yaml
import json
from pathlib import Path
from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.progress import track

try:
    from linkml_runtime import SchemaView
    LINKML_AVAILABLE = True
except ImportError:
    LINKML_AVAILABLE = False

console = Console()

@click.command()
@click.option('--schema', default='define-json.yaml', help='Path to schema file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--format', 'output_format', default='text', 
              type=click.Choice(['text', 'json', 'yaml']), help='Output format')
def validate_schema(schema: str, verbose: bool, output_format: str):
    """Validate Define-JSON schema for fit-for-purpose testing."""
    
    schema_path = Path(schema)
    if not schema_path.exists():
        console.print(f"[red]Error: Schema file {schema} not found[/red]")
        return 1
    
    console.print(f"[bold blue]Validating Define-JSON Schema: {schema}[/bold blue]")
    
    # Load schema
    try:
        with open(schema_path, 'r') as f:
            schema_data = yaml.safe_load(f)
        console.print("[green]✓ Schema loaded successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to load schema: {e}[/red]")
        return 1
    
    # Validation results
    results = {
        'basic_validation': {},
        'structure_validation': {},
        'quality_validation': {},
        'compatibility_validation': {},
        'linkml_validation': {}
    }
    
    # Basic validation
    console.print("\n[bold]1. Basic Validation[/bold]")
    required_sections = ['id', 'name', 'description', 'prefixes', 'classes', 'enums']
    missing_sections = []
    
    for section in required_sections:
        if section in schema_data:
            console.print(f"  [green]✓ {section}[/green]")
            results['basic_validation'][section] = True
        else:
            console.print(f"  [red]✗ {section} (missing)[/red]")
            results['basic_validation'][section] = False
            missing_sections.append(section)
    
    # Structure validation
    console.print("\n[bold]2. Structure Validation[/bold]")
    classes = schema_data.get('classes', {})
    enums = schema_data.get('enums', {})
    
    console.print(f"  Classes: {len(classes)}")
    console.print(f"  Enums: {len(enums)}")
    
    results['structure_validation'] = {
        'class_count': len(classes),
        'enum_count': len(enums),
        'has_classes': len(classes) > 0,
        'has_enums': len(enums) > 0
    }
    
    # Quality validation
    console.print("\n[bold]3. Quality Validation[/bold]")
    classes_with_desc = 0
    aristotelian_pattern = 0
    ends_with_period = 0
    
    for class_name, class_def in classes.items():
        description = class_def.get('description', '')
        if description:
            classes_with_desc += 1
            
            if isinstance(description, str):
                if description.startswith('A ') or description.startswith('An '):
                    aristotelian_pattern += 1
                if description.endswith('.'):
                    ends_with_period += 1
    
    console.print(f"  Classes with descriptions: {classes_with_desc}/{len(classes)} ({classes_with_desc/len(classes)*100:.1f}%)")
    console.print(f"  Ends with period: {ends_with_period}/{len(classes)} ({ends_with_period/len(classes)*100:.1f}%)")
    
    results['quality_validation'] = {
        'description_coverage': classes_with_desc / len(classes) * 100 if classes else 0,
        'period_issues': ends_with_period
    }
    
    # Compatibility validation
    console.print("\n[bold]4. Standards Compatibility[/bold]")
    
    standard_classes = {
        'CDISC': ['Item', 'ItemGroup', 'CodeList', 'MetaDataVersion'],
        'FHIR': ['Resource', 'DocumentReference', 'Coding'],
        'SDMX': ['Dataset', 'Dataflow', 'DataStructureDefinition']
    }
    
    compatibility_results = {}
    for standard, expected_classes in standard_classes.items():
        found = [cls for cls in expected_classes if cls in classes]
        coverage = len(found) / len(expected_classes) * 100
        console.print(f"  {standard}: {len(found)}/{len(expected_classes)} ({coverage:.1f}%)")
        compatibility_results[standard] = {
            'found': found,
            'missing': [cls for cls in expected_classes if cls not in classes],
            'coverage': coverage
        }
    
    results['compatibility_validation'] = compatibility_results
    
    # LinkML validation
    console.print("\n[bold]5. LinkML Integration[/bold]")
    if LINKML_AVAILABLE:
        try:
            sv = SchemaView(str(schema_path))
            all_classes = sv.all_classes()
            all_enums = sv.all_enums()
            console.print(f"  [green]✓ LinkML integration successful[/green]")
            console.print(f"  Classes accessible: {len(all_classes)}")
            console.print(f"  Enums accessible: {len(all_enums)}")
            results['linkml_validation'] = {
                'success': True,
                'class_count': len(all_classes),
                'enum_count': len(all_enums)
            }
        except Exception as e:
            console.print(f"  [red]✗ LinkML integration failed: {e}[/red]")
            results['linkml_validation'] = {'success': False, 'error': str(e)}
    else:
        console.print("  [yellow]⚠ LinkML not available[/yellow]")
        results['linkml_validation'] = {'success': False, 'error': 'LinkML not installed'}
    
    # Summary
    console.print("\n[bold]Summary[/bold]")
    
    # Calculate overall score
    basic_score = sum(results['basic_validation'].values()) / len(results['basic_validation']) * 100
    structure_score = 100 if results['structure_validation']['has_classes'] else 0
    quality_score = results['quality_validation']['description_coverage']
    compatibility_score = sum(r['coverage'] for r in compatibility_results.values()) / len(compatibility_results)
    linkml_score = 100 if results['linkml_validation'].get('success', False) else 0
    
    overall_score = (basic_score + structure_score + quality_score + compatibility_score + linkml_score) / 5
    
    console.print(f"  Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 80:
        console.print("  [green]✓ Schema is fit for purpose[/green]")
    elif overall_score >= 60:
        console.print("  [yellow]⚠ Schema needs improvements[/yellow]")
    else:
        console.print("  [red]✗ Schema needs significant work[/red]")
    
    # Output results
    if output_format == 'json':
        console.print(json.dumps(results, indent=2))
    elif output_format == 'yaml':
        console.print(yaml.dump(results, default_flow_style=False))
    
    return 0 if overall_score >= 60 else 1

if __name__ == '__main__':
    validate_schema() 