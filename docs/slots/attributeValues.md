

# Slot: attributeValues 


_Association to the Attribute Values relating to Key_





URI: [odm:slot/attributeValues](https://cdisc.org/odm2/slot/attributeValues)
Alias: attributeValues

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupKey](../classes/GroupKey.md) | A dimension subset that represents collections of dimensions that are subsets of the full dimension set, distinct from SeriesKey which includes Time dimensions |  no  |
| [DatasetKey](../classes/DatasetKey.md) | An abstract identifier that comprises the cross-product of dimension values to identify a specific cross-section |  no  |
| [SeriesKey](../classes/SeriesKey.md) | A unique identifier that comprises the cross-product of dimension values including Time to identify observations, representing dimensions shared by all observations in a conceptual series |  no  |






## Properties

* Range: NONE




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:attributeValues |
| native | odm:attributeValues |




## LinkML Source

<details>
```yaml
name: attributeValues
description: Association to the Attribute Values relating to Key
from_schema: https://cdisc.org/define-json
rank: 1000
alias: attributeValues
owner: DatasetKey
domain_of:
- DatasetKey

```
</details>