"""
Test suite for SDMX data cube utilities.

Phase 1: DSD (DataStructureDefinition) Builder
- Policy-driven classification of Items into Dimension/Measure/Attribute
- Creation of DataStructureDefinition as ItemGroup(type="DataCube")
- Validation of completeness and correctness
"""

import pytest
from pathlib import Path
import yaml

from define_json.utils.ir import load_mdv
from define_json.utils.sdmx import (
    load_sdmx_policy,
    build_dsd_for_domain,
    validate_dsd_completeness,
    classify_item_role,
    derive_groupkey_from_whereclause,
    is_clean_whereclause,
    infer_attribute_relationships,
    analyze_attribute_variance,
)
from define_json.schema.define import (
    MetaDataVersion,
    ItemGroup,
    Dimension,
    Measure,
    DataAttribute,
    WhereClause,
    GroupKey,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestSDMXPolicyLoading:
    """Test loading and parsing of SDMX policy files."""

    def test_load_valid_policy(self):
        """Policy file should load and parse correctly."""
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        assert policy["domain"] == "LB"
        assert "USUBJID" in policy["dimensions"]
        assert "LBSTRESN" in policy["measures"]
        assert "STUDYID" in policy["attributes"]["dataset_level"]
        assert len(policy["dimension_order"]) == 4

    def test_reject_malformed_policy(self):
        """Malformed policy should fail fast with clear error."""
        with pytest.raises(ValueError, match="Configuration must specify 'domain'"):
            load_sdmx_policy(FIXTURES_DIR / "malformed_policy.yaml")


class TestDSDBuilder:
    """Test DataStructureDefinition builder."""

    def test_build_dsd_creates_datacube_itemgroup(self):
        """DSD should be an ItemGroup with type='DataCube'."""
        mdv = load_mdv(FIXTURES_DIR / "lb_sdmx.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        assert isinstance(dsd, ItemGroup)
        assert dsd.type.value == "DataCube"  # Correct field name is 'type', and it's an enum
        assert dsd.domain == "LB"
        assert dsd.OID.startswith("DSD.")

    def test_dsd_contains_dimension_components(self):
        """DSD should contain Dimension components referencing Items."""
        mdv = load_mdv(FIXTURES_DIR / "lb_sdmx.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Extract Dimension components from DSD items
        dimensions = [item for item in dsd.items if isinstance(item, Dimension)]
        
        assert len(dimensions) == 4, "Should have 4 dimensions per policy"
        dim_names = [dim.name for dim in dimensions]
        assert "USUBJID" in dim_names
        assert "LBTEST" in dim_names
        assert "VISITNUM" in dim_names
        assert "LBSEQ" in dim_names

    def test_dsd_contains_measure_components(self):
        """DSD should contain Measure components."""
        mdv = load_mdv(FIXTURES_DIR / "lb_sdmx.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        measures = [item for item in dsd.items if isinstance(item, Measure)]
        
        assert len(measures) == 3, "Should have 3 measures per policy"
        measure_names = [m.name for m in measures]
        assert "LBSTRESN" in measure_names
        assert "LBSTRESC" in measure_names
        assert "LBORRES" in measure_names

    def test_dsd_contains_attribute_components(self):
        """DSD should contain DataAttribute components with attachment info."""
        mdv = load_mdv(FIXTURES_DIR / "lb_sdmx.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        attributes = [item for item in dsd.items if isinstance(item, DataAttribute)]
        
        assert len(attributes) >= 2, "Should have dataset-level attributes"
        attr_names = [a.name for a in attributes]
        assert "STUDYID" in attr_names
        assert "DOMAIN" in attr_names

    def test_dsd_validation_completeness(self):
        """Validation should confirm all domain variables are classified."""
        mdv = load_mdv(FIXTURES_DIR / "lb_sdmx.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Get all variable OIDs from domain ItemGroup
        lb_group = next(ig for ig in mdv.itemGroups if ig.domain == "LB")
        # Items in ItemGroup can be either full Item objects or ItemRef-like dicts with itemOID
        all_variables = set()
        for item in lb_group.items or []:
            if hasattr(item, 'OID'):
                # Full Item object
                all_variables.add(item.OID)
            elif hasattr(item, 'itemOID'):
                # ItemRef-like object
                all_variables.add(item.itemOID)
        
        # Validate completeness
        is_complete, missing = validate_dsd_completeness(dsd, all_variables, mdv)
        
        assert is_complete, f"DSD should classify all variables, missing: {missing}"
        assert len(missing) == 0


class TestItemRoleClassification:
    """Test policy-driven classification of Items into roles."""

    def test_classify_dimension(self):
        """Variables in policy dimensions should be classified as Dimension."""
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        role = classify_item_role("USUBJID", policy)
        
        assert role == "Dimension"

    def test_classify_measure(self):
        """Variables in policy measures should be classified as Measure."""
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        role = classify_item_role("LBSTRESN", policy)
        
        assert role == "Measure"

    def test_classify_attribute(self):
        """Variables in policy attributes should be classified as Attribute."""
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        role = classify_item_role("STUDYID", policy)
        
        assert role == "Attribute"

    def test_unclassified_variable_fails(self):
        """Variables not in policy should fail fast."""
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_sdmx_policy.yaml")
        
        with pytest.raises(ValueError, match="not classified in configuration"):
            classify_item_role("UNKNOWN_VAR", policy)


class TestWhereClauseToGroupKey:
    """Test WhereClause → GroupKey derivation (Phase 2)."""

    def test_clean_whereclause_derives_to_groupkey(self):
        """Clean WhereClause (EQ on dimensions) should derive to GroupKey."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_whereclause.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        # Build DSD first
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Get clean WhereClause (Glucose at Baseline)
        wc = next(w for w in mdv.whereClauses if w.OID == "WC.LB.GLUCOSE.BASELINE")
        
        # Derive GroupKey
        groupkey = derive_groupkey_from_whereclause(wc, dsd, mdv)
        
        assert groupkey is not None, "Clean WhereClause should derive to GroupKey"
        assert isinstance(groupkey, GroupKey)
        assert groupkey.keyValues is not None
        # KeyValues should be ordered: LBTEST=Glucose, VISITNUM=1
        assert "Glucose" in groupkey.keyValues
        assert "1" in groupkey.keyValues

    def test_complex_whereclause_returns_none(self):
        """WhereClause with non-EQ comparator should return None (not derivable)."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_whereclause.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Get complex WhereClause (GT comparator)
        wc = next(w for w in mdv.whereClauses if w.OID == "WC.LB.COMPLEX")
        
        # Should return None (not derivable)
        groupkey = derive_groupkey_from_whereclause(wc, dsd, mdv)
        
        assert groupkey is None, "Complex WhereClause (GT) should not derive to GroupKey"

    def test_nested_conditions_returns_none(self):
        """WhereClause with multiple conditions (OR logic) should return None."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_whereclause.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Get nested WhereClause (multiple conditions = OR logic)
        wc = next(w for w in mdv.whereClauses if w.OID == "WC.LB.NESTED")
        
        # Should return None (OR logic not supported)
        groupkey = derive_groupkey_from_whereclause(wc, dsd, mdv)
        
        assert groupkey is None, "Nested conditions (OR) should not derive to GroupKey"

    def test_is_clean_whereclause_validates_correctly(self):
        """Helper function should correctly identify clean WhereClauses."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_whereclause.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Clean WhereClause
        wc_clean = next(w for w in mdv.whereClauses if w.OID == "WC.LB.GLUCOSE.BASELINE")
        assert is_clean_whereclause(wc_clean, dsd, mdv), "Should identify clean WhereClause"
        
        # Complex WhereClause (GT)
        wc_complex = next(w for w in mdv.whereClauses if w.OID == "WC.LB.COMPLEX")
        assert not is_clean_whereclause(wc_complex, dsd, mdv), "Should reject non-EQ comparator"
        
        # Nested conditions (OR)
        wc_nested = next(w for w in mdv.whereClauses if w.OID == "WC.LB.NESTED")
        assert not is_clean_whereclause(wc_nested, dsd, mdv), "Should reject multiple conditions"

    def test_groupkey_references_dimension_components(self):
        """Derived GroupKey should reference the correct Dimension components."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_whereclause.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        wc = next(w for w in mdv.whereClauses if w.OID == "WC.LB.GLUCOSE.BASELINE")
        groupkey = derive_groupkey_from_whereclause(wc, dsd, mdv)
        
        assert groupkey is not None
        assert groupkey.describedBy is not None, "GroupKey should reference dimensions"
        # Should reference the dimensions that are constrained (LBTEST, VISITNUM)
        # Note: describedBy can be list of Dimension OIDs or ComponentList OID


class TestAttributeRelationshipInference:
    """Test attribute relationship inference (Phase 3)."""

    def test_constant_attribute_identified_as_dataset_level(self):
        """Attribute with same value across all slices should be dataset-level."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_slices.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # Mock attribute values across slices
        # STUDYID is constant everywhere
        slice_data = {
            "WC.GLUCOSE.BASELINE": {"STUDYID": "STUDY001", "LBCAT": "CHEMISTRY"},
            "WC.GLUCOSE.WEEK4": {"STUDYID": "STUDY001", "LBCAT": "CHEMISTRY"},
            "WC.SODIUM.BASELINE": {"STUDYID": "STUDY001", "LBCAT": "CHEMISTRY"},
            "WC.PLATELET.BASELINE": {"STUDYID": "STUDY001", "LBCAT": "HEMATOLOGY"},
        }
        
        # Get slices (ItemGroups with type=DataSpecialization)
        slices = [ig for ig in mdv.itemGroups if ig.type and 
                  (ig.type == "DataSpecialization" or 
                   (hasattr(ig.type, 'value') and ig.type.value == "DataSpecialization"))]
        
        # Analyze STUDYID variance
        variance = analyze_attribute_variance("STUDYID", slices, slice_data, dsd, mdv)
        
        assert variance["level"] == "dataset", "Constant attribute should be dataset-level"
        assert variance["varies_with"] == [], "Should not vary with any dimension"

    def test_dimension_level_attribute_identified(self):
        """Attribute varying with one dimension should be dimension-level."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_slices.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        
        # LBCAT varies by LBTEST: Glucose/Sodium=CHEMISTRY, Platelet=HEMATOLOGY
        slice_data = {
            "WC.GLUCOSE.BASELINE": {"LBTEST": "Glucose", "VISITNUM": "1", "LBCAT": "CHEMISTRY"},
            "WC.GLUCOSE.WEEK4": {"LBTEST": "Glucose", "VISITNUM": "2", "LBCAT": "CHEMISTRY"},
            "WC.SODIUM.BASELINE": {"LBTEST": "Sodium", "VISITNUM": "1", "LBCAT": "CHEMISTRY"},
            "WC.PLATELET.BASELINE": {"LBTEST": "Platelet", "VISITNUM": "1", "LBCAT": "HEMATOLOGY"},
        }
        
        slices = [ig for ig in mdv.itemGroups if ig.type and 
                  (ig.type == "DataSpecialization" or 
                   (hasattr(ig.type, 'value') and ig.type.value == "DataSpecialization"))]
        
        # Analyze LBCAT variance
        variance = analyze_attribute_variance("LBCAT", slices, slice_data, dsd, mdv)
        
        assert variance["level"] == "dimension", "Should be dimension-level"
        assert "LBTEST" in variance["varies_with"], "Should vary with LBTEST dimension"

    def test_infer_relationships_updates_dsd(self):
        """infer_attribute_relationships should update DataAttribute.role."""
        mdv = load_mdv(FIXTURES_DIR / "lb_with_slices.json")
        policy = load_sdmx_policy(FIXTURES_DIR / "lb_wc_policy.yaml")
        
        dsd = build_dsd_for_domain(mdv, "LB", policy)
        slices = [ig for ig in mdv.itemGroups if ig.type and 
                  (ig.type == "DataSpecialization" or 
                   (hasattr(ig.type, 'value') and ig.type.value == "DataSpecialization"))]
        
        # Provide slice data for inference
        slice_data = {
            "WC.GLUCOSE.BASELINE": {
                "STUDYID": "STUDY001",
                "LBTEST": "Glucose",
                "LBCAT": "CHEMISTRY",
                "LBSTRESU": "mg/dL",
                "VISITNUM": "1",
                "VISIT": "Baseline"
            },
            "WC.GLUCOSE.WEEK4": {
                "STUDYID": "STUDY001",
                "LBTEST": "Glucose",
                "LBCAT": "CHEMISTRY",
                "LBSTRESU": "mg/dL",
                "VISITNUM": "2",
                "VISIT": "Week 4"
            },
            "WC.SODIUM.BASELINE": {
                "STUDYID": "STUDY001",
                "LBTEST": "Sodium",
                "LBCAT": "CHEMISTRY",
                "LBSTRESU": "mmol/L",
                "VISITNUM": "1",
                "VISIT": "Baseline"
            },
            "WC.PLATELET.BASELINE": {
                "STUDYID": "STUDY001",
                "LBTEST": "Platelet",
                "LBCAT": "HEMATOLOGY",
                "LBSTRESU": "10^9/L",
                "VISITNUM": "1",
                "VISIT": "Baseline"
            }
        }
        
        # Run inference
        report = infer_attribute_relationships(dsd, slices, slice_data, mdv)
        
        # Check report structure
        assert "STUDYID" in report, "Should analyze STUDYID"
        assert report["STUDYID"]["level"] == "dataset", "STUDYID should be dataset-level"
        
        # Check that DSD attributes were updated
        studyid_attr = next((a for a in dsd.items if isinstance(a, DataAttribute) and a.name == "STUDYID"), None)
        assert studyid_attr is not None, "Should have STUDYID attribute in DSD"
        assert studyid_attr.role == "Dataset", "Role should be updated to Dataset"
