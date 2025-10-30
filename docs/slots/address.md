

# Slot: address 


_The address of the organization._





URI: [odm:slot/address](https://cdisc.org/odm2/slot/address)
Alias: address

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:address |
| native | odm:address |




## LinkML Source

<details>
```yaml
name: address
description: The address of the organization.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: address
owner: Organization
domain_of:
- Organization
range: string

```
</details>