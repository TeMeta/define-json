

# Slot: condition 


_A condition that must be met for this occurrence to be valid._





URI: [odm:slot/condition](https://cdisc.org/odm2/slot/condition)
Alias: condition

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NominalOccurrence](../classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned encounters or adverse events |  no  |






## Properties

* Range: [Condition](../classes/Condition.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:condition |
| native | odm:condition |




## LinkML Source

<details>
```yaml
name: condition
description: A condition that must be met for this occurrence to be valid.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: condition
owner: NominalOccurrence
domain_of:
- NominalOccurrence
range: Condition
multivalued: true

```
</details>