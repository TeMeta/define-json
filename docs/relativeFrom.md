

# Slot: relativeFrom 


_Reference to the event or occurrence that this timing is relative to._





URI: [odm:relativeFrom](https://cdisc.org/odm2/relativeFrom)
Alias: relativeFrom

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Timing](Timing.md) | A temporal element that describes the timing of an event or occurrence, which... |  no  |







## Properties

* Range: [NominalOccurrence](NominalOccurrence.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:relativeFrom |
| native | odm:relativeFrom |




## LinkML Source

<details>
```yaml
name: relativeFrom
description: Reference to the event or occurrence that this timing is relative to.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: relativeFrom
owner: Timing
domain_of:
- Timing
range: NominalOccurrence

```
</details>