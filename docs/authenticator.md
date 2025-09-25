

# Slot: authenticator 


_Who/what authenticated the resource_





URI: [odm:authenticator](https://cdisc.org/odm2/authenticator)
Alias: authenticator

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |
| [ItemGroup](ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |  no  |
| [IsProfile](IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |  no  |
| [DataStructureDefinition](DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[User](User.md)&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:authenticator |
| native | odm:authenticator |




## LinkML Source

<details>
```yaml
name: authenticator
description: Who/what authenticated the resource
from_schema: https://cdisc.org/define-json
rank: 1000
alias: authenticator
owner: IsProfile
domain_of:
- IsProfile
required: false
any_of:
- range: User
- range: Organization
- range: string

```
</details>