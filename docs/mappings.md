

# Slot: mappings 


_Coding mappings in this version of the metadata_





URI: [odm:mappings](https://cdisc.org/odm2/mappings)
Alias: mappings

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |







## Properties

* Range: [CodingMapping](CodingMapping.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:mappings |
| native | odm:mappings |




## LinkML Source

<details>
```yaml
name: mappings
description: Coding mappings in this version of the metadata
from_schema: https://cdisc.org/define-json
rank: 1000
alias: mappings
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: CodingMapping
multivalued: true
inlined: true
inlined_as_list: true

```
</details>