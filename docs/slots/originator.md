

# Slot: originator 


_Organization or system that created the ODM file_





URI: [odm:slot/originator](https://cdisc.org/odm2/slot/originator)
Alias: originator

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:originator |
| native | odm:originator |




## LinkML Source

<details>
```yaml
name: originator
description: Organization or system that created the ODM file
from_schema: https://cdisc.org/define-json
rank: 1000
alias: originator
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string

```
</details>