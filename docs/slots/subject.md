

# Slot: subject 


_The starting element of the relationship (e.g., an Item or ItemGroup)._





URI: [dds:slot/subject](https://w3id.org/dds/slot/subject)
Alias: subject

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Relationship](../classes/Relationship.md) | A semantic link that defines connections between elements such as Items or ItemGroups, capturing relationships like "is the unit for" or "assesses seriousness of" |  no  |






## Properties

* Range: [IdentifiableElement](../classes/IdentifiableElement.md)

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:subject |
| native | dds:subject |




## LinkML Source

<details>
```yaml
name: subject
description: The starting element of the relationship (e.g., an Item or ItemGroup).
from_schema: https://w3id.org/dds
rank: 1000
alias: subject
owner: Relationship
domain_of:
- Relationship
range: IdentifiableElement
required: true

```
</details>