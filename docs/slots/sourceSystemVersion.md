

# Slot: sourceSystemVersion 


_Version of the source system_





URI: [odm:slot/sourceSystemVersion](https://cdisc.org/odm2/slot/sourceSystemVersion)
Alias: sourceSystemVersion

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file ident... |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:sourceSystemVersion |
| native | odm:sourceSystemVersion |




## LinkML Source

<details>
```yaml
name: sourceSystemVersion
description: Version of the source system
from_schema: https://cdisc.org/define-json
rank: 1000
alias: sourceSystemVersion
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string

```
</details>