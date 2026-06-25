

# Slot: rangeChecks 



URI: [dds:slot/rangeChecks](https://w3id.org/dds/slot/rangeChecks)
Alias: rangeChecks

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LogicalPredicate](../classes/LogicalPredicate.md) | A reusable, composable, and nestable logical expression resolving to a boolean. Used for applicability conditions, validation rules, eligibility criteria, and skip logic. This is a data-model predicate — not a clinical condition (diagnosis). Implements usdm:Condition (the study-design predicate, distinct from the clinical FHIR Condition resource). |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:rangeChecks |
| native | dds:rangeChecks |




## LinkML Source

<details>
```yaml
name: rangeChecks
alias: rangeChecks
domain_of:
- Item
- LogicalPredicate
range: string

```
</details>