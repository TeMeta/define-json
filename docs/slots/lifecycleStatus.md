

# Slot: lifecycleStatus 


_Current lifecycle status of the data product_





URI: [odm:slot/lifecycleStatus](https://cdisc.org/odm2/slot/lifecycleStatus)
Alias: lifecycleStatus

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle |  no  |







## Properties

* Range: [DataProductLifecycleStatus](../enums/DataProductLifecycleStatus.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:lifecycleStatus |
| native | odm:lifecycleStatus |




## LinkML Source

<details>
```yaml
name: lifecycleStatus
description: Current lifecycle status of the data product
from_schema: https://cdisc.org/define-json
rank: 1000
alias: lifecycleStatus
owner: DataProduct
domain_of:
- DataProduct
range: DataProductLifecycleStatus

```
</details>