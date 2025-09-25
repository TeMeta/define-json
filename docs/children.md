

# Slot: children 


_Child item groups within this item group._





URI: [odm:children](https://cdisc.org/odm2/children)
Alias: children

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |







## Properties

* Range: [ItemGroup](ItemGroup.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:children |
| native | odm:children |




## LinkML Source

<details>
```yaml
name: children
description: Child item groups within this item group.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: children
owner: ItemGroup
domain_of:
- ItemGroup
range: ItemGroup
multivalued: true

```
</details>