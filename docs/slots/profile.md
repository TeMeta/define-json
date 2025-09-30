

# Slot: profile 


_Profiles this resource claims to conform to_





URI: [odm:slot/profile](https://cdisc.org/odm2/slot/profile)
Alias: profile

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |







## Properties

* Range: [String](../types/String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:profile |
| native | odm:profile |




## LinkML Source

<details>
```yaml
name: profile
description: Profiles this resource claims to conform to
from_schema: https://cdisc.org/define-json
rank: 1000
alias: profile
owner: IsProfile
domain_of:
- IsProfile
range: string
multivalued: true

```
</details>