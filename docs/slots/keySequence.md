

# Slot: keySequence 


_Ordered list of Items that define the dataset key structure for sorting and uniqueness. Each entry is an OID reference to an Item in the items array. Order determines sorting precedence, merge operations, and record uniqueness. These are allowed to be null, unlike stricter dataset dimensions or primary keys._





URI: [odm:slot/keySequence](https://cdisc.org/odm2/slot/keySequence)
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


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:keySequence |
| native | odm:keySequence |
| close | odm:ItemRef.KeySequence, sdmx:DimensionDescriptor |




## LinkML Source

<details>
```yaml
name: keySequence
description: Ordered list of Items that define the dataset key structure for sorting
  and uniqueness. Each entry is an OID reference to an Item in the items array. Order
  determines sorting precedence, merge operations, and record uniqueness. These are
  allowed to be null, unlike stricter dataset dimensions or primary keys.
from_schema: https://cdisc.org/define-json
close_mappings:
- odm:ItemRef.KeySequence
- sdmx:DimensionDescriptor
rank: 1000
alias: keySequence
owner: ItemGroup
domain_of:
- ItemGroup
range: Item
multivalued: true
inlined: true
inlined_as_list: true

```
</details>