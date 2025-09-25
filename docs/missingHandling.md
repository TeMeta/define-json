

# Slot: missingHandling 


_The method for handling missing values in the measure property_





URI: [odm:missingHandling](https://cdisc.org/odm2/missingHandling)
Alias: missingHandling

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataAttribute](DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |  no  |
| [CubeComponent](CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |  no  |
| [Dimension](Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [Measure](Measure.md) | A data cube property that describes a measurable quantity or value |  no  |







## Properties

* Range: [Method](Method.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:missingHandling |
| native | odm:missingHandling |




## LinkML Source

<details>
```yaml
name: missingHandling
description: The method for handling missing values in the measure property
from_schema: https://cdisc.org/define-json
rank: 1000
alias: missingHandling
owner: CubeComponent
domain_of:
- CubeComponent
range: Method

```
</details>