

# Slot: action 



URI: [dds:slot/action](https://w3id.org/dds/slot/action)
Alias: action

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |
| [IsSdmxDataset](../classes/IsSdmxDataset.md) | A mixin that provides additional metadata specific to SDMX Datasets |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:action |
| native | dds:action |




## LinkML Source

<details>
```yaml
name: action
alias: action
domain_of:
- IsSdmxDataset
- Rule
range: string

```
</details>