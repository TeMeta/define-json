

# Slot: keyValues 


_List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI_





URI: [odm:keyValues](https://cdisc.org/odm2/keyValues)
Alias: keyValues

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SeriesKey](SeriesKey.md) | A unique identifier that comprises the cross-product of dimension values incl... |  no  |
| [GroupKey](GroupKey.md) | A dimension subset that represents collections of dimensions that are subsets... |  no  |
| [DatasetKey](DatasetKey.md) | An abstract identifier that comprises the cross-product of dimension values t... |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:keyValues |
| native | odm:keyValues |




## LinkML Source

<details>
```yaml
name: keyValues
description: List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI
from_schema: https://cdisc.org/define-json
rank: 1000
alias: keyValues
owner: DatasetKey
domain_of:
- DatasetKey

```
</details>