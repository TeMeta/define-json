

# Slot: leftOperand 


_The subject of the constraint (odrl:leftOperand), e.g. "purpose", "recipient", "dateTime"_





URI: [odm:slot/leftOperand](https://cdisc.org/odm2/slot/leftOperand)
Alias: leftOperand

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
| self | odm:leftOperand |
| native | odm:leftOperand |
| exact | odrl:leftOperand |




## LinkML Source

<details>
```yaml
name: leftOperand
description: The subject of the constraint (odrl:leftOperand), e.g. "purpose", "recipient",
  "dateTime"
from_schema: https://cdisc.org/data-definition-spec
exact_mappings:
- odrl:leftOperand
rank: 1000
alias: leftOperand
owner: Constraint
domain_of:
- Constraint
range: string
required: true

```
</details>