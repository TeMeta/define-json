

# Slot: validationPredicates 


_Validation predicates that constrain this parameter's value beyond controlled terminology. All must be satisfied (AND logic). Distinct from applicableWhen which determines if the parameter is needed at all._





URI: [dds:slot/validationPredicates](https://w3id.org/dds/slot/validationPredicates)
Alias: validationPredicates

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |






## Properties

* Range: [LogicalPredicate](../classes/LogicalPredicate.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:validationPredicates |
| native | dds:validationPredicates |




## LinkML Source

<details>
```yaml
name: validationPredicates
description: Validation predicates that constrain this parameter's value beyond controlled
  terminology. All must be satisfied (AND logic). Distinct from applicableWhen which
  determines if the parameter is needed at all.
from_schema: https://w3id.org/dds
rank: 1000
alias: validationPredicates
owner: Parameter
domain_of:
- Parameter
range: LogicalPredicate
multivalued: true
inlined: false

```
</details>