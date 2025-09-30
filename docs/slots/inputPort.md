

# Slot: inputPort 


_Services that provide input into this data product_





URI: [odm:slot/inputPort](https://cdisc.org/odm2/slot/inputPort)
Alias: inputPort

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |







## Properties

* Range: [DataService](../classes/DataService.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:inputPort |
| native | odm:inputPort |




## LinkML Source

<details>
```yaml
name: inputPort
description: Services that provide input into this data product
from_schema: https://cdisc.org/define-json
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