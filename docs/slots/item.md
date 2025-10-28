

# Slot: item 



URI: [odm:slot/item](https://cdisc.org/odm2/slot/item)
Alias: item

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Measure](../classes/Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [RangeCheck](../classes/RangeCheck.md) | A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result |  no  |
| [SourceItem](../classes/SourceItem.md) | A data source that provides the origin of information for an item |  no  |
| [DataAttribute](../classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata about observations |  no  |
| [ObservationRelationship](../classes/ObservationRelationship.md) | A relationship element that associates a DataAttribute with an Observation, allowing value-level Items to be reused across multiple different Views |  no  |
| [Dimension](../classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [CubeComponent](../classes/CubeComponent.md) | An abstract data field that represents a component in a data structure definition, referencing an Item for its definition |  no  |







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