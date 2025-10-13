

# Slot: type 



URI: [odm:slot/type](https://cdisc.org/odm2/slot/type)
Alias: type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |
| [Origin](../classes/Origin.md) | A provenance element that describes the source of data for an item |  no  |
| [Standard](../classes/Standard.md) | A collection element that groups related standards within a specific context, used for defining CDISC implementation guides and controlled terminologies |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:type |
| native | odm:type |




## LinkML Source

<details>
```yaml
name: type
alias: type
domain_of:
- ItemGroup
- Method
- Origin
- Organization
- Standard
- Timing

```
</details>