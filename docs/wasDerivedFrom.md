

# Slot: wasDerivedFrom 


_Reference to another item that this item implements or extends, e.g. a template Item definition._





URI: [odm:wasDerivedFrom](https://cdisc.org/odm2/wasDerivedFrom)
Alias: wasDerivedFrom

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Condition](Condition.md) | A reusable logical construct that combines multiple components using AND logi... |  no  |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [ProvisionAgreement](ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [CodeList](CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [DataAttribute](DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [ReifiedConcept](ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |
| [Method](Method.md) | A reusable computational procedure that describes how to derive values and ca... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [Dataflow](Dataflow.md) | An abstract representation that defines data provision for different referenc... |  no  |
| [CubeComponent](CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [NominalOccurrence](NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned enc... |  no  |
| [MetaDataVersion](MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |
| [DataProduct](DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |
| [Measure](Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [Dimension](Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [Governed](Governed.md) | A mixin that provides slots for audit trail and standards governance, includi... |  no  |
| [GovernedElement](GovernedElement.md) |  |  no  |
| [ConceptProperty](ConceptProperty.md) | A reified property concept that exists within the context of its containing t... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[Item](Item.md)&nbsp;or&nbsp;<br />[ItemGroup](ItemGroup.md)&nbsp;or&nbsp;<br />[MetaDataVersion](MetaDataVersion.md)&nbsp;or&nbsp;<br />[CodeList](CodeList.md)&nbsp;or&nbsp;<br />[ReifiedConcept](ReifiedConcept.md)&nbsp;or&nbsp;<br />[ConceptProperty](ConceptProperty.md)&nbsp;or&nbsp;<br />[Condition](Condition.md)&nbsp;or&nbsp;<br />[Method](Method.md)&nbsp;or&nbsp;<br />[NominalOccurrence](NominalOccurrence.md)&nbsp;or&nbsp;<br />[Dataflow](Dataflow.md)&nbsp;or&nbsp;<br />[CubeComponent](CubeComponent.md)&nbsp;or&nbsp;<br />[DataProduct](DataProduct.md)&nbsp;or&nbsp;<br />[ProvisionAgreement](ProvisionAgreement.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:wasDerivedFrom |
| native | odm:wasDerivedFrom |
| exact | prov:wasDerivedFrom |




## LinkML Source

<details>
```yaml
name: wasDerivedFrom
description: Reference to another item that this item implements or extends, e.g.
  a template Item definition.
from_schema: https://cdisc.org/define-json
exact_mappings:
- prov:wasDerivedFrom
rank: 1000
alias: wasDerivedFrom
owner: Governed
domain_of:
- Governed
any_of:
- range: Item
- range: ItemGroup
- range: MetaDataVersion
- range: CodeList
- range: ReifiedConcept
- range: ConceptProperty
- range: Condition
- range: Method
- range: NominalOccurrence
- range: Dataflow
- range: CubeComponent
- range: DataProduct
- range: ProvisionAgreement

```
</details>