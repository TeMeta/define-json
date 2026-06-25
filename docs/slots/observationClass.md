

# Slot: observationClass 


_Identifies the predefined CDISC model Class._





URI: [odm:slot/observationClass](https://cdisc.org/odm2/slot/observationClass)
Alias: observationClass

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |






## Properties

* Range: [DefClass](../classes/DefClass.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:observationClass |
| native | odm:observationClass |




## LinkML Source

<details>
```yaml
name: observationClass
description: Identifies the predefined CDISC model Class.
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: observationClass
owner: ItemGroup
domain_of:
- ItemGroup
range: DefClass
required: false

```
</details>