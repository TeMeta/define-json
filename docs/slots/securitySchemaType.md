

# Slot: securitySchemaType 


_Security or authentication method used (e.g., OAuth2)_





URI: [odm:slot/securitySchemaType](https://cdisc.org/odm2/slot/securitySchemaType)
Alias: securitySchemaType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:securitySchemaType |
| native | odm:securitySchemaType |




## LinkML Source

<details>
```yaml
name: securitySchemaType
description: Security or authentication method used (e.g., OAuth2)
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: securitySchemaType
owner: DataService
domain_of:
- DataService
range: string

```
</details>