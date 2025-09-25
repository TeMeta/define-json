

# Slot: location 


_The physical location of the organization._





URI: [odm:location](https://cdisc.org/odm2/location)
Alias: location

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
| self | odm:location |
| native | odm:location |




## LinkML Source

<details>
```yaml
name: location
description: The physical location of the organization.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: location
owner: Organization
domain_of:
- Organization
range: string

```
</details>