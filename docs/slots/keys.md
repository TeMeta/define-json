

# Slot: keys 


_Series and Group keys in the data that are associated with dimensions in this structure_





URI: [dds:slot/keys](https://w3id.org/dds/slot/keys)
Alias: keys

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[SeriesKey](../classes/SeriesKey.md)&nbsp;or&nbsp;<br />[GroupKey](../classes/GroupKey.md)

* Multivalued: True

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:keys |
| native | dds:keys |




## LinkML Source

<details>
```yaml
name: keys
description: Series and Group keys in the data that are associated with dimensions
  in this structure
from_schema: https://w3id.org/dds
rank: 1000
alias: keys
owner: Dataset
domain_of:
- Dataset
range: string
required: true
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: SeriesKey
- range: GroupKey

```
</details>