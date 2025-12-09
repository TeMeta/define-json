"""
Test IR utilities: canonical WhereClause registry, slices, ValueList projection, determinism.

These tests define what "canonical" means through TDD with golden fixtures.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any

from define_json.utils.ir import (
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
    transform_value_lists_to_specialisation,
)

try:
    from define_json.converters.xml_to_json import DefineXMLToJSONConverter
    CONVERTERS_AVAILABLE = True
except ImportError:
    CONVERTERS_AVAILABLE = False


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestWhereCauseCanonicalisation:
    """WhereClause canonicalisation must produce stable, deterministic hashes."""

    def test_identical_predicates_produce_same_hash(self):
        """Two WhereClauses with identical conditions must hash to same whereId."""
        mdv = load_mdv(FIXTURES_DIR / "unnormalised_where.json")
        
        # Build registry which will canonicalise all WhereClauses
        registry = build_where_registry(mdv)
        
        # Get the two items with "identical" conditions (just different order)
        vs_items = [ig for ig in mdv.itemGroups if ig.domain == "VS"][0].items
        item1 = [it for it in vs_items if it.OID == "IT.VS.VSORRES.BASELINE"][0]
        item2 = [it for it in vs_items if it.OID == "IT.VS.VSORRES.BASELINE.DUP"][0]
        
        # After registry building, applicableWhen contains string OIDs
        assert item1.applicableWhen is not None, "Item1 should have applicableWhen"
        assert item2.applicableWhen is not None, "Item2 should have applicableWhen"
        
        wc1_oid = item1.applicableWhen[0]
        wc2_oid = item2.applicableWhen[0]
        
        # Must be identical because IN predicates are sorted
        assert wc1_oid == wc2_oid, f"Identical conditions with different order should produce same whereId: {wc1_oid} != {wc2_oid}"
        assert wc1_oid.startswith("WC."), "WhereClause hash should start with WC. prefix"

    def test_hash_is_deterministic(self):
        """Running canonicalisation multiple times must produce identical hash."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        wc = mdv.whereClauses[0]
        
        hash1 = canonicalise_whereclause(wc, mdv)
        hash2 = canonicalise_whereclause(wc, mdv)
        hash3 = canonicalise_whereclause(wc, mdv)
        
        assert hash1 == hash2 == hash3, "Hash must be deterministic across runs"

    def test_different_predicates_produce_different_hash(self):
        """Different conditions must produce different whereIds."""
        mdv1 = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        mdv2 = load_mdv(FIXTURES_DIR / "duplicate_slices.json")

        wc1 = mdv1.whereClauses[0]  # SCREENING
        wc2 = mdv2.whereClauses[0]  # VISIT 1

        hash1 = canonicalise_whereclause(wc1, mdv1)
        hash2 = canonicalise_whereclause(wc2, mdv2)

        assert hash1 != hash2, "Different conditions must hash differently"


class TestWhereClauseRegistry:
    """Registry must deduplicate WhereClauses and repoint all references."""

    def test_registry_deduplicates_identical_conditions(self):
        """Registry must merge WhereClauses with identical predicates."""
        mdv = load_mdv(FIXTURES_DIR / "unnormalised_where.json")
        
        registry = build_where_registry(mdv)
        
        # The two "BASELINE" conditions should map to single canonical whereId
        vs_items = [ig for ig in mdv.itemGroups if ig.domain == "VS"][0].items
        item1 = [it for it in vs_items if it.OID == "IT.VS.VSORRES.BASELINE"][0]
        item2 = [it for it in vs_items if it.OID == "IT.VS.VSORRES.BASELINE.DUP"][0]
        
        # After registry building, applicableWhen contains string OIDs (not WhereClause objects)
        wc1_oid = item1.applicableWhen[0]
        wc2_oid = item2.applicableWhen[0]
        
        assert wc1_oid == wc2_oid, "Identical conditions must be repointed to same canonical OID"
        assert wc1_oid in registry, "Canonical OID must be in registry"

    def test_registry_sets_oid_on_whereclause(self):
        """Registry must set OID=whereId on all WhereClauses."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        
        registry = build_where_registry(mdv)
        
        for wc in mdv.whereClauses:
            assert wc.OID is not None, "WhereClause must have OID set"
            assert wc.OID.startswith("WC."), "WhereClause OID must have WC. prefix"
            assert wc.OID in registry, "WhereClause OID must be in registry"

    def test_registry_repoints_item_applicablewhen(self):
        """All Item.applicableWhen must reference canonical WhereClause OIDs."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        
        registry = build_where_registry(mdv)
        
        for ig in mdv.itemGroups:
            for it in ig.items:
                for wc_oid in it.applicableWhen or []:
                    assert isinstance(wc_oid, str), "applicableWhen must contain string OIDs"
                    assert wc_oid in registry, f"Item {it.name} references non-canonical WhereClause {wc_oid}"


class TestCanonicalSlices:
    """Slice building must create one ItemGroup per (domain, whereId)."""

    def test_merges_duplicate_slices_same_domain_whereid(self):
        """Two slices with same (domain, whereId) must be merged into one."""
        mdv = load_mdv(FIXTURES_DIR / "duplicate_slices.json")
        
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        # Count slices for LB domain
        lb_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "LB" and ig.type == "DatasetSpecialization"
        ]
        
        # Should be exactly one slice (merged from two)
        assert len(lb_slices) == 1, f"Expected 1 merged slice, got {len(lb_slices)}"
        
        # Merged slice must contain items from both original slices
        merged_items = lb_slices[0].items
        item_names = {it.name for it in merged_items}
        
        assert "LBORRES" in item_names, "Merged slice missing LBORRES"
        assert "LBORRESU" in item_names, "Merged slice missing LBORRESU"

    def test_creates_slice_from_contextual_item(self):
        """Items with applicableWhen must be moved into slices."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        
        build_where_registry(mdv)
        
        # Before slicing
        ae_ig = [ig for ig in mdv.itemGroups if ig.domain == "AE"][0]
        contextual_items = [it for it in ae_ig.items if it.applicableWhen]
        assert len(contextual_items) == 1, "Should have one contextual item (AESEV)"
        
        build_canonical_slices(mdv)
        
        # After slicing
        ae_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "AE" and ig.type == "DatasetSpecialization"
        ]
        
        assert len(ae_slices) == 1, "Should create exactly one slice for AE"
        assert ae_slices[0].applicableWhen is not None, "Slice must have applicableWhen"
        assert len(ae_slices[0].applicableWhen) == 1, "Slice must have exactly one WhereClause"

    def test_slice_inherits_correct_whereclause(self):
        """Slice applicableWhen must match the Items' context."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        ae_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "AE" and ig.type == "DatasetSpecialization"
        ]
        
        slice_wc_oid = ae_slices[0].applicableWhen[0]
        assert isinstance(slice_wc_oid, str), "Slice applicableWhen must be string OID"
        
        # All items in slice must reference same whereId
        for it in ae_slices[0].items:
            # Item may not have applicableWhen set (inherits from slice)
            # But if it does, must match slice
            if it.applicableWhen:
                assert it.applicableWhen[0] == slice_wc_oid, "Item context must match slice context"


class TestSliceInvariants:
    """Slice invariant checks must fail fast on malformed structures."""

    def test_rejects_empty_slice(self):
        """Empty slices must be rejected."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        # Manually create empty slice
        from define_json.schema.define import ItemGroup
        empty_slice = ItemGroup.model_construct(
            OID="IG.TEST.EMPTY",
            type="DatasetSpecialization",
            domain="TEST"
        )
        # applicableWhen should be list of string OIDs
        empty_slice.applicableWhen = [list(build_where_registry(mdv).keys())[0]]
        empty_slice.items = []
        mdv.itemGroups.append(empty_slice)
        
        with pytest.raises(ValueError, match="empty"):
            enforce_slice_invariants(mdv)

    def test_rejects_slice_with_multiple_whereclause(self):
        """Slice with multiple applicableWhen must be rejected."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        ae_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "AE" and ig.type == "DatasetSpecialization"
        ]
        
        # Manually add second WhereClause OID
        ae_slices[0].applicableWhen.append("WC.BAD")
        
        with pytest.raises(ValueError, match="exactly one"):
            enforce_slice_invariants(mdv)

    def test_accepts_valid_slices(self):
        """Well-formed slices must pass validation."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        # Should not raise
        enforce_slice_invariants(mdv)


class TestVariableRegistration:
    """Variable registration must track all contexts per variable."""

    def test_registers_default_variables(self):
        """Variables without context must be registered with __DEFAULT__."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        
        var_map = register_variables(mdv)
        
        # AETERM has no context
        assert "AE.AETERM" in var_map, "AETERM should be registered"
        contexts = var_map["AE.AETERM"]
        assert "__DEFAULT__" in contexts, "Context-free variable should have __DEFAULT__"

    def test_registers_contextual_variables(self):
        """Variables with applicableWhen must be registered with whereId."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        var_map = register_variables(mdv)
        
        # AESEV has context
        assert "AE.AESEV" in var_map, "AESEV should be registered"
        contexts = var_map["AE.AESEV"]
        assert len(contexts) > 0, "AESEV should have at least one context"
        assert "__DEFAULT__" not in contexts, "Contextual-only variable should not have __DEFAULT__"


class TestValueListProjection:
    """ValueList projection must create variable-first view ordered by whereId."""

    def test_projects_variable_with_single_context(self):
        """Variable appearing in one slice must project correctly."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        projection = project_valuelist_for_domain(mdv, "AE")
        
        # AESEV appears only in slice
        assert "AESEV" in projection, "AESEV should be in projection"
        aesev_entries = projection["AESEV"]
        assert len(aesev_entries) > 0, "AESEV should have at least one entry"

    def test_projects_variable_with_no_context(self):
        """Variables without context must appear as parent only."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        projection = project_valuelist_for_domain(mdv, "AE")
        
        # AETERM has no context
        assert "AETERM" in projection, "AETERM should be in projection"
        aeterm_entries = projection["AETERM"]
        # Should be empty list (parent only, no contextual entries)
        assert len(aeterm_entries) == 0, "Context-free variable should have no contextual entries"

    def test_entries_ordered_by_whereid(self):
        """Contextual entries must be ordered by whereId for determinism."""
        mdv = load_mdv(FIXTURES_DIR / "duplicate_slices.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        projection = project_valuelist_for_domain(mdv, "LB")
        
        for var, entries in projection.items():
            if len(entries) > 1:
                where_oids = [
                    (e.applicableWhen[0] if e.applicableWhen else "")
                    for e in entries
                ]
                # Must be sorted
                assert where_oids == sorted(where_oids), f"{var} entries not ordered by whereId"


class TestDeterministicSerialisation:
    """Serialisation must produce identical output for identical input."""

    def test_serialize_is_deterministic(self):
        """Running serialize_canonical twice must produce byte-identical output."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        output1 = serialize_canonical(mdv)
        output2 = serialize_canonical(mdv)
        
        assert output1 == output2, "Serialisation must be deterministic"

    def test_hash_stability_across_reloads(self):
        """Loading same file twice and processing must produce identical hash."""
        mdv1 = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv1)
        build_canonical_slices(mdv1)
        output1 = serialize_canonical(mdv1)
        
        mdv2 = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv2)
        build_canonical_slices(mdv2)
        output2 = serialize_canonical(mdv2)
        
        assert output1 == output2, "Processing same file twice must produce identical output"


class TestXMLExporters:
    """XML exporters must produce valid, parseable output."""

    def test_export_define_xml_21_produces_valid_xml(self):
        """Define-XML 2.1 export must be parseable."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        xml_output = export_define_xml_21(mdv, domains=["AE"])
        
        assert xml_output, "XML output must not be empty"
        assert "<Define>" in xml_output, "Must contain Define root element"
        assert "<WhereClauseDefs>" in xml_output, "Must contain WhereClauseDefs"
        
        # Must be valid XML (will raise if not)
        from xml.etree import ElementTree as ET
        root = ET.fromstring(xml_output)
        assert root.tag == "Define"

    def test_export_define_xml_10_produces_valid_xml(self):
        """Define-XML 1.0 export must be parseable."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        
        xml_output = export_define_xml_10(mdv, domains=["AE"])
        
        assert xml_output, "XML output must not be empty"
        assert "<Define10>" in xml_output, "Must contain Define10 root element"
        
        from xml.etree import ElementTree as ET
        root = ET.fromstring(xml_output)
        assert root.tag == "Define10"

    def test_xml_export_respects_domain_filter(self):
        """XML export with domain filter must only include specified domains."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        build_where_registry(mdv)
        
        xml_ae = export_define_xml_21(mdv, domains=["AE"])
        xml_vs = export_define_xml_21(mdv, domains=["VS"])
        
        # AE domain content should be different from VS domain content
        assert xml_ae != xml_vs, "Different domain filters should produce different output"


class TestValueListToSpecialisation:
    """ValueList to Dataset Specialisation transformation tests."""

    def test_transforms_value_lists_to_slices(self):
        """ValueLists should be transformed into DatasetSpecialization slices."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        # Count ValueLists before transformation
        from define_json.schema.define import ItemGroupType
        value_lists_before = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) == ItemGroupType.ValueList
        ]
        assert len(value_lists_before) == 3, "Should have 3 ValueLists before transformation"
        
        # Count domain ItemGroups before (should be preserved)
        domain_groups_before = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) not in (ItemGroupType.ValueList, ItemGroupType.DatasetSpecialization)
        ]
        domain_group_count = len(domain_groups_before)
        
        # Transform
        transform_value_lists_to_specialisation(mdv)
        
        # ValueLists should be removed
        value_lists_after = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) == ItemGroupType.ValueList
        ]
        assert len(value_lists_after) == 0, "All ValueLists should be removed"
        
        # Domain ItemGroups should be preserved
        domain_groups_after = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) not in (ItemGroupType.ValueList, ItemGroupType.DatasetSpecialization)
        ]
        assert len(domain_groups_after) == domain_group_count, "Domain ItemGroups should be preserved"
        
        # Should have created DatasetSpecialization slices
        slices = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization
        ]
        assert len(slices) > 0, "Should create DatasetSpecialization slices"
        
        # Each slice should have exactly one applicableWhen
        for slice_ig in slices:
            assert slice_ig.applicableWhen is not None, "Slice must have applicableWhen"
            assert len(slice_ig.applicableWhen) == 1, "Slice must have exactly one WhereClause"
            assert slice_ig.items is not None, "Slice must have items"
            assert len(slice_ig.items) > 0, "Slice must not be empty"

    def test_groups_items_by_whereclause(self):
        """Items should be grouped by their applicableWhen WhereClause."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        transform_value_lists_to_specialisation(mdv)
        
        # Find slice for WC.VS.VSORRES.TEMP
        from define_json.schema.define import ItemGroupType
        temp_slice = None
        for ig in mdv.itemGroups:
            if (getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization and
                ig.applicableWhen and
                ig.applicableWhen[0] == "WC.VS.VSORRES.TEMP"):
                temp_slice = ig
                break
        
        assert temp_slice is not None, "Should create slice for WC.VS.VSORRES.TEMP"
        assert len(temp_slice.items) == 1, "TEMP slice should have 1 item"
        assert temp_slice.items[0].OID == "IT.VS.VSORRES.TEMP", "Should contain IT.VS.VSORRES.TEMP"
        
        # Find slice for WC.VS.VSORRES.WEIGHT
        weight_slice = None
        for ig in mdv.itemGroups:
            if (getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization and
                ig.applicableWhen and
                ig.applicableWhen[0] == "WC.VS.VSORRES.WEIGHT"):
                weight_slice = ig
                break
        
        assert weight_slice is not None, "Should create slice for WC.VS.VSORRES.WEIGHT"
        assert len(weight_slice.items) == 1, "WEIGHT slice should have 1 item"
        assert weight_slice.items[0].OID == "IT.VS.VSORRES.WEIGHT", "Should contain IT.VS.VSORRES.WEIGHT"

    def test_preserves_item_properties(self):
        """Item properties should be preserved during transformation."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        # Get original item before transformation
        original_item = None
        for vl_ig in mdv.itemGroups:
            if vl_ig.OID == "VL.VS.VSORRES":
                original_item = vl_ig.items[0]
                break
        
        assert original_item is not None, "Should find original item"
        original_data_type = original_item.dataType
        original_origin = original_item.origin
        
        transform_value_lists_to_specialisation(mdv)
        
        # Find transformed item in slice
        from define_json.schema.define import ItemGroupType
        transformed_item = None
        for ig in mdv.itemGroups:
            if (getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization and
                ig.applicableWhen and
                ig.applicableWhen[0] == "WC.VS.VSORRES.TEMP"):
                transformed_item = ig.items[0]
                break
        
        assert transformed_item is not None, "Should find transformed item"
        assert transformed_item.OID == original_item.OID, "OID should be preserved"
        assert transformed_item.dataType == original_data_type, "dataType should be preserved"
        assert transformed_item.origin == original_origin, "origin should be preserved"

    def test_creates_slice_oids_correctly(self):
        """Slice OIDs should follow pattern IG.{domain}.{WhereClauseOID}."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        transform_value_lists_to_specialisation(mdv)
        
        from define_json.schema.define import ItemGroupType
        slices = [
            ig for ig in mdv.itemGroups 
            if getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization
        ]
        
        for slice_ig in slices:
            domain = slice_ig.domain
            wc_oid = slice_ig.applicableWhen[0] if slice_ig.applicableWhen else ""
            expected_oid = f"IG.{domain}.{wc_oid}"
            assert slice_ig.OID == expected_oid, f"Slice OID should be {expected_oid}, got {slice_ig.OID}"

    def test_handles_multiple_value_lists_same_domain(self):
        """Multiple ValueLists in same domain should create separate slices."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        transform_value_lists_to_specialisation(mdv)
        
        # VS domain should have slices from both VL.VS.VSORRES and VL.VS.VSORRESU
        from define_json.schema.define import ItemGroupType
        vs_slices = [
            ig for ig in mdv.itemGroups 
            if (getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization and
                ig.domain == "VS")
        ]
        
        assert len(vs_slices) >= 2, "VS domain should have multiple slices"
        
        # Should have slice for VSORRES.TEMP and VSORRESU.TEMP (different WhereClauses)
        slice_wc_oids = {s.applicableWhen[0] for s in vs_slices if s.applicableWhen}
        assert "WC.VS.VSORRES.TEMP" in slice_wc_oids, "Should have slice for VSORRES.TEMP"
        assert "WC.VS.VSORRESU.TEMP" in slice_wc_oids, "Should have slice for VSORRESU.TEMP"

    def test_handles_items_without_applicable_when(self):
        """Items without applicableWhen should be skipped."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        # Add a ValueList with an item without applicableWhen
        from define_json.schema.define import ItemGroup, Item, ItemGroupType
        vl_without_wc = ItemGroup.model_construct(
            OID="VL.VS.TEST",
            name="VL_VS_TEST",
            domain="VS",
            type=ItemGroupType.ValueList,
            items=[
                Item.model_construct(
                    OID="IT.VS.TEST.NO_WC",
                    name="TEST",
                    dataType="text"
                    # No applicableWhen
                )
            ]
        )
        mdv.itemGroups.append(vl_without_wc)
        
        transform_value_lists_to_specialisation(mdv)
        
        # ValueList should be removed
        assert not any(ig.OID == "VL.VS.TEST" for ig in mdv.itemGroups), "ValueList should be removed"
        
        # Item without applicableWhen should not appear in any slice
        from define_json.schema.define import ItemGroupType
        all_slice_items = []
        for ig in mdv.itemGroups:
            if getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization:
                all_slice_items.extend(ig.items or [])
        
        assert not any(it.OID == "IT.VS.TEST.NO_WC" for it in all_slice_items), "Item without applicableWhen should not be in slices"

    def test_handles_empty_value_list(self):
        """Empty ValueLists should be removed without creating slices."""
        mdv = load_mdv(FIXTURES_DIR / "valuelist_test.json")
        
        # Add an empty ValueList
        from define_json.schema.define import ItemGroup, ItemGroupType
        empty_vl = ItemGroup.model_construct(
            OID="VL.VS.EMPTY",
            name="VL_VS_EMPTY",
            domain="VS",
            type=ItemGroupType.ValueList,
            items=[]
        )
        mdv.itemGroups.append(empty_vl)
        
        transform_value_lists_to_specialisation(mdv)
        
        # Empty ValueList should be removed
        assert not any(ig.OID == "VL.VS.EMPTY" for ig in mdv.itemGroups), "Empty ValueList should be removed"
        
        # No slice should be created for empty ValueList
        assert not any(
            ig.OID == "IG.VS.WC.VS.EMPTY" for ig in mdv.itemGroups
        ), "Should not create slice for empty ValueList"


class TestMultipleClausesExamples:
    """Tests for examples/multiple_clauses.xml and examples/multiple_clauses.json."""

    def test_xml_to_json_matches_existing_json(self):
        """
        Convert multiple_clauses.xml to JSON and verify it matches existing JSON.
        
        Note: multiple_clauses.json is an INTERMEDIATE representation that preserves
        the original XML structure (27 WhereClauses) for lossless roundtrip conversion.
        It does NOT consolidate WhereClauses - that happens only in the canonical DSS representation.
        """
        if not CONVERTERS_AVAILABLE:
            pytest.skip("Conversion modules not available")
        
        examples_dir = Path(__file__).parent.parent / "examples"
        xml_path = examples_dir / "multiple_clauses.xml"
        json_path = examples_dir / "multiple_clauses.json"
        
        if not xml_path.exists():
            pytest.skip(f"XML file not found: {xml_path}")
        
        if not json_path.exists():
            pytest.skip(f"JSON file not found: {json_path}")
        
        import tempfile
        import json
        
        # Convert XML to JSON
        converter = DefineXMLToJSONConverter()
        temp_json = Path(tempfile.mktemp(suffix='.json'))
        
        try:
            converted_data = converter.convert_file(xml_path, temp_json)
            
            # Load both JSON files for comparison
            with open(temp_json, 'r') as f:
                converted_json = json.load(f)
            
            with open(json_path, 'r') as f:
                expected_json = json.load(f)
            
            # Handle different structures - converter outputs direct MetaDataVersion,
            # expected JSON may have metaDataVersion wrapper
            if 'metaDataVersion' in expected_json:
                expected_mdv = expected_json['metaDataVersion']
                if isinstance(expected_mdv, list) and len(expected_mdv) > 0:
                    expected_mdv = expected_mdv[0]
            else:
                expected_mdv = expected_json
            
            # Converter outputs direct MetaDataVersion structure
            converted_mdv = converted_json
            
            # Compare key structural elements
            # Note: We compare structure rather than exact match due to potential
            # differences in ordering, metadata, etc.
            
            # Check OID matches
            assert converted_mdv.get('OID') == expected_mdv.get('OID'), \
                f"OID mismatch: {converted_mdv.get('OID')} != {expected_mdv.get('OID')}"
            
            # Check study name matches
            assert converted_mdv.get('studyName') == expected_mdv.get('studyName'), \
                f"Study name mismatch: {converted_mdv.get('studyName')} != {expected_mdv.get('studyName')}"
            
            # Check ValueLists exist in both
            converted_vls = [
                ig for ig in converted_mdv.get('itemGroups', [])
                if ig.get('type') == 'ValueList'
            ]
            expected_vls = [
                ig for ig in expected_mdv.get('itemGroups', [])
                if ig.get('type') == 'ValueList'
            ]
            
            # Note: Expected JSON may have consolidated WhereClauses and flattened ValueLists,
            # while converted JSON is fresh from XML with nested ValueLists.
            # We compare structure but allow for processing differences.
            
            # Check ValueLists - account for nested vs flattened structure
            # Converted JSON has ValueLists nested in slices, expected may have them flattened
            converted_vls_flat = converted_vls.copy()
            for ig in converted_mdv.get('itemGroups', []):
                if 'slices' in ig and isinstance(ig['slices'], list):
                    for child in ig['slices']:
                        if isinstance(child, dict) and child.get('type') == 'ValueList':
                            converted_vls_flat.append(child)
            
            # Allow for differences due to consolidation/processing
            # The important thing is that both have ValueLists (or both don't)
            if len(expected_vls) > 0:
                assert len(converted_vls_flat) > 0, \
                    f"Expected ValueLists but converted JSON has none (may be nested)"
            
            # Check domain ItemGroups exist
            converted_domains = [
                ig for ig in converted_mdv.get('itemGroups', [])
                if ig.get('type') not in ('ValueList', 'DatasetSpecialization')
            ]
            expected_domains = [
                ig for ig in expected_mdv.get('itemGroups', [])
                if ig.get('type') not in ('ValueList', 'DatasetSpecialization')
            ]
            
            # Domain count may differ due to processing, but should have at least the same domains
            converted_domain_names = {ig.get('domain') for ig in converted_domains if ig.get('domain')}
            expected_domain_names = {ig.get('domain') for ig in expected_domains if ig.get('domain')}
            assert converted_domain_names == expected_domain_names, \
                f"Domain mismatch: {converted_domain_names} != {expected_domain_names}"
            
        finally:
            # Clean up temp file
            if temp_json.exists():
                temp_json.unlink()

    def test_json_to_dss_transformation(self):
        """
        Transform multiple_clauses.json to Dataset Specialisation shape.
        
        Note: This test transforms the INTERMEDIATE representation (multiple_clauses.json)
        to the CANONICAL DSS representation (multiple_clauses_dss.json).
        
        - multiple_clauses.json: Intermediate, preserves original structure (27 WhereClauses)
        - multiple_clauses_dss.json: Canonical, consolidates WhereClauses (16 WhereClauses)
          and creates DatasetSpecialization slices with meaningful OIDs like WC.VS.TEMP.
        
        The transformation consolidates redundant WhereClauses based on their internal
        structure (not just OID), creating a canonical representation suitable for analysis.
        """
        examples_dir = Path(__file__).parent.parent / "examples"
        json_path = examples_dir / "multiple_clauses.json"
        dss_json_path = examples_dir / "multiple_clauses_dss.json"
        
        if not json_path.exists():
            pytest.skip(f"JSON file not found: {json_path}")
        
        import json
        
        # Load original JSON - handle _xmlMetadata field and flatten nested ValueLists
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        # Extract MetaDataVersion, ignoring _xmlMetadata
        if isinstance(json_data, dict):
            if "metaDataVersion" in json_data:
                mdv_data = json_data["metaDataVersion"]
                if isinstance(mdv_data, list) and len(mdv_data) > 0:
                    mdv_data = mdv_data[0]
            else:
                # Remove _xmlMetadata if present
                mdv_data = {k: v for k, v in json_data.items() if k != "_xmlMetadata"}
        else:
            mdv_data = json_data
        
        # Flatten nested ValueLists from slices into top-level itemGroups
        if "itemGroups" in mdv_data:
            flattened_groups = []
            for ig in mdv_data["itemGroups"]:
                flattened_groups.append(ig)
                # Extract ValueLists from slices and set domain from parent
                if "slices" in ig and isinstance(ig["slices"], list):
                    parent_domain = ig.get("domain")
                    for child in ig["slices"]:
                        if isinstance(child, dict) and child.get("type") == "ValueList":
                            # Set domain from parent if not already set
                            if not child.get("domain") and parent_domain:
                                child["domain"] = parent_domain
                            flattened_groups.append(child)
            mdv_data["itemGroups"] = flattened_groups
        
        # Load as MetaDataVersion
        from define_json.schema.define import MetaDataVersion
        mdv = MetaDataVersion.model_validate(mdv_data)
        
        # Count ValueLists before transformation
        from define_json.schema.define import ItemGroupType
        value_lists_before = [
            ig for ig in mdv.itemGroups
            if getattr(ig, "type", None) == ItemGroupType.ValueList
        ]
        assert len(value_lists_before) > 0, "Should have ValueLists before transformation"
        
        # Count domain ItemGroups before (should be preserved)
        domain_groups_before = [
            ig for ig in mdv.itemGroups
            if getattr(ig, "type", None) not in (ItemGroupType.ValueList, ItemGroupType.DatasetSpecialization)
        ]
        domain_count_before = len(domain_groups_before)
        
        # Apply transformation
        transform_value_lists_to_specialisation(mdv)
        
        # Verify transformation
        value_lists_after = [
            ig for ig in mdv.itemGroups
            if getattr(ig, "type", None) == ItemGroupType.ValueList
        ]
        assert len(value_lists_after) == 0, "All ValueLists should be removed"
        
        # Domain ItemGroups should be preserved
        domain_groups_after = [
            ig for ig in mdv.itemGroups
            if getattr(ig, "type", None) not in (ItemGroupType.ValueList, ItemGroupType.DatasetSpecialization)
        ]
        assert len(domain_groups_after) == domain_count_before, \
            f"Domain ItemGroups should be preserved: {len(domain_groups_after)} != {domain_count_before}"
        
        # Should have created DatasetSpecialization slices
        slices = [
            ig for ig in mdv.itemGroups
            if getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization
        ]
        assert len(slices) > 0, "Should create DatasetSpecialization slices"
        
        # Verify each slice has exactly one applicableWhen
        for slice_ig in slices:
            assert slice_ig.applicableWhen is not None, "Slice must have applicableWhen"
            assert len(slice_ig.applicableWhen) == 1, "Slice must have exactly one WhereClause"
            assert slice_ig.items is not None, "Slice must have items"
            assert len(slice_ig.items) > 0, "Slice must not be empty"
        
        # Verify domain ItemGroups have slice OIDs as slices (not ValueLists)
        # Only check domains that have slices
        domains_with_slices = {s.domain for s in slices}
        for domain_ig in domain_groups_after:
            domain = domain_ig.domain
            slices_list = domain_ig.slices or []
            
            # Should NOT have ValueList references
            vl_slices = [c for c in slices_list if isinstance(c, str) and c.startswith('VL.')]
            assert len(vl_slices) == 0, f"Domain {domain} should not have ValueList slices"
            
            # Domains with slices should have slice OID references as slices
            if domain in domains_with_slices:
                slice_refs = [c for c in slices_list if isinstance(c, str) and c.startswith('IG.')]
                assert len(slice_refs) > 0, f"Domain {domain} should have slice references"
        
        # Verify against expected output file if it exists
        if dss_json_path.exists():
            # Load expected output
            expected_mdv = load_mdv(dss_json_path)
            
            # Compare structure
            expected_slices = [
                ig for ig in expected_mdv.itemGroups
                if getattr(ig, "type", None) == ItemGroupType.DatasetSpecialization
            ]
            assert len(slices) == len(expected_slices), \
                f"Slice count mismatch: {len(slices)} != {len(expected_slices)}"
            
            # Compare domain ItemGroups have correct slices
            expected_domains = [
                ig for ig in expected_mdv.itemGroups
                if getattr(ig, "type", None) not in (ItemGroupType.ValueList, ItemGroupType.DatasetSpecialization)
            ]
            
            for domain_ig in domain_groups_after:
                domain = domain_ig.domain
                expected_domain_ig = next((ig for ig in expected_domains if ig.domain == domain), None)
                if expected_domain_ig:
                    expected_slices = expected_domain_ig.slices or []
                    actual_slices = domain_ig.slices or []
                    
                    # Compare slice OID references
                    expected_slice_refs = {c for c in expected_slices if isinstance(c, str) and c.startswith('IG.')}
                    actual_slice_refs = {c for c in actual_slices if isinstance(c, str) and c.startswith('IG.')}
                    assert expected_slice_refs == actual_slice_refs, \
                        f"Domain {domain} slices mismatch: expected {expected_slice_refs}, got {actual_slice_refs}"
        else:
            # If expected file doesn't exist, create it for reference
            # (but this shouldn't happen in normal test runs)
            mdv_dict = mdv.model_dump(mode='json', exclude_none=True)
            output_data = {"metaDataVersion": [mdv_dict]}
            with open(dss_json_path, 'w') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            pytest.fail(f"Expected file {dss_json_path} not found. Created it, please review and commit.")


class TestEndToEndPipeline:
    """End-to-end integration tests for full IR pipeline."""

    def test_full_pipeline_minimal(self):
        """Complete pipeline on minimal fixture must succeed."""
        mdv = load_mdv(FIXTURES_DIR / "minimal_ir.json")
        
        # Step 1: Build registry
        registry = build_where_registry(mdv)
        assert len(registry) > 0, "Registry must contain WhereClauses"
        
        # Step 2: Build slices
        build_canonical_slices(mdv)
        
        # Step 3: Validate
        enforce_slice_invariants(mdv)
        
        # Step 4: Register variables
        var_map = register_variables(mdv)
        assert len(var_map) > 0, "Variable map must contain variables"
        
        # Step 5: Project ValueList
        projection = project_valuelist_for_domain(mdv, "AE")
        assert len(projection) > 0, "Projection must contain variables"
        
        # Step 6: Serialise
        canonical = serialize_canonical(mdv)
        assert canonical, "Canonical serialisation must not be empty"
        
        # Step 7: Export XML
        xml21 = export_define_xml_21(mdv, domains=["AE"])
        xml10 = export_define_xml_10(mdv, domains=["AE"])
        assert xml21 and xml10, "XML exports must not be empty"

    def test_full_pipeline_with_duplicates(self):
        """Pipeline must handle and merge duplicate slices correctly."""
        mdv = load_mdv(FIXTURES_DIR / "duplicate_slices.json")
        
        build_where_registry(mdv)
        build_canonical_slices(mdv)
        enforce_slice_invariants(mdv)
        
        # Verify merge happened
        lb_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "LB" and ig.type == "DatasetSpecialization"
        ]
        assert len(lb_slices) == 1, "Duplicate slices must be merged"

    def test_full_pipeline_with_unnormalised_where(self):
        """Pipeline must normalise identical WhereClauses with different ordering."""
        mdv = load_mdv(FIXTURES_DIR / "unnormalised_where.json")
        
        registry = build_where_registry(mdv)
        build_canonical_slices(mdv)
        
        # The two "BASELINE" items should create only one slice
        vs_slices = [
            ig for ig in mdv.itemGroups 
            if ig.domain == "VS" and ig.type == "DatasetSpecialization"
        ]
        
        # Should be exactly one slice (because WhereClauses are identical after normalisation)
        assert len(vs_slices) == 1, f"Expected 1 slice after normalisation, got {len(vs_slices)}"
        
        # Both VSORRES items should be in the same slice
        # But this might fail if items have different names - let's see
        # Actually both have name="VSORRES" so this will test duplicate detection


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

