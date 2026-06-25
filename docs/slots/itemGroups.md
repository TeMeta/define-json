

# Slot: itemGroups 


_Item groups, containing items, defined in this version of the metadata_





URI: [dds:slot/itemGroups](https://w3id.org/dds/slot/itemGroups)
Alias: itemGroups

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [ItemGroup](../classes/ItemGroup.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:itemGroups |
| native | dds:itemGroups |




## LinkML Source

<details>
```yaml
name: itemGroups
description: Item groups, containing items, defined in this version of the metadata
from_schema: https://w3id.org/dds
rank: 1000
alias: itemGroups
owner: Specification
domain_of:
- Specification
range: ItemGroup
multivalued: true
inlined: true
inlined_as_list: true

```
</details>