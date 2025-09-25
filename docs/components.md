

# Slot: components 


_The components that make up this component list_





URI: [odm:components](https://cdisc.org/odm2/components)
Alias: components

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ComponentList](ComponentList.md) | An abstract definition that specifies a list of components within a data stru... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[Measure](Measure.md)&nbsp;or&nbsp;<br />[Dimension](Dimension.md)&nbsp;or&nbsp;<br />[DataAttribute](DataAttribute.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:components |
| native | odm:components |




## LinkML Source

<details>
```yaml
name: components
description: The components that make up this component list
from_schema: https://cdisc.org/define-json
rank: 1000
alias: components
owner: ComponentList
domain_of:
- ComponentList
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: Measure
- range: Dimension
- range: DataAttribute

```
</details>