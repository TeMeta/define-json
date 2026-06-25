

# Slot: provisionAgreements 



URI: [dds:slot/provisionAgreements](https://w3id.org/dds/slot/provisionAgreements)
Alias: provisionAgreements

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [DataConsumer](../classes/DataConsumer.md) | An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:provisionAgreements |
| native | dds:provisionAgreements |




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