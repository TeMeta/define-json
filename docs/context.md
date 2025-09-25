

# Slot: context 


_The specific context within the containing element to which this formal expression applies._





URI: [odm:context](https://cdisc.org/odm2/context)
Alias: context

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [FormalExpression](FormalExpression.md) | A computational element that defines the execution of a data derivation withi... |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:context |
| native | odm:context |
| exact | fhir:Expression/language |




## LinkML Source

<details>
```yaml
name: context
description: The specific context within the containing element to which this formal
  expression applies.
from_schema: https://cdisc.org/define-json
exact_mappings:
- fhir:Expression/language
rank: 1000
alias: context
owner: FormalExpression
domain_of:
- FormalExpression
range: string

```
</details>