

# Slot: assignee 



URI: [odm:slot/assignee](https://cdisc.org/odm2/slot/assignee)
Alias: assignee

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:assignee |
| native | odm:assignee |




## LinkML Source

<details>
```yaml
name: assignee
alias: assignee
domain_of:
- Policy
- Rule
range: string

```
</details>