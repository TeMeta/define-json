

# Slot: required 


_Indicates whether this parameter must be provided when the  containing expression is evaluated (technical constraint)._





URI: [odm:slot/required](https://cdisc.org/odm2/slot/required)
Alias: required

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |






## Properties

* Range: [Boolean](../types/Boolean.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:required |
| native | odm:required |




## LinkML Source

<details>
```yaml
name: required
description: Indicates whether this parameter must be provided when the  containing
  expression is evaluated (technical constraint).
from_schema: https://cdisc.org/define-json
rank: 1000
ifabsent: 'False'
alias: required
owner: Parameter
domain_of:
- Parameter
range: boolean

```
</details>