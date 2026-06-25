

# Slot: constraint 


_Conditions that narrow when/how the rule applies (odrl:constraint)_





URI: [dds:slot/constraint](https://w3id.org/dds/slot/constraint)
Alias: constraint

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |






## Properties

* Range: [Constraint](../classes/Constraint.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:constraint |
| native | dds:constraint |
| exact | odrl:constraint |




## LinkML Source

<details>
```yaml
name: constraint
description: Conditions that narrow when/how the rule applies (odrl:constraint)
from_schema: https://w3id.org/dds
exact_mappings:
- odrl:constraint
rank: 1000
alias: constraint
owner: Rule
domain_of:
- Rule
range: Constraint
multivalued: true
inlined: true
inlined_as_list: true

```
</details>