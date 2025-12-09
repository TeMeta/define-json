

# Slot: concepts 


_Structured Concepts defined in this version of the metadata_





URI: [odm:slot/concepts](https://cdisc.org/odm2/slot/concepts)
Alias: concepts

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |






## Properties

* Range: [ReifiedConcept](../classes/ReifiedConcept.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:concepts |
| native | odm:concepts |




## LinkML Source

<details>
```yaml
name: concepts
description: Structured Concepts defined in this version of the metadata
from_schema: https://cdisc.org/define-json
rank: 1000
alias: concepts
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: ReifiedConcept
multivalued: true

```
</details>