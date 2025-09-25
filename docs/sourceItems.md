

# Slot: sourceItems 


_Source items for this origin_





URI: [odm:sourceItems](https://cdisc.org/odm2/sourceItems)
Alias: sourceItems

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Origin](Origin.md) | A provenance element that describes the source of data for an item |  no  |







## Properties

* Range: [SourceItem](SourceItem.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:sourceItems |
| native | odm:sourceItems |




## LinkML Source

<details>
```yaml
name: sourceItems
description: Source items for this origin
from_schema: https://cdisc.org/define-json
rank: 1000
alias: sourceItems
owner: Origin
domain_of:
- Origin
range: SourceItem
multivalued: true
inlined: true
inlined_as_list: true

```
</details>