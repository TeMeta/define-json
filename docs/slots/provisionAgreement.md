

# Slot: provisionAgreement 


_Reference(s) to standalone Data Transfer Agreements (ProvisionAgreement) that govern this product's flows. Referenced by OID/URI, not embedded, so the agreement remains an independently maintained artifact._





URI: [dds:slot/provisionAgreement](https://w3id.org/dds/slot/provisionAgreement)
Alias: provisionAgreement

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [ProvisionAgreement](../classes/ProvisionAgreement.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:provisionAgreement |
| native | dds:provisionAgreement |




## LinkML Source

<details>
```yaml
name: provisionAgreement
description: Reference(s) to standalone Data Transfer Agreements (ProvisionAgreement)
  that govern this product's flows. Referenced by OID/URI, not embedded, so the agreement
  remains an independently maintained artifact.
from_schema: https://w3id.org/dds
rank: 1000
alias: provisionAgreement
owner: DataProduct
domain_of:
- DataProduct
range: ProvisionAgreement
multivalued: true
inlined: false

```
</details>