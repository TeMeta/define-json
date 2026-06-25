

# Slot: permission 


_Rules granting the ability to perform an action (odrl:permission)_





URI: [dds:slot/permission](https://w3id.org/dds/slot/permission)
Alias: permission

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


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:permission |
| native | dds:permission |
| exact | odrl:permission |




## LinkML Source

<details>
```yaml
name: permission
description: Rules granting the ability to perform an action (odrl:permission)
from_schema: https://w3id.org/dds
exact_mappings:
- odrl:permission
rank: 1000
alias: permission
owner: Policy
domain_of:
- Policy
range: Rule
multivalued: true
inlined: true
inlined_as_list: true

```
</details>