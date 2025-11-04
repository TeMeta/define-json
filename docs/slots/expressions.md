

# Slot: expressions 



URI: [odm:slot/expressions](https://cdisc.org/odm2/slot/expressions)
Alias: expressions

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items.<br>Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions. |  no  |
| [Condition](../classes/Condition.md) | A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions. |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [RangeCheck](../classes/RangeCheck.md) | A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:expressions |
| native | odm:expressions |




## LinkML Source

<details>
```yaml
name: expressions
alias: expressions
domain_of:
- Condition
- RangeCheck
- Method

```
</details>