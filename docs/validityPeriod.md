

# Slot: validityPeriod 


_Time period during which the resouce is valid_





URI: [odm:validityPeriod](https://cdisc.org/odm2/validityPeriod)
Alias: validityPeriod

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [IsProfile](IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |







## Properties

* Range: [Timing](Timing.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:validityPeriod |
| native | odm:validityPeriod |




## LinkML Source

<details>
```yaml
name: validityPeriod
description: Time period during which the resouce is valid
from_schema: https://cdisc.org/define-json
rank: 1000
alias: validityPeriod
owner: IsProfile
domain_of:
- IsProfile
range: Timing
required: false

```
</details>