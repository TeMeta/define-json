

# Slot: authenticator 


_Who/what authenticated the resource_





URI: [odm:slot/authenticator](https://cdisc.org/odm2/slot/authenticator)
Alias: authenticator

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md)





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