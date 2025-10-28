

# Slot: children 


_References to child ItemGroups (OIDs) within this item group. Use these OID references to look up the actual ItemGroup objects  from the top-level itemGroups collection._





URI: [odm:slot/children](https://cdisc.org/odm2/slot/children)
Alias: children

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |







## Properties

* Range: [String](../types/String.md)

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
description: References to child ItemGroups (OIDs) within this item group. Use these
  OID references to look up the actual ItemGroup objects  from the top-level itemGroups
  collection.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: children
owner: ItemGroup
domain_of:
- ItemGroup
range: string
multivalued: true
inlined: false

```
</details>