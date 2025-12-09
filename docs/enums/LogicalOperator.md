# Enum: LogicalOperator 




_Logical operators for combining conditions in Boolean expressions. For complex expressions, use the EXPRESSION value._



URI: [odm:enum/LogicalOperator](https://cdisc.org/odm2/enum/LogicalOperator)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| EXPRESSION | None | Evaluate condition using expression. Default if expression is present. |
| AND | None | All child conditions must be true (all_of). Default if expression is not present. |
| OR | None | At least one child condition must be true (any_of). |
| NOT | None | Negates the child condition(s) (not_any_of). |




## Slots

| Name | Description |
| ---  | --- |
| [operator](../slots/operator.md) | Logical operator for combining child conditions or range checks. Defaults to ALL if not specified. |





## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: LogicalOperator
description: Logical operators for combining conditions in Boolean expressions. For
  complex expressions, use the EXPRESSION value.
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  EXPRESSION:
    text: EXPRESSION
    description: Evaluate condition using expression. Default if expression is present.
  AND:
    text: AND
    description: All child conditions must be true (all_of). Default if expression
      is not present.
  OR:
    text: OR
    description: At least one child condition must be true (any_of).
  NOT:
    text: NOT
    description: Negates the child condition(s) (not_any_of).

```
</details>