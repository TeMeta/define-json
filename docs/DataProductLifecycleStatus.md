# Enum: DataProductLifecycleStatus 




_An enumeration that defines the lifecycle stages for a DataProduct_



URI: [DataProductLifecycleStatus](DataProductLifecycleStatus.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Ideation | None |  |
| Design | None |  |
| Build | None |  |
| Deploy | None |  |
| Consume | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [lifecycleStatus](lifecycleStatus.md) | Current lifecycle status of the data product |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: DataProductLifecycleStatus
description: An enumeration that defines the lifecycle stages for a DataProduct
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  Ideation:
    text: Ideation
  Design:
    text: Design
  Build:
    text: Build
  Deploy:
    text: Deploy
  Consume:
    text: Consume

```
</details>
