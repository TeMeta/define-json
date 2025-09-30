

# Slot: fileOID 


_Unique identifier for the ODM file_





URI: [odm:slot/fileOID](https://cdisc.org/odm2/slot/fileOID)
Alias: fileOID

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file ident... |  no  |







## Properties

* Range: [String](../types/String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:fileOID |
| native | odm:fileOID |




## LinkML Source

<details>
```yaml
name: fileOID
description: Unique identifier for the ODM file
from_schema: https://cdisc.org/define-json
rank: 1000
alias: fileOID
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string
required: true

```
</details>