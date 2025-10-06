

# Slot: recalled 


_Indicates whether the timing is recalled or not (recalled timings are less reliable)._





URI: [odm:slot/recalled](https://cdisc.org/odm2/slot/recalled)
Alias: recalled

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |







## Properties

* Range: [Boolean](../types/Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:recalled |
| native | odm:recalled |




## LinkML Source

<details>
```yaml
name: recalled
description: Indicates whether the timing is recalled or not (recalled timings are
  less reliable).
from_schema: https://cdisc.org/define-json
rank: 1000
alias: recalled
owner: Timing
domain_of:
- Timing
range: boolean

```
</details>