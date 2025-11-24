"""
Utilities module for Define-JSON.

Common utilities and helper functions.
"""

from .cli import main, create_cli_parser
from .ir import (
    load_mdv,
    canonicalise_whereclause,
    build_where_registry,
    build_canonical_slices,
    enforce_slice_invariants,
    register_variables,
    project_valuelist_for_domain,
    serialize_canonical,
    export_define_xml_21,
    export_define_xml_10,
)
from .sdmx import (
    load_data_cube_config,
    load_sdmx_policy,
    classify_item_role,
    build_dsd_for_domain,
    validate_dsd_completeness,
    is_clean_whereclause,
    derive_groupkey_from_whereclause,
    analyze_attribute_variance,
    infer_attribute_relationships,
)

__all__ = [
    # CLI
    "main",
    "create_cli_parser",
    # IR utilities
    "load_mdv",
    "canonicalise_whereclause",
    "build_where_registry",
    "build_canonical_slices",
    "enforce_slice_invariants",
    "register_variables",
    "project_valuelist_for_domain",
    "serialize_canonical",
    "export_define_xml_21",
    "export_define_xml_10",
    # SDMX utilities
    "load_data_cube_config",
    "load_sdmx_policy",
    "classify_item_role",
    "build_dsd_for_domain",
    "validate_dsd_completeness",
    "is_clean_whereclause",
    "derive_groupkey_from_whereclause",
    "analyze_attribute_variance",
    "infer_attribute_relationships",
]
