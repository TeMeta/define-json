

# Slot: validityPeriod 


_Time period during which the resource is valid_





URI: [dds:slot/validityPeriod](https://w3id.org/dds/slot/validityPeriod)
Alias: validityPeriod

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [Timing](../classes/Timing.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:validityPeriod |
| native | dds:validityPeriod |




## LinkML Source

<details>
```yaml
name: validityPeriod
description: Time period during which the resource is valid
from_schema: https://w3id.org/dds
rank: 1000
alias: validityPeriod
owner: IsProfile
domain_of:
- IsProfile
range: Timing
required: false

```
</details>