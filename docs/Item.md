

# Slot: item 



URI: [odm:item](https://cdisc.org/odm2/item)
Alias: item

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CubeComponent](CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [ObservationRelationship](ObservationRelationship.md) | A relationship element that associates a DataAttribute with an Observation, a... |  no  |
| [DataAttribute](DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [Measure](Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [RangeCheck](RangeCheck.md) | A validation element that performs a simple comparison check between a refere... |  no  |
| [SourceItem](SourceItem.md) | A data source that provides the origin of information for an item |  no  |
| [Dimension](Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:item |
| native | odm:item |




## LinkML Source

<details>
```yaml
name: item
alias: item
domain_of:
- RangeCheck
- SourceItem
- CubeComponent
- ObservationRelationship

```
</details>