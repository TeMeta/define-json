

# Slot: outputDataset 


_Output datasets produced by the data product_





URI: [dds:slot/outputDataset](https://w3id.org/dds/slot/outputDataset)
Alias: outputDataset

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
| self | dds:outputDataset |
| native | dds:outputDataset |




## LinkML Source

<details>
```yaml
name: outputDataset
description: Output datasets produced by the data product
from_schema: https://w3id.org/dds
rank: 1000
alias: outputDataset
owner: DataProduct
domain_of:
- DataProduct
range: Dataset
multivalued: true
inlined: true
inlined_as_list: true

```
</details>