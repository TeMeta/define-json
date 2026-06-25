

# Slot: obligation 


_Duties that must be fulfilled (odrl:obligation)_





URI: [odm:slot/obligation](https://cdisc.org/odm2/slot/obligation)
Alias: obligation

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |






## Properties

* Range: [Rule](../classes/Rule.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:obligation |
| native | odm:obligation |
| exact | odrl:obligation |




## LinkML Source

<details>
```yaml
name: obligation
description: Duties that must be fulfilled (odrl:obligation)
from_schema: https://cdisc.org/data-definition-spec
exact_mappings:
- odrl:obligation
rank: 1000
alias: obligation
owner: Policy
domain_of:
- Policy
range: Rule
multivalued: true
inlined: true
inlined_as_list: true

```
</details>