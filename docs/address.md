

# Slot: address 


_The address of the organization._





URI: [odm:address](https://cdisc.org/odm2/address)
Alias: address

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |  no  |
| [Organization](Organization.md) | An entity that represents organizational information, such as a site or spons... |  no  |







## Properties

* Range: [String](String.md)





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