

# Slot: target 


_The asset the rule applies to (odrl:target), e.g. the Dataflow or Dataset OID/IRI under agreement._





URI: [dds:slot/target](https://w3id.org/dds/slot/target)
Alias: target

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:target |
| native | dds:target |
| exact | odrl:target |




## LinkML Source

<details>
```yaml
name: target
description: The asset the rule applies to (odrl:target), e.g. the Dataflow or Dataset
  OID/IRI under agreement.
from_schema: https://w3id.org/dds
exact_mappings:
- odrl:target
rank: 1000
alias: target
owner: Rule
domain_of:
- Rule
range: string

```
</details>