

# Slot: OID 


_Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use._





URI: [odm:OID](https://cdisc.org/odm2/OID)
Alias: OID

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Comment](Comment.md) | A descriptive element that contains explanatory text provided by a data or me... |  no  |
| [DataService](DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |  no  |
| [ProvisionAgreement](ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [DataProvider](DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |  no  |
| [FormalExpression](FormalExpression.md) | A computational element that defines the execution of a data derivation withi... |  no  |
| [User](User.md) | An entity that represents information about a specific user of a clinical dat... |  no  |
| [ReifiedConcept](ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [CodingMapping](CodingMapping.md) | A mapping relationship that establishes connections between different coding ... |  no  |
| [DocumentReference](DocumentReference.md) | A comprehensive reference element that points to an external document, combin... |  no  |
| [Relationship](Relationship.md) | A semantic link that defines connections between elements such as Items or It... |  no  |
| [ReturnValue](ReturnValue.md) | An output specification that defines the details of what a formal expression ... |  no  |
| [ComponentList](ComponentList.md) | An abstract definition that specifies a list of components within a data stru... |  no  |
| [Parameter](Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [Dataflow](Dataflow.md) | An abstract representation that defines data provision for different referenc... |  no  |
| [ConceptProperty](ConceptProperty.md) | A reified property concept that exists within the context of its containing t... |  no  |
| [DataProduct](DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |
| [Method](Method.md) | A reusable computational procedure that describes how to derive values and ca... |  no  |
| [Resource](Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |  no  |
| [IdentifiableElement](IdentifiableElement.md) |  |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [Timing](Timing.md) | A temporal element that describes the timing of an event or occurrence, which... |  no  |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [Organization](Organization.md) | An entity that represents organizational information, such as a site or spons... |  no  |
| [Dimension](Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [CubeComponent](CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [SiteOrSponsorComment](SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct fr... |  no  |
| [Condition](Condition.md) | A reusable logical construct that combines multiple components using AND logi... |  no  |
| [MetaDataVersion](MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [Identifiable](Identifiable.md) | A mixin that provides slots for making an entity addressable within a study o... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [Measure](Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [CodeList](CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |  no  |
| [GovernedElement](GovernedElement.md) |  |  no  |
| [NominalOccurrence](NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned enc... |  no  |
| [DataAttribute](DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [WhereClause](WhereClause.md) | A conditional element that describes the circumstances under which a containi... |  no  |







## Properties

* Range: [String](String.md)

* Required: True

* Regex pattern: `^[A-Za-z][A-Za-z0-9._-]*$`





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:OID |
| native | odm:OID |




## LinkML Source

<details>
```yaml
name: OID
description: Local identifier within this study/context. Use CDISC OID format for
  regulatory submissions, or simple strings for internal use.
from_schema: https://cdisc.org/define-json
rank: 1000
identifier: true
alias: OID
owner: Identifiable
domain_of:
- Identifiable
range: string
required: true
pattern: ^[A-Za-z][A-Za-z0-9._-]*$

```
</details>