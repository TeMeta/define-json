

# Slot: roleCodeList 


_Reference to the CodeList that defines the roles for this item_





URI: [dds:slot/roleCodeList](https://w3id.org/dds/slot/roleCodeList)
Alias: roleCodeList

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMItemSerialization](../classes/ODMItemSerialization.md) | A mixin providing ODM/CDISC-specific item attributes meaningful only in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation notes, collection exception predicates, and pre-specified values. Applied by the ODM output generator. Not part of the canonical Item. |  no  |






## Properties

* Range: [CodeList](../classes/CodeList.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:roleCodeList |
| native | dds:roleCodeList |




## LinkML Source

<details>
```yaml
name: roleCodeList
description: Reference to the CodeList that defines the roles for this item
from_schema: https://w3id.org/dds
rank: 1000
alias: roleCodeList
owner: ODMItemSerialization
domain_of:
- ODMItemSerialization
range: CodeList

```
</details>