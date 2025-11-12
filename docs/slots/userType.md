

# Slot: userType 


_User's role in the study._





URI: [odm:slot/userType](https://cdisc.org/odm2/slot/userType)
Alias: userType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical data collection or data management system |  no  |







## Properties

* Range: [UserType](../enums/UserType.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:userType |
| native | odm:userType |




## LinkML Source

<details>
```yaml
name: userType
description: User's role in the study.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: userType
owner: User
domain_of:
- User
range: UserType

```
</details>