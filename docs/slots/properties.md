

# Slot: properties 


_Properties of the reified object, which can be other governed elements or simple values_





URI: [dds:slot/properties](https://w3id.org/dds/slot/properties)
Alias: properties

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Concept](../classes/Concept.md) | An abstract concept that can be referenced and specialised by data implementations. Holds ConceptProperties describing the concept's expected data shape. Multiple ItemGroups or Items can implement the same Concept, allowing standard biomedical concepts to be implemented differently across studies while remaining semantically aligned. |  no  |






## Properties

* Range: [ConceptProperty](../classes/ConceptProperty.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:properties |
| native | dds:properties |




## LinkML Source

<details>
```yaml
name: properties
description: Properties of the reified object, which can be other governed elements
  or simple values
from_schema: https://w3id.org/dds
rank: 1000
alias: properties
owner: Concept
domain_of:
- Concept
range: ConceptProperty
multivalued: true
inlined: true
inlined_as_list: true

```
</details>