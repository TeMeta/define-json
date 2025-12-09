

# Slot: creationDateTime 


_Date and time when the ODM file was created_





URI: [odm:slot/creationDateTime](https://cdisc.org/odm2/slot/creationDateTime)
Alias: creationDateTime

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information |  no  |






## Properties

* Range: [Datetime](../types/Datetime.md)

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:creationDateTime |
| native | odm:creationDateTime |




## LinkML Source

<details>
```yaml
name: creationDateTime
description: Date and time when the ODM file was created
from_schema: https://cdisc.org/define-json
rank: 1000
alias: creationDateTime
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: datetime
required: true

```
</details>