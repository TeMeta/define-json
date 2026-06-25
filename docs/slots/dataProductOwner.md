

# Slot: dataProductOwner 


_The person or team accountable for this data product_





URI: [dds:slot/dataProductOwner](https://w3id.org/dds/slot/dataProductOwner)
Alias: dataProductOwner

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:dataProductOwner |
| native | dds:dataProductOwner |
| exact | prov:wasAttributedTo |




## LinkML Source

<details>
```yaml
name: dataProductOwner
description: The person or team accountable for this data product
from_schema: https://w3id.org/dds
exact_mappings:
- prov:wasAttributedTo
rank: 1000
alias: dataProductOwner
owner: DataProduct
domain_of:
- DataProduct
range: string
any_of:
- range: User
- range: Organization
- range: string

```
</details>