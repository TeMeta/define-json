

# Slot: organization 


_The organization the user belongs to._





URI: [odm:slot/organization](https://cdisc.org/odm2/slot/organization)
Alias: organization

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical data collection or data management system |  no  |







## Properties

* Range: [Organization](../classes/Organization.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:organization |
| native | odm:organization |
| close | prov:actedOnBehalfOf |




## LinkML Source

<details>
```yaml
name: organization
description: The organization the user belongs to.
from_schema: https://cdisc.org/define-json
close_mappings:
- prov:actedOnBehalfOf
rank: 1000
alias: organization
owner: User
domain_of:
- User
range: Organization

```
</details>