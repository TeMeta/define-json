

# Slot: dataProductOwner 


_The person or team accountable for this data product_





URI: [odm:dataProductOwner](https://cdisc.org/odm2/dataProductOwner)
Alias: dataProductOwner

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[User](User.md)&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md)





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