

# Slot: properties 


_Properties of the reified object, which can be other governed elements or simple values_





URI: [odm:slot/properties](https://cdisc.org/odm2/slot/properties)
Alias: properties

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ReifiedConcept](../classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and referenceable, showing how different data implementations represent the same underlying meanings through a star schema structure with multiple properties |  no  |







## Properties

* Range: [ConceptProperty](../classes/ConceptProperty.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:properties |
| native | odm:properties |




## LinkML Source

<details>
```yaml
name: properties
description: Properties of the reified object, which can be other governed elements
  or simple values
from_schema: https://cdisc.org/define-json
rank: 1000
alias: properties
owner: ReifiedConcept
domain_of:
- ReifiedConcept
range: ConceptProperty
multivalued: true
inlined: true
inlined_as_list: true

```
</details>