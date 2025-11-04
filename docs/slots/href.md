

# Slot: href 


_Machine-readable instructions to obtain the resource e.g. FHIR path, URL_





URI: [odm:slot/href](https://cdisc.org/odm2/slot/href)
Alias: href

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [Display](../classes/Display.md) | A rendered output of an analysis result. |  no  |
| [Versioned](../classes/Versioned.md) | A mixin that provides version and connectivity information, including version numbers and resource references |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and referenceable, showing how different data implementations represent the same underlying meanings through a star schema structure with multiple properties |  no  |
| [Dictionary](../classes/Dictionary.md) | A dictionary that defines a set of codes and their meanings |  no  |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:href |
| native | odm:href |




## LinkML Source

<details>
```yaml
name: href
description: Machine-readable instructions to obtain the resource e.g. FHIR path,
  URL
from_schema: https://cdisc.org/define-json
rank: 1000
alias: href
owner: Versioned
domain_of:
- Versioned
range: string
required: false

```
</details>