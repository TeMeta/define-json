

# Slot: implementsCondition 


_Reference to a external (e.g. USDM) condition definition that this implements_





URI: [odm:slot/implementsCondition](https://cdisc.org/odm2/slot/implementsCondition)
Alias: implementsCondition

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Condition](../classes/Condition.md) | A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:implementsCondition |
| native | odm:implementsCondition |




## LinkML Source

<details>
```yaml
name: implementsCondition
description: Reference to a external (e.g. USDM) condition definition that this implements
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: implementsCondition
owner: Condition
domain_of:
- Condition
range: string

```
</details>