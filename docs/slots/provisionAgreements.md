

# Slot: provisionAgreements 



URI: [odm:slot/provisionAgreements](https://cdisc.org/odm2/slot/provisionAgreements)
Alias: provisionAgreements

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataConsumer](../classes/DataConsumer.md) | An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider. |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:provisionAgreements |
| native | odm:provisionAgreements |




## LinkML Source

<details>
```yaml
name: provisionAgreements
alias: provisionAgreements
domain_of:
- DataProvider
- DataConsumer
range: string

```
</details>