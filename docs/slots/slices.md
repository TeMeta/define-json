

# Slot: slices 


_Slices are specific subset ItemGroups that belong to, or are used by this ItemGroup_





URI: [odm:slot/slices](https://cdisc.org/odm2/slot/slices)
Alias: slices

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |






## Properties

* Range: [ItemGroup](../classes/ItemGroup.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:slices |
| native | odm:slices |




## LinkML Source

<details>
```yaml
name: slices
description: Slices are specific subset ItemGroups that belong to, or are used by
  this ItemGroup
from_schema: https://cdisc.org/define-json
rank: 1000
alias: slices
owner: ItemGroup
domain_of:
- ItemGroup
range: ItemGroup
multivalued: true
inlined: true
inlined_as_list: true

```
</details>