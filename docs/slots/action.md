

# Slot: action 


_Defines the action to be taken by the recipient system (information, append, replace, delete)_





URI: [odm:slot/action](https://cdisc.org/odm2/slot/action)
Alias: action

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [IsSdmxDataset](../classes/IsSdmxDataset.md) | A mixin that provides additional metadata specific to SDMX Datasets |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:action |
| native | odm:action |




## LinkML Source

<details>
```yaml
name: action
description: Defines the action to be taken by the recipient system (information,
  append, replace, delete)
from_schema: https://cdisc.org/define-json
rank: 1000
alias: action
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset

```
</details>