

# Slot: conditions 



URI: [odm:slot/conditions](https://cdisc.org/odm2/slot/conditions)
Alias: conditions

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [WhereClause](../classes/WhereClause.md) | A conditional element that describes the circumstances under which a containing context applies, linking conditions to structures where they are used |  no  |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [Condition](../classes/Condition.md) | A reusable, composable, and nestable logical construct allowing for complex expressions. Conditions are most useful when given a meaningful name and linked to Study Definitions. |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:conditions |
| native | odm:conditions |




## LinkML Source

<details>
```yaml
name: conditions
alias: conditions
domain_of:
- MetaDataVersion
- WhereClause
- Condition
- Parameter

```
</details>