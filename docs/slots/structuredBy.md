

# Slot: structuredBy 


_Associates the Data Structure Definition that defines the structure of the Data Set. Note that the Data Structure Definition is the same as that associated (non-mandatory) to the Dataflow._





URI: [odm:slot/structuredBy](https://cdisc.org/odm2/slot/structuredBy)
Alias: structuredBy

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [DataStructureDefinition](../classes/DataStructureDefinition.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:structuredBy |
| native | odm:structuredBy |




## LinkML Source

<details>
```yaml
name: structuredBy
description: Associates the Data Structure Definition that defines the structure of
  the Data Set. Note that the Data Structure Definition is the same as that associated
  (non-mandatory) to the Dataflow.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: structuredBy
owner: Dataset
domain_of:
- Dataset
range: DataStructureDefinition

```
</details>