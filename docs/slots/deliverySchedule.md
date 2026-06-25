

# Slot: deliverySchedule 


_Recurring transfer/delivery schedule agreed for this flow. The domain-neutral default is an ISO-8601 repeating interval string (e.g. "R/2025-01-01/P1M"); use a Timing object only when delivery must be anchored to a clinical occurrence. Agreement-level schedule; concrete reporting periods of each delivered Dataset are carried by IsSdmxDataset.reportingBegin/reportingEnd/dataExtractionDate._





URI: [dds:slot/deliverySchedule](https://w3id.org/dds/slot/deliverySchedule)
Alias: deliverySchedule

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[Timing](../classes/Timing.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:deliverySchedule |
| native | dds:deliverySchedule |




## LinkML Source

<details>
```yaml
name: deliverySchedule
description: Recurring transfer/delivery schedule agreed for this flow. The domain-neutral
  default is an ISO-8601 repeating interval string (e.g. "R/2025-01-01/P1M"); use
  a Timing object only when delivery must be anchored to a clinical occurrence. Agreement-level
  schedule; concrete reporting periods of each delivered Dataset are carried by IsSdmxDataset.reportingBegin/reportingEnd/dataExtractionDate.
from_schema: https://w3id.org/dds
rank: 1000
alias: deliverySchedule
owner: Dataflow
domain_of:
- Dataflow
range: string
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: string
- range: Timing

```
</details>