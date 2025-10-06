# Enum: MethodType 




_An enumeration that defines the types of computational methods available for data processing_



URI: [MethodType](../enums/MethodType.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Computation | None | Mathematical computation using values of other items. |
| Imputation | None | Assignment of a value based on a estimation (imputation) procedure. |
| Transformation | None | Transformation of the item's value according to a standard algorithm, such as a change in units. |









## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: MethodType
description: An enumeration that defines the types of computational methods available
  for data processing
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  Computation:
    text: Computation
    description: Mathematical computation using values of other items.
  Imputation:
    text: Imputation
    description: Assignment of a value based on a estimation (imputation) procedure.
  Transformation:
    text: Transformation
    description: Transformation of the item's value according to a standard algorithm,
      such as a change in units.

```
</details>
