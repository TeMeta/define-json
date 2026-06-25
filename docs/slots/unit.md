

# Slot: unit 


_Unit of the rightOperand, where applicable_





URI: [odm:slot/unit](https://cdisc.org/odm2/slot/unit)
Alias: unit

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Constraint](../classes/Constraint.md) | An ODRL constraint expressed as leftOperand operator rightOperand, e.g. purpose eq "safety-reporting", or dateTime lt "2026-01-01". |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:unit |
| native | odm:unit |




## LinkML Source

<details>
```yaml
name: unit
description: Unit of the rightOperand, where applicable
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: unit
owner: Constraint
domain_of:
- Constraint
range: string

```
</details>