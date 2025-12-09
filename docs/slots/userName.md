

# Slot: userName 


_The username of the user._





URI: [odm:slot/userName](https://cdisc.org/odm2/slot/userName)
Alias: userName

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical data collection or data management system |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:userName |
| native | odm:userName |




## LinkML Source

<details>
```yaml
name: userName
description: The username of the user.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: userName
owner: User
domain_of:
- User
range: string

```
</details>