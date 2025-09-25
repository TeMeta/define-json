# Enum: DataType 




_An enumeration that defines the fundamental data types available for items_



URI: [DataType](DataType.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| text | None | Character text with no length restriction |
| integer | None | Integer numbers |
| float | None | Floating-point numbers (decimals) |
| date | None | Calendar date |
| time | None | Time of day |
| datetime | None | Calendar date and time of day |
| boolean | None | Logical values (true/false) |
| double | None | Double-precision floating-point numbers |
| hex | None | Hexadecimal number |
| base64 | None | Base-64 encoded binary data |
| hexBinary | None | Hexadecimal encoded binary data |




## Slots

| Name | Description |
| ---  | --- |
| [dataType](dataType.md) | The data type of the item |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: DataType
description: An enumeration that defines the fundamental data types available for
  items
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  text:
    text: text
    description: Character text with no length restriction.
  integer:
    text: integer
    description: Integer numbers.
  float:
    text: float
    description: Floating-point numbers (decimals).
  date:
    text: date
    description: Calendar date.
  time:
    text: time
    description: Time of day.
  datetime:
    text: datetime
    description: Calendar date and time of day.
  boolean:
    text: boolean
    description: Logical values (true/false).
  double:
    text: double
    description: Double-precision floating-point numbers.
  hex:
    text: hex
    description: Hexadecimal number.
  base64:
    text: base64
    description: Base-64 encoded binary data.
  hexBinary:
    text: hexBinary
    description: Hexadecimal encoded binary data.

```
</details>
