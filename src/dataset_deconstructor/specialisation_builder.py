"""
Dataset specialisation builder for dataset deconstruction.

This module provides focused specialisation building functionality that can be easily tested.
"""

import uuid
from typing import List, Dict, Any
from dataclasses import dataclass

try:
    from .models import DatasetBreakdown
except ImportError:
    from models import DatasetBreakdown


@dataclass
class SpecialisationComponents:
    """Components of a dataset specialisation."""
    data_structure_definition: Dict[str, Any]
    reified_concepts: List[Dict[str, Any]]
    item_groups: List[Dict[str, Any]]
    items: List[Dict[str, Any]]
    code_lists: List[Dict[str, Any]]
    range_checks: List[Dict[str, Any]]
    codings: List[Dict[str, Any]]
    dataset: Dict[str, Any]


class SpecialisationBuilder:
    """
    Builds complete Dataset Specialisations using the detailed breakdown analysis.
    
    This class is focused solely on building specialisations and can be easily tested.
    """
    
    def __init__(self):
        self.data_type_mapping = {
            'object': 'text',
            'string': 'text',
            'int64': 'integer',
            'float64': 'float',
            'datetime64[ns]': 'datetime',
            'bool': 'boolean'
        }
    
    def build_specialisation(self, breakdown: DatasetBreakdown) -> SpecialisationComponents:
        """
        Build a complete Dataset Specialisation from the breakdown analysis.
        
        Args:
            breakdown: Detailed dataset breakdown
            
        Returns:
            SpecialisationComponents with all specialisation parts
        """
        # Build individual components
        dsd = self._build_data_structure_definition(breakdown)
        reified_concepts = self._build_reified_concepts(breakdown)
        item_groups = self._build_item_groups(breakdown)
        items = self._build_items(breakdown)
        code_lists = self._build_code_lists(breakdown)
        range_checks = self._build_range_checks(breakdown)
        codings = self._build_codings(breakdown)
        dataset = self._build_dataset(breakdown)
        
        return SpecialisationComponents(
            data_structure_definition=dsd,
            reified_concepts=reified_concepts,
            item_groups=item_groups,
            items=items,
            code_lists=code_lists,
            range_checks=range_checks,
            codings=codings,
            dataset=dataset
        )
    
    def build_specialisation_dict(self, breakdown: DatasetBreakdown) -> Dict[str, Any]:
        """
        Build a complete Dataset Specialisation as a dictionary.
        
        Args:
            breakdown: Detailed dataset breakdown
            
        Returns:
            Complete Dataset Specialisation as a dictionary
        """
        components = self.build_specialisation(breakdown)
        
        return {
            "DataStructureDefinition": components.data_structure_definition,
            "ReifiedConcepts": components.reified_concepts,
            "ItemGroups": components.item_groups,
            "Items": components.items,
            "CodeLists": components.code_lists,
            "RangeChecks": components.range_checks,
            "Codings": components.codings,
            "Dataset": components.dataset
        }
    
    def _build_data_structure_definition(self, breakdown: DatasetBreakdown) -> Dict[str, Any]:
        """Build DataStructureDefinition."""
        structure = breakdown.structure
        
        dimensions = [col.name for col in breakdown.key_dimensions]
        if structure.topic_dimension:
            dimensions.append(structure.topic_dimension)
        
        measures = []
        attributes = []
        
        for topic_breakdown in breakdown.topic_breakdowns:
            measures.extend([col.name for col in topic_breakdown.measure_columns])
            attributes.extend([col.name for col in topic_breakdown.attribute_columns])
        
        # Add global attributes
        attributes.extend([col.name for col in breakdown.global_attributes])
        
        return {
            "OID": breakdown.data_structure_definition_oid,
            "name": f"DSD_{structure.structure_type.value}",
            "dimensions": dimensions,
            "measures": list(set(measures)),
            "attributes": list(set(attributes)),
            "description": f"Data Structure Definition for {structure.structure_type.value} dataset"
        }
    
    def _build_reified_concepts(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build ReifiedConcepts with proper Coding."""
        reified_concepts = []
        
        for topic_breakdown in breakdown.topic_breakdowns:
            if topic_breakdown.reified_concept:
                rc = topic_breakdown.reified_concept
                
                # Build comprehensive coding
                coding = []
                # Note: concept_match not available in current ReifiedConcept implementation
                
                # Add domain coding
                if breakdown.structure.topic_dimension:
                    domain = breakdown.structure.topic_dimension[:2]
                    coding.append(f"domain:{domain}")
                
                # Add topic-specific coding
                coding.append(f"topic:{topic_breakdown.topic_info.topic_name}")
                coding.append("type:observation")
                
                reified_concept = {
                    "OID": rc.OID,
                    "name": rc.name,
                    "description": rc.description,
                    "coding": coding,
                    "uuid": str(uuid.uuid4())
                }
                
                reified_concepts.append(reified_concept)
        
        return reified_concepts
    
    def _build_item_groups(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build ItemGroups including nested topic-specific ones."""
        item_groups = []
        
        # Main dataset ItemGroup
        main_items = []
        for col_analysis in breakdown.key_dimensions + breakdown.global_attributes:
            main_items.append(col_analysis.name)
        
        main_ig = {
            "OID": f"IG_MAIN_{breakdown.dataset_oid}",
            "name": f"Main_{breakdown.structure.structure_type.value}",
            "description": f"Main ItemGroup for {breakdown.structure.structure_type.value} dataset",
            "items": main_items,
            "children": [tb.item_group_oid for tb in breakdown.topic_breakdowns]
        }
        item_groups.append(main_ig)
        
        # Topic-specific ItemGroups
        for topic_breakdown in breakdown.topic_breakdowns:
            items = []
            items.extend([col.name for col in topic_breakdown.measure_columns])
            items.extend([col.name for col in topic_breakdown.property_columns])
            items.extend([col.name for col in topic_breakdown.attribute_columns])
            
            ig = {
                "OID": topic_breakdown.item_group_oid,
                "name": f"Topic_{topic_breakdown.topic_info.topic_name}",
                "description": f"ItemGroup for topic: {topic_breakdown.topic_info.topic_name}",
                "whereClause": topic_breakdown.where_clause,
                "implementsConcept": topic_breakdown.reified_concept.OID if topic_breakdown.reified_concept else None,
                "items": items,
                "coding": [
                    f"topic:{topic_breakdown.topic_info.topic_name}",
                    "type:topic_specialisation",
                    "role:observation_group"
                ]
            }
            item_groups.append(ig)
        
        return item_groups
    
    def _build_items(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build Items with proper Coding."""
        items = []
        
        # Process all columns
        all_columns = []
        all_columns.extend(breakdown.key_dimensions)
        all_columns.extend(breakdown.global_attributes)
        
        for topic_breakdown in breakdown.topic_breakdowns:
            all_columns.extend(topic_breakdown.measure_columns)
            all_columns.extend(topic_breakdown.property_columns)
            all_columns.extend(topic_breakdown.attribute_columns)
        
        for col_analysis in all_columns:
            item = {
                "OID": f"ITEM_{col_analysis.name}",
                "name": col_analysis.name,
                "dataType": self._map_data_type(col_analysis.data_type),
                "coding": col_analysis.coding_suggestions,
                "description": f"Item for column: {col_analysis.name}",
                "mandatory": col_analysis.null_count == 0
            }
            
            # Add topic relationship if applicable
            if col_analysis.topic_related:
                item["coding"].append(f"topic_related:{col_analysis.topic_related}")
            
            items.append(item)
        
        return items
    
    def _build_code_lists(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build CodeLists from categorical data."""
        code_lists = []
        
        for col_analysis in breakdown.key_dimensions + breakdown.global_attributes:
            if col_analysis.data_type == 'object' and len(col_analysis.unique_values) <= 20:
                code_list = {
                    "OID": f"CL_{col_analysis.name}",
                    "name": f"CodeList_{col_analysis.name}",
                    "description": f"CodeList for {col_analysis.name}",
                    "coding": ["type:codelist", f"source:column:{col_analysis.name}"],
                    "items": [
                        {
                            "codedValue": val,
                            "decode": val,
                            "coding": [f"value:{val}"]
                        }
                        for val in col_analysis.unique_values
                    ]
                }
                code_lists.append(code_list)
        
        return code_lists
    
    def _build_range_checks(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build RangeChecks from numeric data."""
        range_checks = []
        
        # This would analyze the actual data to determine ranges
        # For now, create placeholder range checks
        for col_analysis in breakdown.key_dimensions + breakdown.global_attributes:
            if col_analysis.data_type in ['float64', 'int64']:
                range_check = {
                    "OID": f"RC_{col_analysis.name}",
                    "name": f"RangeCheck_{col_analysis.name}",
                    "description": f"Range check for {col_analysis.name}",
                    "coding": ["type:range_check", f"source:column:{col_analysis.name}"],
                    "item": f"ITEM_{col_analysis.name}"
                }
                range_checks.append(range_check)
        
        return range_checks
    
    def _build_codings(self, breakdown: DatasetBreakdown) -> List[Dict[str, Any]]:
        """Build Codings for concept mapping."""
        codings = []
        
        for topic_breakdown in breakdown.topic_breakdowns:
            if topic_breakdown.reified_concept:
                # Create basic coding for each concept
                coding = {
                    "OID": f"CODING_{topic_breakdown.reified_concept.OID}",
                    "name": f"Coding_{topic_breakdown.topic_info.topic_name}",
                    "description": f"Coding for {topic_breakdown.topic_info.topic_name}",
                    "system": "internal",  # Default system since we don't have external concept mapping
                    "code": topic_breakdown.reified_concept.OID,
                    "display": topic_breakdown.topic_info.topic_name
                }
                codings.append(coding)
        
        return codings
    
    def _build_dataset(self, breakdown: DatasetBreakdown) -> Dict[str, Any]:
        """Build the main Dataset component."""
        return {
            "OID": breakdown.dataset_oid,
            "name": f"{breakdown.structure.structure_type.value}_dataset",
            "structuredBy": breakdown.data_structure_definition_oid,
            "description": f"Dataset specialisation for {breakdown.structure.structure_type.value} structure"
        }
    
    def _map_data_type(self, pandas_dtype: str) -> str:
        """Map pandas data types to CDISC data types."""
        return self.data_type_mapping.get(pandas_dtype, 'text')
