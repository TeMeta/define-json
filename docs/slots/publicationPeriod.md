

# Slot: publicationPeriod 


_Specifies the period of publication of the data or metadata in terms of whatever provisioning agreements might be in force._





URI: [dds:slot/publicationPeriod](https://w3id.org/dds/slot/publicationPeriod)
Alias: publicationPeriod

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
| self | dds:publicationPeriod |
| native | dds:publicationPeriod |




## LinkML Source

<details>
```yaml
name: publicationPeriod
description: Specifies the period of publication of the data or metadata in terms
  of whatever provisioning agreements might be in force.
from_schema: https://w3id.org/dds
rank: 1000
alias: publicationPeriod
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>