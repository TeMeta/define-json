# Enum: PolicyType 




_ODRL policy subtypes._



URI: [odm:enum/PolicyType](https://cdisc.org/odm2/enum/PolicyType)

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


* from schema: https://cdisc.org/data-definition-spec






## LinkML Source

<details>
```yaml
name: PolicyType
description: ODRL policy subtypes.
from_schema: https://cdisc.org/data-definition-spec
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