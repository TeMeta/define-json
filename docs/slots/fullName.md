

# Slot: fullName 


_The full name of the user._





URI: [odm:slot/fullName](https://cdisc.org/odm2/slot/fullName)
Alias: fullName

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical dat... |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:fullName |
| native | odm:fullName |




## LinkML Source

<details>
```yaml
name: fullName
description: The full name of the user.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: fullName
owner: User
domain_of:
- User
range: string

```
</details>