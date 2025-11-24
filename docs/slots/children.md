

# Slot: children 


_Child ItemGroups nested within this item group (e.g., ValueLists under parent domains). Can be either: - Full ItemGroup objects (preferred for hierarchical nesting) - OID string references (for cross-references to avoid duplication)_





URI: [odm:slot/children](https://cdisc.org/odm2/slot/children)
Alias: children

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |







## Properties

* Range: [ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[String](../types/String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:children |
| native | odm:children |




## LinkML Source

<details>
```yaml
name: children
description: 'Child ItemGroups nested within this item group (e.g., ValueLists under
  parent domains). Can be either: - Full ItemGroup objects (preferred for hierarchical
  nesting) - OID string references (for cross-references to avoid duplication)'
from_schema: https://cdisc.org/define-json
rank: 1000
alias: children
owner: ItemGroup
domain_of:
- ItemGroup
range: ItemGroup
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: ItemGroup
- range: string

```
</details>