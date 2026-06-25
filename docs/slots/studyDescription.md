

# Slot: studyDescription 


_Description of the study_





URI: [dds:slot/studyDescription](https://w3id.org/dds/slot/studyDescription)
Alias: studyDescription

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |
| [StudyMetadata](../classes/StudyMetadata.md) | A mixin that provides study-level metadata attributes including study identification and protocol information |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:studyDescription |
| native | dds:studyDescription |




## LinkML Source

<details>
```yaml
name: studyDescription
description: Description of the study
from_schema: https://w3id.org/dds
rank: 1000
alias: studyDescription
owner: StudyMetadata
domain_of:
- StudyMetadata
range: string

```
</details>