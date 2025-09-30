

# Slot: protocolName 


_Protocol name for the study_





URI: [odm:slot/protocolName](https://cdisc.org/odm2/slot/protocolName)
Alias: protocolName

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
| self | odm:protocolName |
| native | odm:protocolName |




## LinkML Source

<details>
```yaml
name: protocolName
description: Protocol name for the study
from_schema: https://cdisc.org/define-json
rank: 1000
alias: protocolName
owner: StudyMetadata
domain_of:
- StudyMetadata
range: string

```
</details>