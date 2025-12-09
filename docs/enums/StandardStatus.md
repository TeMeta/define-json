# Enum: StandardStatus 




_An enumeration that defines permissible values for standard status_



URI: [odm:enum/StandardStatus](https://cdisc.org/odm2/enum/StandardStatus)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| DRAFT | None | Draft version of the standard |
| FINAL | None | Final version of the standard |




## Slots

| Name | Description |
| ---  | --- |
| [status](../slots/status.md) | Status of an Implementation Guide or of a Controlled Terminology |





## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: StandardStatus
description: An enumeration that defines permissible values for standard status
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  DRAFT:
    text: DRAFT
    description: Draft version of the standard
  FINAL:
    text: FINAL
    description: Final version of the standard

```
</details>