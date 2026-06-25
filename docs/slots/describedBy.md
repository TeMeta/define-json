

# Slot: describedBy 



URI: [dds:slot/describedBy](https://w3id.org/dds/slot/describedBy)
Alias: describedBy

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupKey](../classes/GroupKey.md) | A dimension subset that represents collections of dimensions that are subsets of the full dimension set, distinct from SeriesKey which includes Time dimensions |  no  |
| [SeriesKey](../classes/SeriesKey.md) | A unique identifier that comprises the cross-product of dimension values including Time to identify observations, representing dimensions shared by all observations in a conceptual series |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [DatasetKey](../classes/DatasetKey.md) | An abstract identifier that comprises the cross-product of dimension values to identify a specific cross-section |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:describedBy |
| native | dds:describedBy |




## LinkML Source

<details>
```yaml
name: describedBy
alias: describedBy
domain_of:
- Dataset
- DatasetKey
range: string

```
</details>