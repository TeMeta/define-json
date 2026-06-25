

# Slot: inputPort 


_Services that provide input into this data product_





URI: [dds:slot/inputPort](https://w3id.org/dds/slot/inputPort)
Alias: inputPort

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [DataService](../classes/DataService.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:inputPort |
| native | dds:inputPort |




## LinkML Source

<details>
```yaml
name: inputPort
description: Services that provide input into this data product
from_schema: https://w3id.org/dds
rank: 1000
alias: inputPort
owner: DataProduct
domain_of:
- DataProduct
range: DataService
multivalued: true
inlined: true
inlined_as_list: true

```
</details>