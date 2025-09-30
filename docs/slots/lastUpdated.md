

# Slot: lastUpdated 


_When the resource was last updated_





URI: [odm:slot/lastUpdated](https://cdisc.org/odm2/slot/lastUpdated)
Alias: lastUpdated

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAttribute](../classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned enc... |  no  |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different referenc... |  no  |
| [Measure](../classes/Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [CubeComponent](../classes/CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |
| [Dimension](../classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [ConceptProperty](../classes/ConceptProperty.md) | A reified property concept that exists within the context of its containing t... |  no  |
| [GovernedElement](../classes/GovernedElement.md) |  |  no  |
| [Condition](../classes/Condition.md) | A reusable logical construct that combines multiple components using AND logi... |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |  no  |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and ca... |  no  |
| [Governed](../classes/Governed.md) | A mixin that provides slots for audit trail and standards governance, includi... |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |







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