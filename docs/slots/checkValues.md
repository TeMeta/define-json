

# Slot: checkValues 


_Values to compare against_





URI: [dds:slot/checkValues](https://w3id.org/dds/slot/checkValues)
Alias: checkValues

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RangeCheck](../classes/RangeCheck.md) | A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result |  no  |






## Properties

* Range: [String](../types/String.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:checkValues |
| native | dds:checkValues |




## LinkML Source

<details>
```yaml
name: checkValues
description: Values to compare against
from_schema: https://w3id.org/dds
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