

# Slot: hasPolicy 



URI: [dds:slot/hasPolicy](https://w3id.org/dds/slot/hasPolicy)
Alias: hasPolicy

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:hasPolicy |
| native | dds:hasPolicy |




## LinkML Source

<details>
```yaml
name: hasPolicy
alias: hasPolicy
domain_of:
- Dataset
- DataProduct
- ProvisionAgreement
range: string

```
</details>