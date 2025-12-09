

# Slot: provisionAgreements 


_The ProvisionAgreements that this provider has with Data Consumers_





URI: [odm:slot/provisionAgreements](https://cdisc.org/odm2/slot/provisionAgreements)
Alias: provisionAgreements

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |






## Properties

* Range: [ProvisionAgreement](../classes/ProvisionAgreement.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:provisionAgreements |
| native | odm:provisionAgreements |




## LinkML Source

<details>
```yaml
name: provisionAgreements
description: The ProvisionAgreements that this provider has with Data Consumers
from_schema: https://cdisc.org/define-json
rank: 1000
alias: provisionAgreements
owner: DataProvider
domain_of:
- DataProvider
range: ProvisionAgreement
multivalued: true

```
</details>