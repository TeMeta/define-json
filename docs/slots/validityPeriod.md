

# Slot: validityPeriod 


_Time period during which the resouce is valid_





URI: [odm:slot/validityPeriod](https://cdisc.org/odm2/slot/validityPeriod)
Alias: validityPeriod

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |







## Properties

* Range: [Timing](../classes/Timing.md)





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