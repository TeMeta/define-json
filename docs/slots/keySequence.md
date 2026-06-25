

# Slot: keySequence 


_Ordered list of Items defining the default sort order for this dataset. Each entry is an OID reference to an Item in the items array; order determines sorting precedence and merge operations. May reference Items that are not part of uniqueKey. Distinct from uniqueKey, which establishes record uniqueness._





URI: [dds:slot/keySequence](https://w3id.org/dds/slot/keySequence)
Alias: keySequence

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |






## Properties

* Range: [Item](../classes/Item.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:keySequence |
| native | dds:keySequence |
| close | sdmx:DimensionDescriptor |




## LinkML Source

<details>
```yaml
name: keySequence
description: Ordered list of Items defining the default sort order for this dataset.
  Each entry is an OID reference to an Item in the items array; order determines sorting
  precedence and merge operations. May reference Items that are not part of uniqueKey.
  Distinct from uniqueKey, which establishes record uniqueness.
from_schema: https://w3id.org/dds
close_mappings:
- sdmx:DimensionDescriptor
rank: 1000
alias: keySequence
owner: ItemGroup
domain_of:
- ItemGroup
range: Item
multivalued: true

```
</details>