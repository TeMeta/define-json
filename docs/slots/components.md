

# Slot: components 


_The components that make up this component list_





URI: [dds:slot/components](https://w3id.org/dds/slot/components)
Alias: components

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ComponentList](../classes/ComponentList.md) | An abstract definition that specifies a list of components within a data structure definition, including various descriptor types |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[Measure](../classes/Measure.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[DataAttribute](../classes/DataAttribute.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:components |
| native | dds:components |




## LinkML Source

<details>
```yaml
name: components
description: The components that make up this component list
from_schema: https://w3id.org/dds
rank: 1000
alias: components
owner: ComponentList
domain_of:
- ComponentList
range: string
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: Measure
- range: Dimension
- range: DataAttribute

```
</details>