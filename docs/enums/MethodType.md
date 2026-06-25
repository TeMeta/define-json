# Enum: MethodType 




_An enumeration that defines the types of computational methods available for data processing_



URI: [dds:enum/MethodType](https://w3id.org/dds/enum/MethodType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Computation | None | Mathematical computation using values of other items. |
| Imputation | None | Assignment of a value based on a estimation (imputation) procedure. |
| Transformation | None | Transformation of the item's value according to a standard algorithm, such as a change in units. |
| Analysis | None | Creation of analysis results dataset. |
| Display | None | Creation of rendered output for display. |








## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: MethodType
description: An enumeration that defines the types of computational methods available
  for data processing
from_schema: https://w3id.org/dds
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
  Analysis:
    text: Analysis
    description: Creation of analysis results dataset.
  Display:
    text: Display
    description: Creation of rendered output for display.

```
</details>