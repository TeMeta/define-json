

# Slot: profile 


_Profiles this resource claims to conform to_





URI: [odm:slot/profile](https://cdisc.org/odm2/slot/profile)
Alias: profile

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |







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