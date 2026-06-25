

# Slot: observationClass 


_Identifies the predefined CDISC model Class._





URI: [dds:slot/observationClass](https://w3id.org/dds/slot/observationClass)
Alias: observationClass

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |






## Properties

* Range: [DefClass](../classes/DefClass.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:observationClass |
| native | dds:observationClass |




## LinkML Source

<details>
```yaml
name: observationClass
description: Identifies the predefined CDISC model Class.
from_schema: https://w3id.org/dds
rank: 1000
alias: observationClass
owner: ItemGroup
domain_of:
- ItemGroup
range: DefClass
required: false

```
</details>