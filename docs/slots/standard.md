

# Slot: standard 


_Reference to the standard being implemented_





URI: [odm:slot/standard](https://cdisc.org/odm2/slot/standard)
Alias: standard

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [IsODMStandard](../classes/IsODMStandard.md) | A mixin that provides properties to indicate standards compliance |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |






## Properties

* Range: [Standard](../classes/Standard.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:standard |
| native | odm:standard |




## LinkML Source

<details>
```yaml
name: standard
description: Reference to the standard being implemented
from_schema: https://cdisc.org/define-json
rank: 1000
alias: standard
owner: IsODMStandard
domain_of:
- IsODMStandard
range: Standard

```
</details>