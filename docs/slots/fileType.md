

# Slot: fileType 


_Type of ODM file (e.g., Snapshot, Transactional)_





URI: [odm:slot/fileType](https://cdisc.org/odm2/slot/fileType)
Alias: fileType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information |  no  |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |







## Properties

* Range: [String](../types/String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:fileType |
| native | odm:fileType |




## LinkML Source

<details>
```yaml
name: fileType
description: Type of ODM file (e.g., Snapshot, Transactional)
from_schema: https://cdisc.org/define-json
rank: 1000
alias: fileType
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string
required: true

```
</details>