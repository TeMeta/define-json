# Enum: SoftHard 




_An enumeration that indicates whether a validation check should be treated as an error or a warning_



URI: [SoftHard](../enums/SoftHard.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Soft | None | Warning |
| Hard | None | Error |




## Slots

| Name | Description |
| ---  | --- |
| [softHard](../slots/softHard.md) | Indicates whether a validation check is an error ("Hard") or a warning ("Soft") |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: SoftHard
description: An enumeration that indicates whether a validation check should be treated
  as an error or a warning
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  Soft:
    text: Soft
    description: Warning
  Hard:
    text: Hard
    description: Error

```
</details>
