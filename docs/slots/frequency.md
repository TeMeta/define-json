

# Slot: frequency 


_Frequency. Use dose frequency terminology e.g. "BID" if applicable._





URI: [odm:slot/frequency](https://cdisc.org/odm2/slot/frequency)
Alias: frequency

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:frequency |
| native | odm:frequency |




## LinkML Source

<details>
```yaml
name: frequency
description: Frequency. Use dose frequency terminology e.g. "BID" if applicable.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: frequency
owner: Timing
domain_of:
- Timing
range: string

```
</details>