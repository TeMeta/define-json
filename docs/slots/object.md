

# Slot: object 


_The ending element of the relationship._





URI: [odm:slot/object](https://cdisc.org/odm2/slot/object)
Alias: object

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Relationship](../classes/Relationship.md) | A semantic link that defines connections between elements such as Items or It... |  no  |







## Properties

* Range: [IdentifiableElement](../classes/IdentifiableElement.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:object |
| native | odm:object |




## LinkML Source

<details>
```yaml
name: object
description: The ending element of the relationship.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: object
owner: Relationship
domain_of:
- Relationship
range: IdentifiableElement
required: true

```
</details>