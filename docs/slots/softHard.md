

# Slot: softHard 


_Indicates whether a validation check is an error ("Hard") or a warning ("Soft")_





URI: [odm:slot/softHard](https://cdisc.org/odm2/slot/softHard)
Alias: softHard

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RangeCheck](../classes/RangeCheck.md) | A validation element that performs a simple comparison check between a refere... |  no  |







## Properties

* Range: [SoftHard](../enums/SoftHard.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:softHard |
| native | odm:softHard |




## LinkML Source

<details>
```yaml
name: softHard
description: Indicates whether a validation check is an error ("Hard") or a warning
  ("Soft")
from_schema: https://cdisc.org/define-json
rank: 1000
alias: softHard
owner: RangeCheck
domain_of:
- RangeCheck
range: SoftHard

```
</details>