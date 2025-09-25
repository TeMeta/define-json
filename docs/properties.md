

# Slot: properties 


_Properties of the reified object, which can be other governed elements or simple values_





URI: [odm:properties](https://cdisc.org/odm2/properties)
Alias: properties

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ReifiedConcept](ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |  no  |







## Properties

* Range: [ConceptProperty](ConceptProperty.md)

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