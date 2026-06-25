

# Slot: profile 



URI: [dds:slot/profile](https://w3id.org/dds/slot/profile)
Alias: profile

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [IsProfile](../classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Products, including profiles, security tags, and validity periods |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:profile |
| native | dds:profile |




## LinkML Source

<details>
```yaml
name: profile
alias: profile
domain_of:
- IsProfile
- Policy
range: string

```
</details>