

# Slot: collectionExceptionCondition 


_Condition that defines when collection may be exempted_





URI: [odm:slot/collectionExceptionCondition](https://cdisc.org/odm2/slot/collectionExceptionCondition)
Alias: collectionExceptionCondition

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [IsODMItem](../classes/IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model items, including roles, completion instructions, and implementation notes |  no  |







## Properties

* Range: [Condition](../classes/Condition.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:collectionExceptionCondition |
| native | odm:collectionExceptionCondition |




## LinkML Source

<details>
```yaml
name: collectionExceptionCondition
description: Condition that defines when collection may be exempted
from_schema: https://cdisc.org/define-json
rank: 1000
alias: collectionExceptionCondition
owner: IsODMItem
domain_of:
- IsODMItem
range: Condition

```
</details>