

# Slot: parameters 


_Parameters used in the expression_





URI: [odm:slot/parameters](https://cdisc.org/odm2/slot/parameters)
Alias: parameters

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [FormalExpression](../classes/FormalExpression.md) | A computational element that defines the execution of a data derivation within a specific context |  no  |






## Properties

* Range: [Parameter](../classes/Parameter.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:parameters |
| native | odm:parameters |




## LinkML Source

<details>
```yaml
name: parameters
description: Parameters used in the expression
from_schema: https://cdisc.org/define-json
rank: 1000
alias: parameters
owner: FormalExpression
domain_of:
- FormalExpression
range: Parameter
multivalued: true
inlined: true
inlined_as_list: true

```
</details>