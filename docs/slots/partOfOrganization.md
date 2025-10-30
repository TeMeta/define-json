

# Slot: partOfOrganization 


_Reference to a parent organization if this organization is part of a larger entity._





URI: [odm:slot/partOfOrganization](https://cdisc.org/odm2/slot/partOfOrganization)
Alias: partOfOrganization

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |







## Properties

* Range: [Organization](../classes/Organization.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:partOfOrganization |
| native | odm:partOfOrganization |




## LinkML Source

<details>
```yaml
name: partOfOrganization
description: Reference to a parent organization if this organization is part of a
  larger entity.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: partOfOrganization
owner: Organization
domain_of:
- Organization
range: Organization

```
</details>