

# Slot: decimalDigits 


_For decimal values, the number of digits after the decimal point_





URI: [odm:slot/decimalDigits](https://cdisc.org/odm2/slot/decimalDigits)
Alias: decimalDigits

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [Formatted](../classes/Formatted.md) | A mixin that provides slots for reporting, exchange, or storage formatting |  no  |







## Properties

* Range: [Integer](../types/Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:decimalDigits |
| native | odm:decimalDigits |




## LinkML Source

<details>
```yaml
name: decimalDigits
description: For decimal values, the number of digits after the decimal point
from_schema: https://cdisc.org/define-json
rank: 1000
alias: decimalDigits
owner: Formatted
domain_of:
- Formatted
range: integer

```
</details>