

# Slot: security 


_Security tags applied to this resource_





URI: [dds:slot/security](https://w3id.org/dds/slot/security)
Alias: security

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [Coding](../classes/Coding.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:security |
| native | dds:security |




## LinkML Source

<details>
```yaml
name: security
description: Security tags applied to this resource
from_schema: https://w3id.org/dds
rank: 1000
alias: security
owner: IsProfile
domain_of:
- IsProfile
range: Coding
multivalued: true
inlined: true
inlined_as_list: true

```
</details>