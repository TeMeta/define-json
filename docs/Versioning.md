
## Versioning Architecture: Copy-and-Link vs Inheritance

Define-JSON employs a **copy-and-link** versioning model rather than traditional inheritance hierarchies. This architectural choice has profound implications for clinical data management, regulatory compliance, and system maintainability.

### The Copy-and-Link Model

Instead of inheriting from parent versions, each `MetaDataVersion` is a complete, self-contained snapshot that links back to its sources via `wasDerivedFrom` relationships:

```
                    ┌──wasDerivedFrom── CDISC Standard v1.0
                    │
Study ABC v1.3 ─────┼──wasDerivedFrom── Study Template v2.1
                    │
                    └──wasDerivedFrom── Local Extensions
```

Each version contains **complete copies** of all relevant definitions, creating an immutable snapshot with explicit provenance chains.

### Why This Matters for Clinical Data

**Regulatory Compliance**

- **Immutable Audit Trail**: Once created, versions never change - essential for regulatory submissions
- **Complete Context**: Each submission is self-contained with no external dependencies
- **Clear Lineage**: `wasDerivedFrom` provides unambiguous provenance for regulatory review

**Data Integrity**

- **No Cascade Failures**: Changes to standards don't break existing studies
- **Temporal Consistency**: Historical analyses remain reproducible indefinitely
- **Explicit Customisation**: Study-specific modifications are clearly documented

**Operational Benefits**

- **Simplified Queries**: All metadata is local - no complex inheritance resolution
- **Parallel Development**: Teams can work independently without version conflicts
- **Predictable Performance**: No deep inheritance chains to traverse

### Trade-offs Considered

**Storage vs Simplicity**

- **Cost**: More storage required for duplicated definitions
- **Benefit**: Eliminates complex inheritance logic and cascade dependencies
- **Reality**: Storage is cheap; developer time and regulatory risk are expensive

**Propagation vs Isolation**

- **Challenge**: Updates must be explicitly propagated to derived versions
- **Benefit**: Prevents unintended changes from affecting production systems
- **Mitigation**: Tooling can assist with selective update propagation

**Divergence vs Control**

- **Risk**: Versions may diverge over time without careful governance
- **Benefit**: Explicit control over what changes are adopted and when
- **Practice**: Regular review cycles ensure alignment where needed

### Implementation Pattern

This mirrors successful patterns in other domains:

- **Git**: Complete snapshots with parent pointers, not deltas
- **Docker**: Immutable layers with explicit inheritance
- **Blockchain**: Immutable blocks with cryptographic lineage

For clinical data, where **"reproducible forever"** is not just good practice but regulatory requirement, this architecture provides the foundation for trustworthy, auditable data systems.