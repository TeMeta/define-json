

# Slot: href 


_Machine-readable instructions to obtain the resource e.g. FHIR path, URL_





URI: [odm:slot/href](https://cdisc.org/odm2/slot/href)
Alias: href

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different referenc... |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |  no  |
| [Versioned](../classes/Versioned.md) | A mixin that provides version and connectivity information, including version... |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combin... |  no  |







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