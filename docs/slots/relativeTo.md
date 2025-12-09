

# Slot: relativeTo 


_Reference to the event or occurrence that this timing is relative to._





URI: [odm:slot/relativeTo](https://cdisc.org/odm2/slot/relativeTo)
Alias: relativeTo

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |






## Properties

* Range: [NominalOccurrence](../classes/NominalOccurrence.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:relativeTo |
| native | odm:relativeTo |




## LinkML Source

<details>
```yaml
name: relativeTo
description: Reference to the event or occurrence that this timing is relative to.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: relativeTo
owner: Timing
domain_of:
- Timing
range: NominalOccurrence

```
</details>