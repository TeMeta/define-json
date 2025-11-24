

# Slot: publicationYear 


_Specifies the year of publication of the data or metadata in terms of whatever provisioning agreements might be in force._





URI: [odm:slot/publicationYear](https://cdisc.org/odm2/slot/publicationYear)
Alias: publicationYear

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
| self | odm:publicationYear |
| native | odm:publicationYear |




## LinkML Source

<details>
```yaml
name: publicationYear
description: Specifies the year of publication of the data or metadata in terms of
  whatever provisioning agreements might be in force.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: publicationYear
owner: IsSdmxDataset
domain_of:
- IsSdmxDataset

```
</details>