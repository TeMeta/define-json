

# Slot: applicableWhen 



URI: [dds:slot/applicableWhen](https://w3id.org/dds/slot/applicableWhen)
Alias: applicableWhen

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:applicableWhen |
| native | dds:applicableWhen |




## LinkML Source

<details>
```yaml
name: applicableWhen
alias: applicableWhen
domain_of:
- Item
- ItemGroup
- Parameter
- Analysis
range: string

```
</details>