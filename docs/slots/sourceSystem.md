

# Slot: sourceSystem 


_Source system that generated the data_





URI: [odm:slot/sourceSystem](https://cdisc.org/odm2/slot/sourceSystem)
Alias: sourceSystem

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
| self | odm:sourceSystem |
| native | odm:sourceSystem |




## LinkML Source

<details>
```yaml
name: sourceSystem
description: Source system that generated the data
from_schema: https://cdisc.org/define-json
rank: 1000
alias: sourceSystem
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string

```
</details>