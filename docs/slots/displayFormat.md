

# Slot: displayFormat 


_A display format for the item_





URI: [odm:slot/displayFormat](https://cdisc.org/odm2/slot/displayFormat)
Alias: displayFormat

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [Formatted](../classes/Formatted.md) | A mixin that provides slots for reporting, exchange, or storage formatting |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:displayFormat |
| native | odm:displayFormat |




## LinkML Source

<details>
```yaml
name: displayFormat
description: A display format for the item
from_schema: https://cdisc.org/define-json
rank: 1000
alias: displayFormat
owner: Formatted
domain_of:
- Formatted
range: string

```
</details>