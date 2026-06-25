

# Slot: relativeFrom 


_The protocol anchor from which this timing is measured. Either a TimingLandmark or a USDM ScheduledActivityInstance OID reference._





URI: [dds:slot/relativeFrom](https://w3id.org/dds/slot/relativeFrom)
Alias: relativeFrom

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
| self | dds:relativeFrom |
| native | dds:relativeFrom |




## LinkML Source

<details>
```yaml
name: relativeFrom
description: The protocol anchor from which this timing is measured. Either a TimingLandmark
  or a USDM ScheduledActivityInstance OID reference.
from_schema: https://w3id.org/dds
rank: 1000
alias: relativeFrom
owner: Timing
domain_of:
- Timing
range: string
any_of:
- range: TimingLandmark
- range: string

```
</details>