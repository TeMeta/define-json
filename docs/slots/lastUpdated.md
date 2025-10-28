

# Slot: lastUpdated 


_When the resource was last updated_





URI: [odm:slot/lastUpdated](https://cdisc.org/odm2/slot/lastUpdated)
Alias: lastUpdated

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items.<br>Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions. |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [DataAttribute](../classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata about observations |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [Dimension](../classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [CubeComponent](../classes/CubeComponent.md) | An abstract data field that represents a component in a data structure definition, referencing an Item for its definition |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [WhereClause](../classes/WhereClause.md) | A conditional element that describes the circumstances under which a containing context applies, linking conditions to structures where they are used |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and referenceable, showing how different data implementations represent the same underlying meanings through a star schema structure with multiple properties |  no  |
| [ConceptProperty](../classes/ConceptProperty.md) | A reified property concept that exists within the context of its containing topic concept |  no  |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned encounters or adverse events |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Display](../classes/Display.md) | A rendered output of an analysis result. |  no  |
| [GovernedElement](../classes/GovernedElement.md) |  |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Governed](../classes/Governed.md) | A mixin that provides slots for audit trail and standards governance, including mandatory status, comments, and attribution |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle |  no  |
| [Comment](../classes/Comment.md) | A descriptive element that contains explanatory text provided by a data or metadata handler |  no  |
| [Measure](../classes/Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [Condition](../classes/Condition.md) | A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions. |  no  |







## Properties

* Range: [Datetime](../types/Datetime.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:lastUpdated |
| native | odm:lastUpdated |




## LinkML Source

<details>
```yaml
name: lastUpdated
description: When the resource was last updated
from_schema: https://cdisc.org/define-json
rank: 1000
alias: lastUpdated
owner: Governed
domain_of:
- Governed
range: datetime

```
</details>