

# Slot: itemGroups 


_Item groups, containing items, defined in this version of the metadata_





URI: [odm:slot/itemGroups](https://cdisc.org/odm2/slot/itemGroups)
Alias: itemGroups

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |






## Properties

* Range: [ItemGroup](../classes/ItemGroup.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:itemGroups |
| native | odm:itemGroups |




## LinkML Source

<details>
```yaml
name: itemGroups
description: Item groups, containing items, defined in this version of the metadata
from_schema: https://cdisc.org/define-json
rank: 1000
alias: itemGroups
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: ItemGroup
multivalued: true
inlined: true
inlined_as_list: true

```
</details>