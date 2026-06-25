

# Slot: consumer 


_The Data Consumer that is part of this agreement_





URI: [dds:slot/consumer](https://w3id.org/dds/slot/consumer)
Alias: consumer

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[DataConsumer](../classes/DataConsumer.md)&nbsp;or&nbsp;<br />[DataProduct](../classes/DataProduct.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:consumer |
| native | dds:consumer |




## LinkML Source

<details>
```yaml
name: consumer
description: The Data Consumer that is part of this agreement
from_schema: https://w3id.org/dds
rank: 1000
alias: consumer
owner: ProvisionAgreement
domain_of:
- ProvisionAgreement
range: string
any_of:
- range: DataConsumer
- range: DataProduct
- range: Organization
- range: string

```
</details>