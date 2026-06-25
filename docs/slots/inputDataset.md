

# Slot: inputDataset 


_Source datasets used by the data product_





URI: [dds:slot/inputDataset](https://w3id.org/dds/slot/inputDataset)
Alias: inputDataset

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [Dataset](../classes/Dataset.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:inputDataset |
| native | dds:inputDataset |




## LinkML Source

<details>
```yaml
name: inputDataset
description: Source datasets used by the data product
from_schema: https://w3id.org/dds
rank: 1000
alias: inputDataset
owner: DataProduct
domain_of:
- DataProduct
range: Dataset
multivalued: true
inlined: true
inlined_as_list: true

```
</details>