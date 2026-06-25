

# Slot: policyType 


_ODRL policy subtype (Set, Offer, Agreement)_





URI: [dds:slot/policyType](https://w3id.org/dds/slot/policyType)
Alias: policyType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |






## Properties

* Range: [PolicyType](../enums/PolicyType.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:policyType |
| native | dds:policyType |




## LinkML Source

<details>
```yaml
name: policyType
description: ODRL policy subtype (Set, Offer, Agreement)
from_schema: https://w3id.org/dds
rank: 1000
ifabsent: PolicyType(Agreement)
alias: policyType
owner: Policy
domain_of:
- Policy
range: PolicyType

```
</details>