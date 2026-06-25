

# Slot: consumesDataFrom 


_The Dataflows that this consumer receives data from_





URI: [dds:slot/consumesDataFrom](https://w3id.org/dds/slot/consumesDataFrom)
Alias: consumesDataFrom

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataConsumer](../classes/DataConsumer.md) | An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider. |  no  |






## Properties

* Range: [Dataflow](../classes/Dataflow.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:consumesDataFrom |
| native | dds:consumesDataFrom |




## LinkML Source

<details>
```yaml
name: consumesDataFrom
description: The Dataflows that this consumer receives data from
from_schema: https://w3id.org/dds
rank: 1000
alias: consumesDataFrom
owner: DataConsumer
domain_of:
- DataConsumer
range: Dataflow
multivalued: true

```
</details>