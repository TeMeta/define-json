

# Slot: providesDataFor 


_The Dataflows that this provider supplies data for_





URI: [odm:providesDataFor](https://cdisc.org/odm2/providesDataFor)
Alias: providesDataFor

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |  no  |







## Properties

* Range: [Dataflow](Dataflow.md)

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