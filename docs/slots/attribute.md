

# Slot: attribute 



URI: [odm:slot/attribute](https://cdisc.org/odm2/slot/attribute)
Alias: attribute

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ObservationRelationship](../classes/ObservationRelationship.md) | A relationship element that associates a DataAttribute with an Observation, allowing value-level Items to be reused across multiple different Views |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [DataflowRelationship](../classes/DataflowRelationship.md) | A relationship element that associates a DataAttribute with a Dataflow, reported at the Dataset level |  no  |
| [MeasureRelationship](../classes/MeasureRelationship.md) | A relationship element that associates a DataAttribute with a Measure |  no  |
| [DimensionRelationship](../classes/DimensionRelationship.md) | A relationship element that associates a DataAttribute with a specific Dimension at a specific level |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |
| [GroupRelationship](../classes/GroupRelationship.md) | A relationship element that associates a DataAttribute with a set of Dimensions, used when attribute values vary based on all group dimension values |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:attribute |
| native | odm:attribute |




## LinkML Source

<details>
```yaml
name: attribute
alias: attribute
domain_of:
- Resource
- MeasureRelationship
- DataflowRelationship
- GroupRelationship
- DimensionRelationship
- ObservationRelationship

```
</details>