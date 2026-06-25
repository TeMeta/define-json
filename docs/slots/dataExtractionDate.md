

# Slot: dataExtractionDate 


_A specific time period that identifies the date and time that the data are extracted from a data source._





URI: [dds:slot/dataExtractionDate](https://w3id.org/dds/slot/dataExtractionDate)
Alias: dataExtractionDate

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
| self | dds:dataExtractionDate |
| native | dds:dataExtractionDate |




## LinkML Source

<details>
```yaml
name: dataExtractionDate
description: A specific time period that identifies the date and time that the data
  are extracted from a data source.
from_schema: https://w3id.org/dds
rank: 1000
alias: dataExtractionDate
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>