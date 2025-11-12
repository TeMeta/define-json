

# Slot: significantDigits 


_For numeric values, the number of significant digits_





URI: [odm:slot/significantDigits](https://cdisc.org/odm2/slot/significantDigits)
Alias: significantDigits

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [Formatted](../classes/Formatted.md) | A mixin that provides slots for reporting, exchange, or storage formatting |  no  |







## Properties

* Range: [Integer](../types/Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:significantDigits |
| native | odm:significantDigits |




## LinkML Source

<details>
```yaml
name: significantDigits
description: For numeric values, the number of significant digits
from_schema: https://cdisc.org/define-json
rank: 1000
alias: significantDigits
owner: Formatted
domain_of:
- Formatted
range: integer

```
</details>