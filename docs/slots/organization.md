

# Slot: organization 


_The organization the user belongs to._





URI: [dds:slot/organization](https://w3id.org/dds/slot/organization)
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


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:organization |
| native | dds:organization |
| close | prov:actedOnBehalfOf |




## LinkML Source

<details>
```yaml
name: organization
description: The organization the user belongs to.
from_schema: https://w3id.org/dds
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