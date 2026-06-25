

# Slot: prohibition 


_Rules forbidding an action (odrl:prohibition)_





URI: [odm:slot/prohibition](https://cdisc.org/odm2/slot/prohibition)
Alias: prohibition

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
| self | odm:prohibition |
| native | odm:prohibition |
| exact | odrl:prohibition |




## LinkML Source

<details>
```yaml
name: prohibition
description: Rules forbidding an action (odrl:prohibition)
from_schema: https://cdisc.org/data-definition-spec
exact_mappings:
- odrl:prohibition
rank: 1000
alias: prohibition
owner: Policy
domain_of:
- Policy
range: Rule
multivalued: true
inlined: true
inlined_as_list: true

```
</details>