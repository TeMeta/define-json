

# Slot: selection 


_Machine-executable instructions for selecting data from the resource._





URI: [odm:slot/selection](https://cdisc.org/odm2/slot/selection)
Alias: selection

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |







## Properties

* Range: [FormalExpression](../classes/FormalExpression.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:selection |
| native | odm:selection |




## LinkML Source

<details>
```yaml
name: selection
description: Machine-executable instructions for selecting data from the resource.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: selection
owner: Resource
domain_of:
- Resource
range: FormalExpression
multivalued: true
inlined: true
inlined_as_list: true

```
</details>