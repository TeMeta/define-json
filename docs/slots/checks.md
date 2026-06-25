

# Slot: checks 


_Reusable validation checks (e.g. published CORE rules) included in this metadata package. Each Check references the elements it applies to by OID and may cite an external published rule, enabling reuse and loose coupling._





URI: [dds:slot/checks](https://w3id.org/dds/slot/checks)
Alias: checks

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [Check](../classes/Check.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:checks |
| native | dds:checks |




## LinkML Source

<details>
```yaml
name: checks
description: Reusable validation checks (e.g. published CORE rules) included in this
  metadata package. Each Check references the elements it applies to by OID and may
  cite an external published rule, enabling reuse and loose coupling.
from_schema: https://w3id.org/dds
rank: 1000
alias: checks
owner: Specification
domain_of:
- Specification
range: Check
multivalued: true
inlined: true
inlined_as_list: true

```
</details>