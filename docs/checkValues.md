

# Slot: checkValues 


_Values to compare against_





URI: [odm:checkValues](https://cdisc.org/odm2/checkValues)
Alias: checkValues

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RangeCheck](RangeCheck.md) | A validation element that performs a simple comparison check between a refere... |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:checkValues |
| native | odm:checkValues |




## LinkML Source

<details>
```yaml
name: checkValues
description: Values to compare against
from_schema: https://cdisc.org/define-json
rank: 1000
alias: checkValues
owner: RangeCheck
domain_of:
- RangeCheck
range: string
multivalued: true
inlined: true
inlined_as_list: true

```
</details>