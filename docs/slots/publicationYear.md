

# Slot: publicationYear 


_Specifies the year of publication of the data or metadata in terms of whatever provisioning agreements might be in force._





URI: [dds:slot/publicationYear](https://w3id.org/dds/slot/publicationYear)
Alias: publicationYear

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
| self | dds:publicationYear |
| native | dds:publicationYear |




## LinkML Source

<details>
```yaml
name: publicationYear
description: Specifies the year of publication of the data or metadata in terms of
  whatever provisioning agreements might be in force.
from_schema: https://w3id.org/dds
rank: 1000
alias: publicationYear
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset
range: string

```
</details>