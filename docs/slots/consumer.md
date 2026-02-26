

# Slot: consumer 


_The Data Consumer that is part of this agreement_





URI: [odm:slot/consumer](https://cdisc.org/odm2/slot/consumer)
Alias: consumer

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |






## Properties

* Range: NONE&nbsp;or&nbsp;<br />[DataProduct](../classes/DataProduct.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:consumer |
| native | odm:consumer |




## LinkML Source

<details>
```yaml
name: consumer
description: The Data Consumer that is part of this agreement
from_schema: https://cdisc.org/define-json
rank: 1000
alias: consumer
owner: ProvisionAgreement
domain_of:
- ProvisionAgreement
any_of:
- range: DataProduct
- range: Organization
- range: string

```
</details>