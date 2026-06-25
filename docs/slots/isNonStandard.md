

# Slot: isNonStandard 


_One or more members of this set are non-standard extensions_





URI: [dds:slot/isNonStandard](https://w3id.org/dds/slot/isNonStandard)
Alias: isNonStandard

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [ODMStandardReference](../classes/ODMStandardReference.md) | A mixin providing attributes for CDISC standards compliance indication. Applied when serializing to Define-XML context. Not canonical. |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |






## Properties

* Range: [Boolean](../types/Boolean.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:isNonStandard |
| native | dds:isNonStandard |




## LinkML Source

<details>
```yaml
name: isNonStandard
description: One or more members of this set are non-standard extensions
from_schema: https://w3id.org/dds
rank: 1000
alias: isNonStandard
owner: ODMStandardReference
domain_of:
- ODMStandardReference
range: boolean

```
</details>