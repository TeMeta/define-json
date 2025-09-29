

# Slot: metadata 


_Root-level ODM metadata including file attributes and study information_





URI: [odm:slot/metadata](https://cdisc.org/odm2/slot/metadata)
Alias: metadata

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |







## Properties

* Range: [ODMMetadata](../classes/ODMMetadata.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:metadata |
| native | odm:metadata |




## LinkML Source

<details>
```yaml
name: metadata
description: Root-level ODM metadata including file attributes and study information
from_schema: https://cdisc.org/define-json
rank: 1000
alias: metadata
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: ODMMetadata
required: true
inlined: true

```
</details>