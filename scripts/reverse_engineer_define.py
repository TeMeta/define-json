#!/usr/bin/env python3
"""
Reverse Engineer Define-JSON from Dataset-JSON

Reads actual dataset data (Dataset-JSON format) and automatically generates
Define-JSON metadata by analyzing the data structure and inferring:
- Variable classifications (IDENTIFIER, TIMING, TOPIC, RESULT, ATTRIBUTE)
- Dataset structure (vertical vs horizontal)
- SDMX roles (Dimension, Measure, Attribute)
- ItemGroup definitions
- ValueList contexts

Addresses the "throwing vase over wall" problem by bootstrapping metadata
from actual data rather than manual specification.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src/dataset_deconstructor"))

from dataset_deconstructor import (
    DatasetDeconstructor,
    DeconstructionConfig,
)
from variable_classifier import CDISCVariableClassifier

# Note: We don't actually use the generated classes for output, just plain dicts
# from define_json.schema.define import (
#     MetaDataVersion,
#     ItemGroupDef,
#     ItemDef,
#     DataType,
#     ItemGroupType,
#     WhereClause,
#     Condition,
#     RangeCheck,
#     Comparator,
# )

logger = logging.getLogger(__name__)


@dataclass
class DataCubeConfigSuggestion:
    """Suggested data cube configuration derived from data analysis."""
    domain: str
    dimensions: List[Dict[str, Any]]
    measures: List[Dict[str, Any]]
    attributes: List[Dict[str, Any]]
    confidence_threshold: float = 0.7


@dataclass
class ReverseEngineeringResult:
    """Complete result of reverse engineering process."""
    metadata_version: Dict[str, Any]  # Define-JSON structure
    data_cube_config_suggestion: DataCubeConfigSuggestion
    analysis_summary: Dict[str, Any]


class DatasetJSONReader:
    """Reads Dataset-JSON and converts to pandas DataFrame."""
    
    @staticmethod
    def read(path: Path) -> pd.DataFrame:
        """
        Read Dataset-JSON file and convert to DataFrame.
        
        Dataset-JSON structure:
        {
          "clinicalData": {
            "itemGroupData": {
              "IG.LB": {
                "records": [
                  ["STUDY01", "SUBJ001", ...],
                  ...
                ],
                "columns": [
                  {"name": "STUDYID", "label": "Study", "dataType": "string"},
                  ...
                ]
              }
            }
          }
        }
        """
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Extract first itemGroupData (support single domain for now)
        clinical_data = data.get("clinicalData", {})
        item_group_data = clinical_data.get("itemGroupData", {})
        
        if not item_group_data:
            raise ValueError("No itemGroupData found in Dataset-JSON")
        
        # Get first item group
        ig_name = list(item_group_data.keys())[0]
        ig_data = item_group_data[ig_name]
        
        # Extract columns and records
        columns = [col["name"] for col in ig_data.get("columns", [])]
        records = ig_data.get("records", [])
        
        # Create DataFrame
        df = pd.DataFrame(records, columns=columns)
        
        logger.info(f"Loaded Dataset-JSON: {ig_name} with {len(df)} rows, {len(df.columns)} columns")
        return df, ig_name


class DataCubeConfigGenerator:
    """Generates data cube configuration suggestions from CDISC classifications."""
    
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        self.classifier = CDISCVariableClassifier()
    
    def generate_config(self, df: pd.DataFrame, domain: str) -> DataCubeConfigSuggestion:
        """
        Generate data cube configuration suggestion from dataset analysis.
        
        Mapping from CDISC Variable Types to data cube roles:
        - IDENTIFIER → Dimension (subject, study, sequence)
        - TIMING → Dimension (visit, date)
        - TOPIC → Dimension (test code, parameter)
        - RESULT → Measure (observed result, standardized result)
        - ATTRIBUTE → Attribute (units, categories, methods)
        """
        classifications = self.classifier.classify_dataset_columns(df)
        
        dimensions = []
        measures = []
        attributes = []
        
        for col_name, classification in classifications.items():
            var_type = classification.variable_type.value
            confidence = classification.confidence
            
            entry = {
                "name": col_name,
                "confidence": confidence,
                "reason": classification.reason,
                "cdisc_type": var_type
            }
            
            # Map CDISC types to SDMX roles
            if var_type == "identifier":
                dimensions.append(entry)
            elif var_type == "timing":
                dimensions.append(entry)
            elif var_type == "topic":
                dimensions.append({
                    **entry,
                    "dimension_type": "topic",
                    "note": "Topic dimension - defines what is being measured"
                })
            elif var_type == "result":
                measures.append(entry)
            elif var_type == "attribute":
                attributes.append(entry)
            else:
                # Unclassified - default to attribute with low confidence
                attributes.append({
                    **entry,
                    "confidence": 0.5,
                    "note": "Unclassified - defaulted to attribute"
                })
        
        return DataCubeConfigSuggestion(
            domain=domain,
            dimensions=dimensions,
            measures=measures,
            attributes=attributes,
            confidence_threshold=self.confidence_threshold
        )


class DefineJSONGenerator:
    """Generates Define-JSON structure from deconstruction results."""
    
    def __init__(self):
        self.deconstructor = DatasetDeconstructor(
            config=DeconstructionConfig(enable_specialisation_building=True)
        )
    
    def generate(self, df: pd.DataFrame, domain: str, 
                 cube_config: DataCubeConfigSuggestion) -> Dict[str, Any]:
        """
        Generate Define-JSON metadata from dataset analysis.
        
        Returns:
            MetaDataVersion structure as dictionary
        """
        # Deconstruct dataset
        breakdown = self.deconstructor.deconstruct_dataset(df, domain)
        
        # Generate ItemDefs
        item_defs = []
        for col in df.columns:
            # Infer data type from pandas dtype
            dtype = self._infer_data_type(df[col])
            
            item_def = {
                "OID": f"IT.{domain}.{col}",
                "name": col,
                "dataType": dtype,
                "description": f"{col} variable in {domain} domain",
                # Add role from cube configuration
                "cube_role": self._get_cube_role(col, cube_config),
                "cdisc_classification": self._get_cdisc_classification(col, df)
            }
            item_defs.append(item_def)
        
        # Generate ItemGroupDefs
        item_group_defs = []
        
        # Main ItemGroup
        main_ig = {
            "OID": f"IG.{domain}",
            "name": domain,
            "type": breakdown.structure.structure_type.value,
            "items": [f"IT.{domain}.{col}" for col in df.columns],
            "description": f"{domain} domain dataset"
        }
        item_group_defs.append(main_ig)
        
        # If vertical structure, create topic-specific ItemGroups
        if breakdown.structure.structure_type.value == "vertical":
            for topic_breakdown in breakdown.topic_breakdowns:
                topic_ig = {
                    "OID": topic_breakdown.item_group_oid,
                    "name": topic_breakdown.topic_info.topic_name,
                    "type": "DataSpecialization",
                    "applicableWhen": [topic_breakdown.where_clause] if topic_breakdown.where_clause else [],
                    "items": [f"IT.{domain}.{col.name}" for col in topic_breakdown.measure_columns],
                    "description": f"Specialization for {topic_breakdown.topic_info.topic_name}"
                }
                item_group_defs.append(topic_ig)
        
        metadata_version = {
            "OID": f"MDV.{domain}.REV_ENG",
            "name": f"{domain} Reverse Engineered Metadata",
            "description": f"Automatically generated metadata from dataset analysis",
            "ItemGroupDefs": item_group_defs,
            "ItemDefs": item_defs,
            "analysis_metadata": {
                "structure_type": breakdown.structure.structure_type.value,
                "topic_dimension": breakdown.structure.topic_dimension,
                "topics_found": [t.topic_name for t in breakdown.structure.topics],
                "key_dimensions": breakdown.structure.key_dimensions,
                "measure_columns": breakdown.structure.measure_columns,
            }
        }
        
        return metadata_version
    
    def _infer_data_type(self, series: pd.Series) -> str:
        """Infer Define-JSON DataType from pandas dtype."""
        dtype_map = {
            "int64": "integer",
            "float64": "float",
            "object": "string",
            "bool": "boolean",
            "datetime64": "datetime"
        }
        return dtype_map.get(str(series.dtype), "string")
    
    def _get_cube_role(self, col_name: str, config: DataCubeConfigSuggestion) -> str:
        """Get data cube role for column from configuration."""
        for dim in config.dimensions:
            if dim["name"] == col_name:
                return "Dimension"
        for meas in config.measures:
            if meas["name"] == col_name:
                return "Measure"
        for attr in config.attributes:
            if attr["name"] == col_name:
                return "Attribute"
        return "Unknown"
    
    def _get_cdisc_classification(self, col_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Get CDISC classification for column."""
        classifier = CDISCVariableClassifier()
        classifications = classifier.classify_dataset_columns(df)
        
        if col_name in classifications:
            classification = classifications[col_name]
            return {
                "type": classification.variable_type.value,
                "confidence": classification.confidence,
                "reason": classification.reason
            }
        return {"type": "unknown", "confidence": 0.0, "reason": "Not classified"}


class ReverseEngineer:
    """Main reverse engineering orchestrator."""
    
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        self.config_generator = DataCubeConfigGenerator(confidence_threshold)
        self.define_generator = DefineJSONGenerator()
    
    def reverse_engineer(self, dataset_json_path: Path, 
                        domain: Optional[str] = None) -> ReverseEngineeringResult:
        """
        Complete reverse engineering pipeline.
        
        Args:
            dataset_json_path: Path to Dataset-JSON file
            domain: Optional domain name (will be inferred if not provided)
            
        Returns:
            Complete reverse engineering result with metadata and policy
        """
        logger.info(f"🔍 Starting reverse engineering: {dataset_json_path}")
        
        # Step 1: Read Dataset-JSON
        df, inferred_domain = DatasetJSONReader.read(dataset_json_path)
        domain = domain or inferred_domain
        
        # Step 2: Generate data cube configuration suggestion
        logger.info("📊 Generating data cube configuration suggestions...")
        cube_config = self.config_generator.generate_config(df, domain)
        
        # Step 3: Generate Define-JSON metadata
        logger.info("📝 Generating Define-JSON metadata...")
        metadata = self.define_generator.generate(df, domain, cube_config)
        
        # Step 4: Create analysis summary
        summary = {
            "domain": domain,
            "rows": len(df),
            "columns": len(df.columns),
            "structure_type": metadata["analysis_metadata"]["structure_type"],
            "topics_found": len(metadata["analysis_metadata"]["topics_found"]),
            "confidence_summary": {
                "dimensions": len(cube_config.dimensions),
                "measures": len(cube_config.measures),
                "attributes": len(cube_config.attributes),
            }
        }
        
        logger.info(f"✅ Reverse engineering complete!")
        logger.info(f"   Structure: {summary['structure_type']}")
        logger.info(f"   Topics: {summary['topics_found']}")
        logger.info(f"   Dimensions: {summary['confidence_summary']['dimensions']}")
        logger.info(f"   Measures: {summary['confidence_summary']['measures']}")
        
        return ReverseEngineeringResult(
            metadata_version=metadata,
            data_cube_config_suggestion=cube_config,
            analysis_summary=summary
        )
    
    def write_outputs(self, result: ReverseEngineeringResult, output_dir: Path):
        """Write all outputs to files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Define-JSON metadata
        define_json_path = output_dir / "define_metadata.json"
        with open(define_json_path, 'w') as f:
            json.dump(result.metadata_version, f, indent=2)
        logger.info(f"📄 Wrote Define-JSON: {define_json_path}")
        
        # 2. Data cube configuration suggestion (YAML format)
        config_yaml_path = output_dir / "data_cube_config_suggestion.yaml"
        import yaml
        
        config_dict = {
            "domain": result.data_cube_config_suggestion.domain,
            "confidence_threshold": result.data_cube_config_suggestion.confidence_threshold,
            "dimensions": result.data_cube_config_suggestion.dimensions,
            "measures": result.data_cube_config_suggestion.measures,
            "attributes": result.data_cube_config_suggestion.attributes,
        }
        
        with open(config_yaml_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
        logger.info(f"📄 Wrote data cube config: {config_yaml_path}")
        
        # 3. Analysis summary
        summary_path = output_dir / "analysis_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(result.analysis_summary, f, indent=2)
        logger.info(f"📄 Wrote summary: {summary_path}")
        
        # 4. Human-readable report
        report_path = output_dir / "reverse_engineering_report.md"
        self._write_report(result, report_path)
        logger.info(f"📄 Wrote report: {report_path}")
    
    def _write_report(self, result: ReverseEngineeringResult, path: Path):
        """Write human-readable markdown report."""
        config = result.data_cube_config_suggestion
        summary = result.analysis_summary
        metadata = result.metadata_version
        
        report = f"""# Reverse Engineering Report

## Summary

- **Domain**: {summary['domain']}
- **Rows**: {summary['rows']:,}
- **Columns**: {summary['columns']}
- **Structure Type**: {summary['structure_type']}
- **Topics Found**: {summary['topics_found']}

## Data Cube Configuration

### Dimensions ({len(config.dimensions)})
Variables that define coordinates/axes of the data cube:

"""
        for dim in config.dimensions:
            report += f"- **{dim['name']}** (confidence: {dim['confidence']:.2f})\n"
            report += f"  - CDISC Type: `{dim['cdisc_type']}`\n"
            report += f"  - Reason: {dim['reason']}\n"
            if 'note' in dim:
                report += f"  - Note: {dim['note']}\n"
        
        report += f"\n### Measures ({len(config.measures)})\n"
        report += "Variables containing actual measurement values:\n\n"
        for meas in config.measures:
            report += f"- **{meas['name']}** (confidence: {meas['confidence']:.2f})\n"
            report += f"  - CDISC Type: `{meas['cdisc_type']}`\n"
            report += f"  - Reason: {meas['reason']}\n"
        
        report += f"\n### Attributes ({len(config.attributes)})\n"
        report += "Variables containing metadata/context:\n\n"
        for attr in config.attributes:
            report += f"- **{attr['name']}** (confidence: {attr['confidence']:.2f})\n"
            report += f"  - CDISC Type: `{attr['cdisc_type']}`\n"
            report += f"  - Reason: {attr['reason']}\n"
        
        report += "\n## Dataset Structure Analysis\n\n"
        report += f"- **Structure Type**: {metadata['analysis_metadata']['structure_type']}\n"
        report += f"- **Topic Dimension**: {metadata['analysis_metadata']['topic_dimension']}\n"
        report += f"- **Topics**: {', '.join(metadata['analysis_metadata']['topics_found'])}\n"
        report += f"- **Key Dimensions**: {', '.join(metadata['analysis_metadata']['key_dimensions'])}\n"
        
        report += "\n## ItemGroup Definitions Generated\n\n"
        for ig in metadata['ItemGroupDefs']:
            report += f"### {ig['name']} (`{ig['OID']}`)\n"
            report += f"- Type: `{ig['type']}`\n"
            report += f"- Items: {len(ig['items'])}\n"
            if ig.get('applicableWhen'):
                report += f"- Applicable When: `{ig['applicableWhen'][0]}`\n"
            report += "\n"
        
        report += "\n## Next Steps\n\n"
        report += "1. **Review Classifications**: Check data cube role assignments match domain knowledge\n"
        report += "2. **Adjust Configuration**: Edit `data_cube_config_suggestion.yaml` if needed\n"
        report += "3. **Enhance Metadata**: Add descriptions, labels, CodeLists\n"
        report += "4. **Validate**: Run consistency checks against source data\n"
        report += "5. **Integrate**: Incorporate into Define-JSON IR pipeline\n"
        
        with open(path, 'w') as f:
            f.write(report)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Reverse engineer Define-JSON metadata from Dataset-JSON"
    )
    parser.add_argument(
        "dataset_json",
        type=Path,
        help="Path to Dataset-JSON file"
    )
    parser.add_argument(
        "--domain",
        help="Domain name (will be inferred if not provided)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reverse_engineered"),
        help="Output directory for generated files (default: reverse_engineered/)"
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.7,
        help="Confidence threshold for classifications (default: 0.7)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s - %(message)s'
    )
    
    # Run reverse engineering
    engineer = ReverseEngineer(confidence_threshold=args.confidence)
    
    try:
        result = engineer.reverse_engineer(args.dataset_json, args.domain)
        engineer.write_outputs(result, args.output_dir)
        
        print(f"\n✅ Reverse engineering complete!")
        print(f"📁 Outputs written to: {args.output_dir}")
        print(f"\nGenerated files:")
        print(f"  - define_metadata.json               (Define-JSON metadata)")
        print(f"  - data_cube_config_suggestion.yaml   (Data cube configuration)")
        print(f"  - analysis_summary.json              (Analysis metrics)")
        print(f"  - reverse_engineering_report.md      (Human-readable report)")
        
    except Exception as e:
        logger.error(f"❌ Reverse engineering failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

