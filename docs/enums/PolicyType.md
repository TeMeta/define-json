# Enum: PolicyType 




_ODRL policy subtypes._



URI: [dds:enum/PolicyType](https://w3id.org/dds/enum/PolicyType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Set | odrl:Set |  |
| Offer | odrl:Offer |  |
| Agreement | odrl:Agreement |  |




## Slots

| Name | Description |
| ---  | --- |
| [policyType](../slots/policyType.md) | ODRL policy subtype (Set, Offer, Agreement) |





## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: PolicyType
description: ODRL policy subtypes.
from_schema: https://w3id.org/dds
rank: 1000
permissible_values:
  Set:
    text: Set
    meaning: odrl:Set
  Offer:
    text: Offer
    meaning: odrl:Offer
  Agreement:
    text: Agreement
    meaning: odrl:Agreement

```
</details>