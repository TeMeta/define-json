

# Slot: implementsPredicate 


_Reference to an external (e.g. USDM) predicate/condition definition that this implements_





URI: [dds:slot/implementsPredicate](https://w3id.org/dds/slot/implementsPredicate)
Alias: implementsPredicate

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LogicalPredicate](../classes/LogicalPredicate.md) | A reusable, composable, and nestable logical expression resolving to a boolean. Used for applicability conditions, validation rules, eligibility criteria, and skip logic. This is a data-model predicate — not a clinical condition (diagnosis). Implements usdm:Condition (the study-design predicate, distinct from the clinical FHIR Condition resource). |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:implementsPredicate |
| native | dds:implementsPredicate |




## LinkML Source

<details>
```yaml
name: implementsPredicate
description: Reference to an external (e.g. USDM) predicate/condition definition that
  this implements
from_schema: https://w3id.org/dds
rank: 1000
alias: implementsPredicate
owner: LogicalPredicate
domain_of:
- LogicalPredicate
range: string

```
</details>