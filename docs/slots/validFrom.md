

# Slot: validFrom 


_Indicates the inclusive start time indicating the validity of the information in the data set._





URI: [dds:slot/validFrom](https://w3id.org/dds/slot/validFrom)
Alias: validFrom

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
| self | dds:validFrom |
| native | dds:validFrom |




## LinkML Source

<details>
```yaml
name: validFrom
description: Indicates the inclusive start time indicating the validity of the information
  in the data set.
from_schema: https://w3id.org/dds
rank: 1000
alias: validFrom
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>