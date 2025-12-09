

# Slot: event 


_The ID of the event in a Schedule._





URI: [odm:slot/event](https://cdisc.org/odm2/slot/event)
Alias: event

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned encounters or adverse events |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:event |
| native | odm:event |




## LinkML Source

<details>
```yaml
name: event
description: The ID of the event in a Schedule.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: event
owner: NominalOccurrence
domain_of:
- NominalOccurrence
range: string
required: false

```
</details>