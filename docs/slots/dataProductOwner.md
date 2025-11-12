

# Slot: dataProductOwner 


_The person or team accountable for this data product_





URI: [odm:slot/dataProductOwner](https://cdisc.org/odm2/slot/dataProductOwner)
Alias: dataProductOwner

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:dataProductOwner |
| native | odm:dataProductOwner |
| exact | prov:wasAttributedTo |




## LinkML Source

<details>
```yaml
name: dataProductOwner
description: The person or team accountable for this data product
from_schema: https://cdisc.org/define-json
exact_mappings:
- prov:wasAttributedTo
rank: 1000
alias: dataProductOwner
owner: DataProduct
domain_of:
- DataProduct
any_of:
- range: User
- range: Organization
- range: string

```
</details>