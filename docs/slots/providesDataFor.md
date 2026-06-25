

# Slot: providesDataFor 


_The Dataflows that this provider supplies data for_





URI: [dds:slot/providesDataFor](https://w3id.org/dds/slot/providesDataFor)
Alias: providesDataFor

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |






## Properties

* Range: [Dataflow](../classes/Dataflow.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:providesDataFor |
| native | dds:providesDataFor |




## LinkML Source

<details>
```yaml
name: providesDataFor
description: The Dataflows that this provider supplies data for
from_schema: https://w3id.org/dds
rank: 1000
alias: providesDataFor
owner: DataProvider
domain_of:
- DataProvider
range: Dataflow
multivalued: true

```
</details>