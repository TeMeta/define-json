

# Slot: subject 


_The starting element of the relationship (e.g., an Item or ItemGroup)._





URI: [odm:slot/subject](https://cdisc.org/odm2/slot/subject)
Alias: subject

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
| self | odm:subject |
| native | odm:subject |




## LinkML Source

<details>
```yaml
name: subject
description: The starting element of the relationship (e.g., an Item or ItemGroup).
from_schema: https://cdisc.org/define-json
rank: 1000
alias: subject
owner: Relationship
domain_of:
- Relationship
range: IdentifiableElement
required: true

```
</details>