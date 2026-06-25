

# Slot: uniqueKey 


_Unordered set of Items whose combined values uniquely identify a record in this dataset (the record key). Each entry is an OID reference to an Item in the items array. Order is not significant for uniqueness — use keySequence for sort order. Splitting uniqueness from sorting resolves the previous overloading of keySequence._





URI: [dds:slot/uniqueKey](https://w3id.org/dds/slot/uniqueKey)
Alias: uniqueKey

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
| self | dds:uniqueKey |
| native | dds:uniqueKey |
| close | odm:ItemRef.KeySequence |




## LinkML Source

<details>
```yaml
name: uniqueKey
description: Unordered set of Items whose combined values uniquely identify a record
  in this dataset (the record key). Each entry is an OID reference to an Item in the
  items array. Order is not significant for uniqueness — use keySequence for sort
  order. Splitting uniqueness from sorting resolves the previous overloading of keySequence.
from_schema: https://w3id.org/dds
close_mappings:
- odm:ItemRef.KeySequence
rank: 1000
alias: uniqueKey
owner: ItemGroup
domain_of:
- ItemGroup
range: Item
multivalued: true

```
</details>