

# Slot: studyDescription 


_Description of the study_





URI: [odm:slot/studyDescription](https://cdisc.org/odm2/slot/studyDescription)
Alias: studyDescription

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [StudyMetadata](../classes/StudyMetadata.md) | A mixin that provides study-level metadata attributes including study identif... |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:studyDescription |
| native | odm:studyDescription |




## LinkML Source

<details>
```yaml
name: studyDescription
description: Description of the study
from_schema: https://cdisc.org/define-json
rank: 1000
alias: studyDescription
owner: StudyMetadata
domain_of:
- StudyMetadata
range: string

```
</details>