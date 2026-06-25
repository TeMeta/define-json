

# Slot: required 


_Indicates whether this parameter must be provided when the  containing expression is evaluated (technical constraint)._





URI: [dds:slot/required](https://w3id.org/dds/slot/required)
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


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:required |
| native | dds:required |




## LinkML Source

<details>
```yaml
name: required
description: Indicates whether this parameter must be provided when the  containing
  expression is evaluated (technical constraint).
from_schema: https://w3id.org/dds
rank: 1000
ifabsent: 'False'
alias: required
owner: Parameter
domain_of:
- Parameter
range: boolean

```
</details>