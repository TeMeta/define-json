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
)


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
            if ig.domain == "LB" and ig.type == "DataSpecialization"
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
            if ig.domain == "AE" and ig.type == "DataSpecialization"
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
            if ig.domain == "AE" and ig.type == "DataSpecialization"
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
            type="DataSpecialization",
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
            if ig.domain == "AE" and ig.type == "DataSpecialization"
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
            if ig.domain == "LB" and ig.type == "DataSpecialization"
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
            if ig.domain == "VS" and ig.type == "DataSpecialization"
        ]
        
        # Should be exactly one slice (because WhereClauses are identical after normalisation)
        assert len(vs_slices) == 1, f"Expected 1 slice after normalisation, got {len(vs_slices)}"
        
        # Both VSORRES items should be in the same slice
        # But this might fail if items have different names - let's see
        # Actually both have name="VSORRES" so this will test duplicate detection


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

