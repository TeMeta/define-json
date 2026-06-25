

# Slot: reportingEnd 


_A specific time period in a known system of time periods that identifies the end period of a report._





URI: [dds:slot/reportingEnd](https://w3id.org/dds/slot/reportingEnd)
Alias: reportingEnd

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
| self | dds:reportingEnd |
| native | dds:reportingEnd |




## LinkML Source

<details>
```yaml
name: reportingEnd
description: A specific time period in a known system of time periods that identifies
  the end period of a report.
from_schema: https://w3id.org/dds
rank: 1000
alias: reportingEnd
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>