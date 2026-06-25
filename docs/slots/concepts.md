

# Slot: concepts 


_Structured Concepts defined in this version of the metadata_





URI: [dds:slot/concepts](https://w3id.org/dds/slot/concepts)
Alias: concepts

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [Concept](../classes/Concept.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:concepts |
| native | dds:concepts |




## LinkML Source

<details>
```yaml
name: concepts
description: Structured Concepts defined in this version of the metadata
from_schema: https://w3id.org/dds
rank: 1000
alias: concepts
owner: Specification
domain_of:
- Specification
range: Concept
multivalued: true

```
</details>