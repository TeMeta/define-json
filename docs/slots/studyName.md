

# Slot: studyName 


_Name of the study_





URI: [odm:slot/studyName](https://cdisc.org/odm2/slot/studyName)
Alias: studyName

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [StudyMetadata](../classes/StudyMetadata.md) | A mixin that provides study-level metadata attributes including study identification and protocol information |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:studyName |
| native | odm:studyName |




## LinkML Source

<details>
```yaml
name: studyName
description: Name of the study
from_schema: https://cdisc.org/define-json
rank: 1000
alias: studyName
owner: StudyMetadata
domain_of:
- StudyMetadata
range: string

```
</details>