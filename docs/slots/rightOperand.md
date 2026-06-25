

# Slot: rightOperand 


_The value compared against (odrl:rightOperand)_





URI: [odm:slot/rightOperand](https://cdisc.org/odm2/slot/rightOperand)
Alias: rightOperand

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Constraint](../classes/Constraint.md) | An ODRL constraint expressed as leftOperand operator rightOperand, e.g. purpose eq "safety-reporting", or dateTime lt "2026-01-01". |  no  |






## Properties

* Range: [String](../types/String.md)

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:rightOperand |
| native | odm:rightOperand |
| exact | odrl:rightOperand |




## LinkML Source

<details>
```yaml
name: rightOperand
description: The value compared against (odrl:rightOperand)
from_schema: https://cdisc.org/data-definition-spec
exact_mappings:
- odrl:rightOperand
rank: 1000
alias: rightOperand
owner: Constraint
domain_of:
- Constraint
range: string
required: true

```
</details>