

# Slot: asOfDateTime 


_Date and time when the data snapshot was taken_





URI: [odm:slot/asOfDateTime](https://cdisc.org/odm2/slot/asOfDateTime)
Alias: asOfDateTime

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information |  no  |







## Properties

* Range: [Datetime](../types/Datetime.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:asOfDateTime |
| native | odm:asOfDateTime |




## LinkML Source

<details>
```yaml
name: asOfDateTime
description: Date and time when the data snapshot was taken
from_schema: https://cdisc.org/define-json
rank: 1000
alias: asOfDateTime
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: datetime

```
</details>