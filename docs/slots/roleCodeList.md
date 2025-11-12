

# Slot: roleCodeList 


_Reference to the CodeList that defines the roles for this item_





URI: [odm:slot/roleCodeList](https://cdisc.org/odm2/slot/roleCodeList)
Alias: roleCodeList

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [IsODMItem](../classes/IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model items, including roles, completion instructions, and implementation notes |  no  |







## Properties

* Range: [CodeList](../classes/CodeList.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:roleCodeList |
| native | odm:roleCodeList |




## LinkML Source

<details>
```yaml
name: roleCodeList
description: Reference to the CodeList that defines the roles for this item
from_schema: https://cdisc.org/define-json
rank: 1000
alias: roleCodeList
owner: IsODMItem
domain_of:
- IsODMItem
range: CodeList

```
</details>