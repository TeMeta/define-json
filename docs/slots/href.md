

# Slot: href 


_Machine-readable instructions to obtain the resource e.g. FHIR path, URL_





URI: [dds:slot/href](https://w3id.org/dds/slot/href)
Alias: href

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [Versioned](../classes/Versioned.md) | A mixin that provides version and connectivity information, including version numbers and resource references |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Concept](../classes/Concept.md) | An abstract concept that can be referenced and specialised by data implementations. Holds ConceptProperties describing the concept's expected data shape. Multiple ItemGroups or Items can implement the same Concept, allowing standard biomedical concepts to be implemented differently across studies while remaining semantically aligned. |  no  |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [Dictionary](../classes/Dictionary.md) | A dictionary that defines a set of codes and their meanings |  no  |
| [Display](../classes/Display.md) | A rendered output of an analysis result. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:href |
| native | dds:href |




## LinkML Source

<details>
```yaml
name: href
description: Machine-readable instructions to obtain the resource e.g. FHIR path,
  URL
from_schema: https://w3id.org/dds
rank: 1000
alias: href
owner: Versioned
domain_of:
- Versioned
range: string
required: false

```
</details>