

# Slot: lifecycleStatus 


_Current lifecycle status of the data product_





URI: [dds:slot/lifecycleStatus](https://w3id.org/dds/slot/lifecycleStatus)
Alias: lifecycleStatus

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [DataProductLifecycleStatus](../enums/DataProductLifecycleStatus.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:lifecycleStatus |
| native | dds:lifecycleStatus |




## LinkML Source

<details>
```yaml
name: lifecycleStatus
description: Current lifecycle status of the data product
from_schema: https://w3id.org/dds
rank: 1000
alias: lifecycleStatus
owner: DataProduct
domain_of:
- DataProduct
range: DataProductLifecycleStatus

```
</details>