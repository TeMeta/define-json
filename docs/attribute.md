

# Slot: attribute 



URI: [odm:attribute](https://cdisc.org/odm2/attribute)
Alias: attribute

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DimensionRelationship](DimensionRelationship.md) | A relationship element that associates a DataAttribute with a specific Dimens... |  no  |
| [ObservationRelationship](ObservationRelationship.md) | A relationship element that associates a DataAttribute with an Observation, a... |  no  |
| [DataService](DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |  no  |
| [GroupRelationship](GroupRelationship.md) | A relationship element that associates a DataAttribute with a set of Dimensio... |  no  |
| [Resource](Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |  no  |
| [DataflowRelationship](DataflowRelationship.md) | A relationship element that associates a DataAttribute with a Dataflow, repor... |  no  |
| [MeasureRelationship](MeasureRelationship.md) | A relationship element that associates a DataAttribute with a Measure |  no  |







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