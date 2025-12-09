

# Slot: dataExtractionDate 


_A specific time period that identifies the date and time that the data are extracted from a data source._





URI: [odm:slot/dataExtractionDate](https://cdisc.org/odm2/slot/dataExtractionDate)
Alias: dataExtractionDate

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
| self | odm:dataExtractionDate |
| native | odm:dataExtractionDate |




## LinkML Source

<details>
```yaml
name: dataExtractionDate
description: A specific time period that identifies the date and time that the data
  are extracted from a data source.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: dataExtractionDate
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset

```
</details>