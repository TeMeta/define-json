

# Slot: keyValues 


_List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI_





URI: [dds:slot/keyValues](https://w3id.org/dds/slot/keyValues)
Alias: keyValues

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupKey](../classes/GroupKey.md) | A dimension subset that represents collections of dimensions that are subsets of the full dimension set, distinct from SeriesKey which includes Time dimensions |  no  |
| [SeriesKey](../classes/SeriesKey.md) | A unique identifier that comprises the cross-product of dimension values including Time to identify observations, representing dimensions shared by all observations in a conceptual series |  no  |
| [DatasetKey](../classes/DatasetKey.md) | An abstract identifier that comprises the cross-product of dimension values to identify a specific cross-section |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:keyValues |
| native | dds:keyValues |




## LinkML Source

<details>
```yaml
name: keyValues
description: List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI
from_schema: https://w3id.org/dds
rank: 1000
alias: keyValues
owner: DatasetKey
domain_of:
- DatasetKey
range: string

```
</details>