

# Class: StudyMetadata 


_A mixin that provides study-level metadata attributes including study identification and protocol information_





URI: [dds:class/StudyMetadata](https://w3id.org/dds/class/StudyMetadata)


```mermaid
erDiagram
StudyMetadata {
    string studyOID  
    string studyName  
    string studyDescription  
    string protocolName  
}



```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [studyOID](../slots/studyOID.md) | 1 <br/> [String](../types/String.md) | Unique identifier for the study | direct |
| [studyName](../slots/studyName.md) | 0..1 <br/> [String](../types/String.md) | Name of the study | direct |
| [studyDescription](../slots/studyDescription.md) | 0..1 <br/> [String](../types/String.md) | Description of the study | direct |
| [protocolName](../slots/protocolName.md) | 0..1 <br/> [String](../types/String.md) | Protocol name for the study | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |









## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:StudyMetadata |
| native | dds:StudyMetadata |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: StudyMetadata
description: A mixin that provides study-level metadata attributes including study
  identification and protocol information
from_schema: https://w3id.org/dds
mixin: true
attributes:
  studyOID:
    name: studyOID
    description: Unique identifier for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - StudyMetadata
    required: true
  studyName:
    name: studyName
    description: Name of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - StudyMetadata
  studyDescription:
    name: studyDescription
    description: Description of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - StudyMetadata
  protocolName:
    name: protocolName
    description: Protocol name for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - StudyMetadata

```
</details>

### Induced

<details>
```yaml
name: StudyMetadata
description: A mixin that provides study-level metadata attributes including study
  identification and protocol information
from_schema: https://w3id.org/dds
mixin: true
attributes:
  studyOID:
    name: studyOID
    description: Unique identifier for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyOID
    owner: StudyMetadata
    domain_of:
    - StudyMetadata
    range: string
    required: true
  studyName:
    name: studyName
    description: Name of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyName
    owner: StudyMetadata
    domain_of:
    - StudyMetadata
    range: string
  studyDescription:
    name: studyDescription
    description: Description of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyDescription
    owner: StudyMetadata
    domain_of:
    - StudyMetadata
    range: string
  protocolName:
    name: protocolName
    description: Protocol name for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: protocolName
    owner: StudyMetadata
    domain_of:
    - StudyMetadata
    range: string

```
</details>