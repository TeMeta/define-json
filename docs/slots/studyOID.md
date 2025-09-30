

# Slot: studyOID 


_Unique identifier for the study_





URI: [odm:slot/studyOID](https://cdisc.org/odm2/slot/studyOID)
Alias: studyOID

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [StudyMetadata](../classes/StudyMetadata.md) | A mixin that provides study-level metadata attributes including study identif... |  no  |







## Properties

* Range: [String](../types/String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:studyOID |
| native | odm:studyOID |




## LinkML Source

<details>
```yaml
name: studyOID
description: Unique identifier for the study
from_schema: https://cdisc.org/define-json
rank: 1000
alias: studyOID
owner: StudyMetadata
domain_of:
- StudyMetadata
range: string
required: true

```
</details>