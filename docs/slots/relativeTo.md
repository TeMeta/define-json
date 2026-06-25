

# Slot: relativeTo 


_The protocol anchor this timing is relative to. Either a TimingLandmark (well-known protocol event such as RANDOMIZATION or FIRST_DOSE) or a free-form OID/identifier referencing a USDM ScheduledActivityInstance._





URI: [dds:slot/relativeTo](https://w3id.org/dds/slot/relativeTo)
Alias: relativeTo

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[TimingLandmark](../enums/TimingLandmark.md)&nbsp;or&nbsp;<br />[String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:relativeTo |
| native | dds:relativeTo |




## LinkML Source

<details>
```yaml
name: relativeTo
description: The protocol anchor this timing is relative to. Either a TimingLandmark
  (well-known protocol event such as RANDOMIZATION or FIRST_DOSE) or a free-form OID/identifier
  referencing a USDM ScheduledActivityInstance.
from_schema: https://w3id.org/dds
rank: 1000
alias: relativeTo
owner: Timing
domain_of:
- Timing
range: string
any_of:
- range: TimingLandmark
- range: string

```
</details>