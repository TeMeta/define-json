

# Slot: decimalDigits 


_For decimal values, the number of digits after the decimal point_





URI: [odm:decimalDigits](https://cdisc.org/odm2/decimalDigits)
Alias: decimalDigits

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [Formatted](Formatted.md) | A mixin that provides slots for reporting, exchange, or storage formatting |  no  |







## Properties

* Range: [Integer](Integer.md)





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