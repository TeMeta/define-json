

# Slot: rightOperand 


_The value compared against (odrl:rightOperand)_





URI: [dds:slot/rightOperand](https://w3id.org/dds/slot/rightOperand)
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


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:rightOperand |
| native | dds:rightOperand |
| exact | odrl:rightOperand |




## LinkML Source

<details>
```yaml
name: rightOperand
description: The value compared against (odrl:rightOperand)
from_schema: https://w3id.org/dds
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