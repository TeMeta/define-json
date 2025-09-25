

# Slot: expression 


_The actual text of the formal expression (renamed from 'code' for disambiguation)._





URI: [odm:expression](https://cdisc.org/odm2/expression)
Alias: expression

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [FormalExpression](FormalExpression.md) | A computational element that defines the execution of a data derivation withi... |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:expression |
| native | odm:expression |




## LinkML Source

<details>
```yaml
name: expression
description: The actual text of the formal expression (renamed from 'code' for disambiguation).
from_schema: https://cdisc.org/define-json
rank: 1000
alias: expression
owner: FormalExpression
domain_of:
- FormalExpression
range: string
required: true

```
</details>