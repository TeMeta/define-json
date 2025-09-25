

# Slot: outputPort 


_Services that expose output from this data product_





URI: [odm:outputPort](https://cdisc.org/odm2/outputPort)
Alias: outputPort

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |







## Properties

* Range: [DataService](DataService.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:outputPort |
| native | odm:outputPort |




## LinkML Source

<details>
```yaml
name: outputPort
description: Services that expose output from this data product
from_schema: https://cdisc.org/define-json
rank: 1000
alias: outputPort
owner: DataProduct
domain_of:
- DataProduct
range: DataService
multivalued: true
inlined: true
inlined_as_list: true

```
</details>