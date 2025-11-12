

# Slot: timing 


_A named event reference, that can nest further named timing references._





URI: [odm:slot/timing](https://cdisc.org/odm2/slot/timing)
Alias: timing

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned encounters or adverse events |  no  |







## Properties

* Range: [Timing](../classes/Timing.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:timing |
| native | odm:timing |




## LinkML Source

<details>
```yaml
name: timing
description: A named event reference, that can nest further named timing references.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: timing
owner: NominalOccurrence
domain_of:
- NominalOccurrence
range: Timing
required: true

```
</details>