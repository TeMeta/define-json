

# Slot: expressions 



URI: [dds:slot/expressions](https://w3id.org/dds/slot/expressions)
Alias: expressions

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [Check](../classes/Check.md) | A reusable validation check included in the metadata package, such as a published CORE rule. Linked many-to-many by reference to the metadata and/or data elements it applies to, and optionally citing an external published rule so checks stay reusable and loosely coupled. Distinct from RangeCheck, which is an inline executable comparison; a RangeCheck may implement a Check. |  no  |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items.<br>Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions. |  no  |
| [LogicalPredicate](../classes/LogicalPredicate.md) | A reusable, composable, and nestable logical expression resolving to a boolean. Used for applicability conditions, validation rules, eligibility criteria, and skip logic. This is a data-model predicate — not a clinical condition (diagnosis). Implements usdm:Condition (the study-design predicate, distinct from the clinical FHIR Condition resource). |  no  |
| [RangeCheck](../classes/RangeCheck.md) | A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:expressions |
| native | dds:expressions |




## LinkML Source

<details>
```yaml
name: expressions
alias: expressions
domain_of:
- LogicalPredicate
- RangeCheck
- Check
- Method
range: string

```
</details>