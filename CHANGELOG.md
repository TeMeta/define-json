# Changelog

Notable changes to `define.yaml` (the Data Definition Specification LinkML schema). Format loosely
follows [Keep a Changelog](https://keepachangelog.com). The schema is not yet
semver-versioned, so entries are dated.

## [Unreleased] — Queries, reusable checks, key split — 2026-06-25

**Backward-compatible / additive.** New classes/slots/enum only; one slot
repurposed (`keySequence`) with a new sibling added. No existing instances populate
the affected slots. Verified: `gen-linkml` and `linkml-lint` pass.

### Added

- **Class `Query`** (`is_a GovernedElement`, `close_mappings: odm:Query`): a reified,
  externally referenced query linked many-to-many to metadata and/or data elements via
  `about` (non-inlined OID references), with `queryType`, `text`, `status`, `source`.
  Catalogued in the new `MetaDataVersion.queries` collection (#2).
- **Class `Check`** (`is_a GovernedElement`): a reusable validation check (e.g. a
  published CORE rule) linked many-to-many via `appliesTo` (non-inlined), with
  `publishedBy`, `externalReference` (uri/curie), `severity`, and optional
  `expressions`. Catalogued in the new `MetaDataVersion.checks` collection.
  `RangeCheck.implementsCheck` references a `Check` to connect inline checks to the
  reusable rule they implement (#1).
- **Enum `QueryType`** (`Internal`/`External`) for `Query.queryType` (#2).
- **`ItemGroup.uniqueKey`**: unordered set of Items establishing record uniqueness
  (carries the `odm:ItemRef.KeySequence` mapping) (#12).

### Changed

- **`ItemGroup.keySequence`** repurposed to mean *sort order only* (ordered, may
  include non-key Items); uniqueness moved to the new `uniqueKey`. Resolves the prior
  overloading of one slot for sorting + uniqueness + merge (#12).

## [Unreleased] — DTA enablement — 2026-06-24

**Backward-compatible / additive only.** No classes or slots were removed, no new
required fields were added to existing classes, and no inlining was changed on any
slot used by existing instances. Verified: the full define files still load and
validate, and `examples/concept_method_example.json` (the only file using the
concept slots) is unaffected. Net change +209 lines (2562 → 2771).

### Why

Representing a **Data Transfer Agreement (DTA)** exposed three structural gaps:

1. **A DTA could not be serialised as a self-contained artifact.** `ProvisionAgreement`
   existed, but its `provider`/`dataFlow`/`source` were non-inlined references with no
   container reachable from the tree root — so the agreement couldn't hold its own parts.
2. **No agreement-level delivery timing.** Timing existed only on concrete `Dataset`
   reporting periods, not as a transfer schedule on the flow/agreement.
3. **No structured home for legal/governance terms.** `hasPolicy` was untyped, there was
   no `DataConsumer` (asymmetric with `DataProvider`), and confidentiality/permitted-use/
   retention terms were unmodelled.

Design decisions taken (with the user, as a peer): the DTA is a **standalone artifact**
that embeds a **frozen snapshot** of the agreed structure and links to the live spec for
provenance; the canonical concept layer is **referenced** (Registry), not embedded; legal
terms use **ODRL**; the schedule default is a domain-neutral ISO-8601 string so the model
stays **clinical-first but horizontal-ready**.

### Added

- **Prefix `odrl`** (`http://www.w3.org/ns/odrl/2/`). _Reason:_ legal terms are modelled
  with ODRL; the schema already used DPROD/DCAT, which express policy via ODRL.
- **`ProvisionAgreement.hasPolicy`** → `Policy` (multivalued, inlined). _Reason:_ the
  agreement is the legal instrument but previously had nowhere to carry its terms (gap 3).
- **`Dataflow.deliverySchedule`** → `any_of [string, Timing]` (multivalued, inlined).
  _Reason:_ agreement-level transfer cadence (gap 2). Default is an ISO-8601 repeating
  interval string (neutral); `Timing` remains available for clinical anchoring. Concrete
  reporting periods stay on `Dataset` via `IsSdmxDataset.*`.
- **`DataProduct.provisionAgreement`** → `ProvisionAgreement` (multivalued, **not**
  inlined). _Reason:_ lets a data product catalogue the DTAs governing its flows by
  OID/URI, while the DTA stays an independently maintained artifact.
- **Class `DataConsumer`** (`is_a Organization`, `close_mappings: sdmx:DataConsumer`).
  _Reason:_ restores symmetry with `DataProvider`; gives the demand side a typed home
  (`consumesDataFrom`, `provisionAgreements`) (gap 3).
- **Class `Policy`** (`exact_mappings: odrl:Policy`, `close_mappings: dcat:hasPolicy`)
  with `policyType`, `profile`, `assigner`, `assignee`, and `permission`/`prohibition`/
  `obligation` rule lists. _Reason:_ structured legal terms for the DTA (gap 3).
- **Class `Rule`** (`odrl:Rule`) with `action`, `target`, `assigner`/`assignee`,
  `constraint`. _Reason:_ ODRL permission/prohibition/duty semantics.
- **Class `Constraint`** (`odrl:Constraint`) with `leftOperand`/`operator`/`rightOperand`/
  `unit`. _Reason:_ expresses conditions such as `purpose eq "safety-reporting"`.
- **Enum `PolicyType`** (`Set`/`Offer`/`Agreement`, mapped to ODRL). _Reason:_ typed
  `Policy.policyType`; a DTA is an ODRL `Agreement`.
- **Enum `ConstraintOperator`** (`eq`/`neq`/`lt`/`lteq`/`gt`/`gteq`/`isPartOf`/`isA`/
  `isAnyOf`/`isNoneOf`, mapped to ODRL). _Reason:_ typed `Constraint.operator`.

### Changed

- **`ProvisionAgreement.provider`, `.dataFlow`, `.source` → `inlined: true`** and
  **`Dataflow.structure` → `inlined: true`**. _Reason:_ a standalone DTA must be a
  self-contained, signable **snapshot** (gap 1). These slots are not used by existing
  instances, so the change is non-breaking.
- **`ProvisionAgreement.consumer`** `any_of` now includes **`DataConsumer`** (ahead of
  `DataProduct`/`Organization`/`string`). _Reason:_ allow the typed consumer; existing
  string/Organization values remain valid.
- **`Dataset.hasPolicy` and `DataProduct.hasPolicy` → `range: Policy`.** _Reason:_ both
  were untyped (no range); typing them makes governance terms machine-checkable. No
  existing file populated these slots, so no migration is needed.

### Fixed

- **Declared the `ncit` prefix** (`http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#`).
  _Reason:_ `ncit:*` CURIEs were used in enum `meaning`s but the prefix was undeclared
  (#14).
- **`Parameter.required.ifabsent` and `DataStructureDefinition.evolvingStructure.ifabsent`**
  changed from the bare boolean `false` to the string `'False'`. _Reason:_ the metamodel
  types `ifabsent` as string/null, so an unquoted boolean failed validation (#23).
- **`Analysis.analysisMethod`**: moved `any_of` out of the `description` text (it was
  indented under it, so it was inert) and set `range: Method`; the previously referenced
  `AnalysisMethod` class does not exist (#17).
- **Standardised string-type declarations**: added schema-level `default_range: string`
  and removed the 52 redundant explicit `range: string` slot facets. `any_of` members
  (`- range: string`) are retained as they are explicit union alternatives. Semantically
  identical to the prior state, so no instances are affected (#13).

### Notes / follow-ups

- The schema has no `version` field; consider adding one to make changes citable.
- Generated docs under `docs/` are produced from the schema and need a `gen-doc`
  refresh to include the new classes.
- A pinned copy of this schema lives in the `data-definition-dta` skill bundle
  (`reference/define.yaml`) and should be re-synced when the canonical schema changes.
