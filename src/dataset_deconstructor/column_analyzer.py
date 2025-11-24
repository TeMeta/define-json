"""
Column analysis for dataset deconstruction - Standalone Version.

Provides focused column analysis functionality with no external dependencies.
"""

import pandas as pd
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from .topic_detector import DatasetStructure, StructureType
except ImportError:
    from topic_detector import DatasetStructure, StructureType


class ColumnRole(Enum):
    """Role of a column in the dataset."""
    KEY = "key"  # Study, subject, time dimensions
    TOPIC = "topic"  # Observation topic (e.g., VSTESTCD)
    MEASURE = "measure"  # Result values (e.g., VSORRES)
    ATTRIBUTE = "attribute"  # Metadata (e.g., VSORRESU, VSDTC)
    PROPERTY = "property"  # Topic-specific properties (e.g., BMI_UNIT)


@dataclass
class ColumnAnalysis:
    """Detailed analysis of a dataset column."""
    name: str
    role: ColumnRole
    data_type: str
    null_count: int
    unique_values: List[str]
    coding_suggestions: List[str]
    topic_related: Optional[str] = None

