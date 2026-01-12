

# Slot: isNonStandard 


_One or more members of this set are non-standard extensions_





URI: [odm:slot/isNonStandard](https://cdisc.org/odm2/slot/isNonStandard)
Alias: isNonStandard

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [IsODMStandard](../classes/IsODMStandard.md) | A mixin that provides properties to indicate standards compliance |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |






## Properties

* Range: [Boolean](../types/Boolean.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:isNonStandard |
| native | odm:isNonStandard |




## LinkML Source

<details>
```yaml
name: isNonStandard
description: One or more members of this set are non-standard extensions
from_schema: https://cdisc.org/define-json
rank: 1000
alias: isNonStandard
owner: IsODMStandard
domain_of:
- IsODMStandard
range: boolean

```
</details>