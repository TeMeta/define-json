

# Slot: address 


_The address of the organization._





URI: [dds:slot/address](https://w3id.org/dds/slot/address)
Alias: address

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [DataConsumer](../classes/DataConsumer.md) | An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider. |  no  |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:address |
| native | dds:address |




## LinkML Source

<details>
```yaml
name: address
description: The address of the organization.
from_schema: https://w3id.org/dds
rank: 1000
alias: address
owner: Organization
domain_of:
- Organization
range: string

```
</details>