

# Slot: version 


_The version of the external resources_





URI: [odm:version](https://cdisc.org/odm2/version)
Alias: version

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataflow](Dataflow.md) | An abstract representation that defines data provision for different referenc... |  no  |
| [DataService](DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |  no  |
| [ProvisionAgreement](ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [DataProduct](DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |
| [ReifiedConcept](ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [Resource](Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [IsProfile](IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |
| [CodeList](CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |  no  |
| [DocumentReference](DocumentReference.md) | A comprehensive reference element that points to an external document, combin... |  no  |
| [Versioned](Versioned.md) | A mixin that provides version and connectivity information, including version... |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:version |
| native | odm:version |




## LinkML Source

<details>
```yaml
name: version
description: The version of the external resources
from_schema: https://cdisc.org/define-json
rank: 1000
alias: version
owner: Versioned
domain_of:
- Versioned
range: string

```
</details>