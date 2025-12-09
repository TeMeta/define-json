

# Slot: providesDataFor 


_The Dataflows that this provider supplies data for_





URI: [odm:slot/providesDataFor](https://cdisc.org/odm2/slot/providesDataFor)
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


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:providesDataFor |
| native | odm:providesDataFor |




## LinkML Source

<details>
```yaml
name: providesDataFor
description: The Dataflows that this provider supplies data for
from_schema: https://cdisc.org/define-json
rank: 1000
alias: providesDataFor
owner: DataProvider
domain_of:
- DataProvider
range: Dataflow
multivalued: true

```
</details>