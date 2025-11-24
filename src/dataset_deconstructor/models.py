"""
Shared models for dataset deconstruction - Standalone Version.

Contains shared dataclasses with no external dependencies.
"""

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING, Any

try:
    from .topic_detector import TopicInfo
    from .column_analyzer import ColumnAnalysis
except ImportError:
    from topic_detector import TopicInfo
    from column_analyzer import ColumnAnalysis


# Simplified ReifiedConceptInfo for standalone use
@dataclass
class ReifiedConceptInfo:
    """Simplified reified concept information."""
    OID: str
    name: str
    description: str


@dataclass
class TopicBreakdown:
    """Detailed breakdown for a specific topic."""
    topic_info: TopicInfo
    reified_concept: Optional[ReifiedConceptInfo]
    measure_columns: List[ColumnAnalysis]
    property_columns: List[ColumnAnalysis]
    attribute_columns: List[ColumnAnalysis]
    where_clause: str
    item_group_oid: str


if TYPE_CHECKING:
    from .detailed_breakdown import DatasetStructure

@dataclass
class DatasetBreakdown:
    """Complete breakdown of a dataset."""
    structure: Any  # DatasetStructure - avoiding circular import
    key_dimensions: List[ColumnAnalysis]
    topic_breakdowns: List[TopicBreakdown]
    global_attributes: List[ColumnAnalysis]
    data_structure_definition_oid: str
    dataset_oid: str

