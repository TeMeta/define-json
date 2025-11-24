

# Slot: validTo 


_Indicates the inclusive end time indicating the validity of the information in the data set._





URI: [odm:slot/validTo](https://cdisc.org/odm2/slot/validTo)
Alias: validTo

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
| self | odm:validTo |
| native | odm:validTo |




## LinkML Source

<details>
```yaml
name: validTo
description: Indicates the inclusive end time indicating the validity of the information
  in the data set.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: validTo
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset

```
</details>