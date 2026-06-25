

# Slot: collectionExceptionPredicate 


_Logical predicate defining when data collection for this item may be exempted._





URI: [dds:slot/collectionExceptionPredicate](https://w3id.org/dds/slot/collectionExceptionPredicate)
Alias: collectionExceptionPredicate

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMItemSerialization](../classes/ODMItemSerialization.md) | A mixin providing ODM/CDISC-specific item attributes meaningful only in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation notes, collection exception predicates, and pre-specified values. Applied by the ODM output generator. Not part of the canonical Item. |  no  |






## Properties

* Range: [LogicalPredicate](../classes/LogicalPredicate.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:collectionExceptionPredicate |
| native | dds:collectionExceptionPredicate |




## LinkML Source

<details>
```yaml
name: collectionExceptionPredicate
description: Logical predicate defining when data collection for this item may be
  exempted.
from_schema: https://w3id.org/dds
rank: 1000
alias: collectionExceptionPredicate
owner: ODMItemSerialization
domain_of:
- ODMItemSerialization
range: LogicalPredicate

```
</details>