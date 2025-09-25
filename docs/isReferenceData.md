

# Slot: isReferenceData 


_Set to Yes if this is a reference item group._





URI: [odm:isReferenceData](https://cdisc.org/odm2/isReferenceData)
Alias: isReferenceData

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:isReferenceData |
| native | odm:isReferenceData |




## LinkML Source

<details>
```yaml
name: isReferenceData
description: Set to Yes if this is a reference item group.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: isReferenceData
owner: ItemGroup
domain_of:
- ItemGroup
range: boolean

```
</details>