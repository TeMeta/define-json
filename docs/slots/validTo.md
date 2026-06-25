

# Slot: validTo 


_Indicates the inclusive end time indicating the validity of the information in the data set._





URI: [dds:slot/validTo](https://w3id.org/dds/slot/validTo)
Alias: validTo

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsSdmxDataset](../classes/IsSdmxDataset.md) | A mixin that provides additional metadata specific to SDMX Datasets |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:validTo |
| native | dds:validTo |




## LinkML Source

<details>
```yaml
name: validTo
description: Indicates the inclusive end time indicating the validity of the information
  in the data set.
from_schema: https://w3id.org/dds
rank: 1000
alias: validTo
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>