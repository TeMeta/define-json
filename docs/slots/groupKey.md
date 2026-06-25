

# Slot: groupKey 



URI: [dds:slot/groupKey](https://w3id.org/dds/slot/groupKey)
Alias: groupKey

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupRelationship](../classes/GroupRelationship.md) | A relationship element that associates a DataAttribute with a set of Dimensions, used when attribute values vary based on all group dimension values |  no  |
| [DimensionRelationship](../classes/DimensionRelationship.md) | A relationship element that associates a DataAttribute with a specific Dimension at a specific level |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:groupKey |
| native | dds:groupKey |




## LinkML Source

<details>
```yaml
name: groupKey
alias: groupKey
domain_of:
- GroupRelationship
- DimensionRelationship
range: string

```
</details>