

# Slot: analyses 


_Analyses defined in this version of the metadata._





URI: [odm:slot/analyses](https://cdisc.org/odm2/slot/analyses)
Alias: analyses

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |






## Properties

* Range: [Analysis](../classes/Analysis.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:analyses |
| native | odm:analyses |




## LinkML Source

<details>
```yaml
name: analyses
description: Analyses defined in this version of the metadata.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: analyses
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: Analysis
multivalued: true
inlined: true
inlined_as_list: true

```
</details>