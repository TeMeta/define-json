#!/usr/bin/env python3
"""
CLI tool for validating Data Definition Specification schema.
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

# ---------------------------------------------------------------------------
# Cross-vocabulary mapping IRI validation
# ---------------------------------------------------------------------------
# Keys whose values are CURIEs pointing at terms in external vocabularies.
MAPPING_KEYS = {
    'exact_mappings', 'close_mappings', 'narrow_mappings',
    'broad_mappings', 'related_mappings', 'mappings',
}
# Single-CURIE keys that also reference external terms.
URI_KEYS = {'slot_uri', 'class_uri', 'subproperty_of', 'meaning'}

# Authoritative term sets for the closed, well-known vocabularies whose local
# names we can verify offline. A CURIE using one of these prefixes whose local
# name is absent here is reported as an error. Prefixes NOT listed here (sdmx,
# usdm, omop, fhir, odm, osb, ncit, dcat, odrl, dprod, dcterms, sdtm) are only
# checked for prefix declaration: they have no stable closed term set we can
# bundle, or they use path-style / code-based conventions. Extend as needed.
KNOWN_TERMS = {
    'skos': {  # SKOS core (http://www.w3.org/2004/02/skos/core#)
        'Concept', 'ConceptScheme', 'Collection', 'OrderedCollection',
        'prefLabel', 'altLabel', 'hiddenLabel', 'notation', 'note',
        'changeNote', 'definition', 'editorialNote', 'example',
        'historyNote', 'scopeNote',
        'broader', 'narrower', 'related', 'broaderTransitive',
        'narrowerTransitive', 'semanticRelation',
        'broadMatch', 'narrowMatch', 'relatedMatch', 'closeMatch',
        'exactMatch', 'mappingRelation',
        'inScheme', 'hasTopConcept', 'topConceptOf', 'member', 'memberList',
    },
    'qb': {  # RDF Data Cube (http://purl.org/linked-data/cube#)
        'Attachable', 'ComponentSet', 'DataSet', 'DataStructureDefinition',
        'SliceKey', 'ComponentProperty', 'MeasureProperty', 'CodedProperty',
        'DimensionProperty', 'AttributeProperty', 'ComponentSpecification',
        'Observation', 'ObservationGroup', 'Slice', 'HierarchicalCodeList',
        'dataSet', 'observation', 'slice', 'structure', 'component',
        'componentProperty', 'dimension', 'measure', 'attribute',
        'measureType', 'codeList', 'order', 'componentAttachment',
        'sliceStructure', 'sliceKey', 'concept', 'hierarchyRoot',
        'parentChildProperty',
    },
    'prov': {  # PROV-O (http://www.w3.org/ns/prov#)
        'Entity', 'Activity', 'Agent', 'Collection', 'Bundle', 'Person',
        'Organization', 'SoftwareAgent', 'Location', 'Influence', 'Usage',
        'Generation', 'Derivation', 'Attribution', 'Association', 'Delegation',
        'Communication', 'Start', 'End', 'Invalidation', 'InstantaneousEvent',
        'wasGeneratedBy', 'wasDerivedFrom', 'wasAttributedTo',
        'wasAssociatedWith', 'actedOnBehalfOf', 'used', 'wasInformedBy',
        'wasStartedBy', 'wasEndedBy', 'wasInvalidatedBy', 'startedAtTime',
        'endedAtTime', 'generatedAtTime', 'invalidatedAtTime', 'atTime',
        'wasRevisionOf', 'wasQuotedFrom', 'hadPrimarySource', 'alternateOf',
        'specializationOf', 'hadMember', 'value', 'atLocation', 'hadRole',
        'hadActivity', 'qualifiedAttribution', 'qualifiedAssociation',
        'qualifiedDerivation', 'qualifiedGeneration', 'qualifiedUsage',
    },
}


def collect_mapping_curies(schema_data):
    """Return list of (curie, json_path) for every external-vocabulary reference."""
    out = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in MAPPING_KEYS:
                    for c in (v if isinstance(v, list) else [v]):
                        if isinstance(c, str):
                            out.append((c, '.'.join(path + [k])))
                elif k in URI_KEYS and isinstance(v, str):
                    out.append((v, '.'.join(path + [k])))
                else:
                    walk(v, path + [str(k)])
        elif isinstance(node, list):
            for item in node:
                walk(item, path)

    for section in ('classes', 'enums', 'slots', 'types', 'subsets'):
        walk(schema_data.get(section, {}), [section])
    return out


def validate_mapping_iris(schema_data):
    """Check each mapping CURIE: declared prefix + known term where verifiable.

    Returns (errors, warnings). Errors: undeclared prefix, or unknown local name
    in a vocabulary with a bundled term set. Warnings: terms within one prefix
    that collide case-insensitively (a likely casing inconsistency).
    """
    prefixes = set(schema_data.get('prefixes', {}))
    errors, warnings = [], []
    by_prefix = {}

    for curie, where in collect_mapping_curies(schema_data):
        if ':' not in curie or curie.split(':', 1)[0] in ('http', 'https'):
            continue
        pre, local = curie.split(':', 1)
        by_prefix.setdefault(pre, {}).setdefault(local.lower(), set()).add(local)
        if pre not in prefixes:
            errors.append(f"undeclared prefix '{pre}:' in {curie} ({where})")
        elif pre in KNOWN_TERMS and local not in KNOWN_TERMS[pre]:
            errors.append(f"unknown {pre} term '{curie}' ({where})")

    for pre, locals_map in by_prefix.items():
        for variants in locals_map.values():
            if len(variants) > 1:
                # Differing only in the first character's case is the normal RDF
                # class-vs-property convention (Foo the class, foo the property);
                # only flag deeper casing differences (e.g. MetaData vs Metadata).
                normalized = {v[:1].lower() + v[1:] for v in variants}
                if len(normalized) > 1:
                    warnings.append(
                        f"inconsistent casing for {pre}: " + " vs ".join(sorted(variants))
                    )
    return errors, warnings


@click.command()
@click.option('--schema', default='dds.yaml', help='Path to schema file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--format', 'output_format', default='text', 
              type=click.Choice(['text', 'json', 'yaml']), help='Output format')
def validate_schema(schema: str, verbose: bool, output_format: str):
    """Validate Data Definition Specification schema for fit-for-purpose testing."""
    
    schema_path = Path(schema)
    if not schema_path.exists():
        console.print(f"[red]Error: Schema file {schema} not found[/red]")
        return 1
    
    console.print(f"[bold blue]Validating Data Definition Specification Schema: {schema}[/bold blue]")
    
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
        'linkml_validation': {},
        'mapping_iri_validation': {}
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
    
    # Mapping IRI validation
    console.print("\n[bold]6. Mapping IRI Validation[/bold]")
    iri_errors, iri_warnings = validate_mapping_iris(schema_data)
    console.print(
        f"  Term-checked vocabularies: {', '.join(sorted(KNOWN_TERMS))} "
        f"(others: prefix-declaration only)"
    )
    for w in iri_warnings:
        console.print(f"  [yellow]⚠ {w}[/yellow]")
    if iri_errors:
        for e in iri_errors:
            console.print(f"  [red]✗ {e}[/red]")
        console.print(f"  [red]✗ {len(iri_errors)} invalid mapping IRI(s)[/red]")
    else:
        console.print("  [green]✓ all mapping IRIs use declared prefixes and known terms[/green]")
    results['mapping_iri_validation'] = {
        'valid': not iri_errors,
        'error_count': len(iri_errors),
        'errors': iri_errors,
        'warnings': iri_warnings,
    }

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
    
    # Invalid mapping IRIs are a hard failure regardless of the heuristic score.
    return 0 if (overall_score >= 60 and not iri_errors) else 1

if __name__ == '__main__':
    validate_schema() 