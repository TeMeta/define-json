

# Slot: label 


_Human-readable label, shown in UIs_





URI: [odm:slot/label](https://cdisc.org/odm2/slot/label)
Alias: label

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical data collection or data management system |  no  |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items.<br>Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions. |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |
| [DataAttribute](../classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata about observations |  no  |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |
| [Measure](../classes/Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [ConceptProperty](../classes/ConceptProperty.md) | A reified property concept that exists within the context of its containing topic concept |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Dictionary](../classes/Dictionary.md) | A dictionary that defines a set of codes and their meanings |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle |  no  |
| [ReturnValue](../classes/ReturnValue.md) | An output specification that defines the details of what a formal expression returns |  no  |
| [Labelled](../classes/Labelled.md) | A mixin that provides slots for detailing meanings and multilingual descriptions |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ComponentList](../classes/ComponentList.md) | An abstract definition that specifies a list of components within a data structure definition, including various descriptor types |  no  |
| [Relationship](../classes/Relationship.md) | A semantic link that defines connections between elements such as Items or ItemGroups, capturing relationships like "is the unit for" or "assesses seriousness of" |  no  |
| [Display](../classes/Display.md) | A rendered output of an analysis result. |  no  |
| [Dimension](../classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [GovernedElement](../classes/GovernedElement.md) |  |  no  |
| [Standard](../classes/Standard.md) | A collection element that groups related standards within a specific context, used for defining CDISC implementation guides and controlled terminologies |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [IdentifiableElement](../classes/IdentifiableElement.md) |  |  no  |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned encounters or adverse events |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and referenceable, showing how different data implementations represent the same underlying meanings through a star schema structure with multiple properties |  no  |
| [FormalExpression](../classes/FormalExpression.md) | A computational element that defines the execution of a data derivation within a specific context |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [Condition](../classes/Condition.md) | A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions. |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [WhereClause](../classes/WhereClause.md) | A conditional element that describes the circumstances under which a containing context applies, linking conditions to structures where they are used |  no  |
| [CubeComponent](../classes/CubeComponent.md) | An abstract data field that represents a component in a data structure definition, referencing an Item for its definition |  no  |
| [Comment](../classes/Comment.md) | A descriptive element that contains explanatory text provided by a data or metadata handler |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:label |
| native | odm:label |
| exact | skos:prefLabel |




## LinkML Source

<details>
```yaml
name: label
description: Human-readable label, shown in UIs
from_schema: https://cdisc.org/define-json
exact_mappings:
- skos:prefLabel
rank: 1000
alias: label
owner: Labelled
domain_of:
- Labelled
any_of:
- range: string
- range: TranslatedText

```
</details>