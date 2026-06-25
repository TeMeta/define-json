

# Slot: queries 


_Queries raised against metadata and/or data elements in this specification. Each Query references its target element(s) by OID, so the same query can relate to many metadata and data elements (many-to-many)._





URI: [dds:slot/queries](https://w3id.org/dds/slot/queries)
Alias: queries

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [Query](../classes/Query.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:queries |
| native | dds:queries |




## LinkML Source

<details>
```yaml
name: queries
description: Queries raised against metadata and/or data elements in this specification.
  Each Query references its target element(s) by OID, so the same query can relate
  to many metadata and data elements (many-to-many).
from_schema: https://w3id.org/dds
rank: 1000
alias: queries
owner: Specification
domain_of:
- Specification
range: Query
multivalued: true
inlined: true
inlined_as_list: true

```
</details>