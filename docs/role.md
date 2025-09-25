

# Slot: role 



URI: [odm:role](https://cdisc.org/odm2/role)
Alias: role

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CubeComponent](CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [DataProvider](DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |  no  |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [DataAttribute](DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [Measure](Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [IsODMItem](IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |  no  |
| [Organization](Organization.md) | An entity that represents organizational information, such as a site or spons... |  no  |
| [Dimension](Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:role |
| native | odm:role |




## LinkML Source

<details>
```yaml
name: role
alias: role
domain_of:
- IsODMItem
- Organization
- CubeComponent

```
</details>