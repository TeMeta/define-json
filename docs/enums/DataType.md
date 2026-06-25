# Enum: DataType 




_An enumeration that defines the fundamental data types available for items_



URI: [dds:enum/DataType](https://w3id.org/dds/enum/DataType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| text | None | Character text with no length restriction. |
| integer | None | Integer numbers. |
| float | None | Floating-point numbers (decimals). |
| date | None | Calendar date. |
| time | None | Time of day. |
| datetime | None | Calendar date and time of day. |
| boolean | None | Logical values (true/false). |
| double | None | Double-precision floating-point numbers. |
| hex | None | Hexadecimal number. |
| base64 | None | Base-64 encoded binary data. |
| hexBinary | None | Hexadecimal encoded binary data. |
| durationDatetime | None | ISO 8601 duration value representing a span of time (e.g., P1Y2M3DT4H5M6S). |




## Slots

| Name | Description |
| ---  | --- |
| [dataType](../slots/dataType.md) | The data type of the item. |





## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: DataType
description: An enumeration that defines the fundamental data types available for
  items
from_schema: https://w3id.org/dds
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
  durationDatetime:
    text: durationDatetime
    description: ISO 8601 duration value representing a span of time (e.g., P1Y2M3DT4H5M6S).

```
</details>