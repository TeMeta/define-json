

# Slot: security 


_Security tags applied to this resource_





URI: [odm:security](https://cdisc.org/odm2/security)
Alias: security

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [IsProfile](IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |







## Properties

* Range: [Coding](Coding.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:security |
| native | odm:security |




## LinkML Source

<details>
```yaml
name: security
description: Security tags applied to this resource
from_schema: https://cdisc.org/define-json
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