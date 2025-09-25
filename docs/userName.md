

# Slot: userName 


_The username of the user._





URI: [odm:userName](https://cdisc.org/odm2/userName)
Alias: userName

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [User](User.md) | An entity that represents information about a specific user of a clinical dat... |  no  |







## Properties

* Range: [String](String.md)





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