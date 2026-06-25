

# Slot: assigner 



URI: [dds:slot/assigner](https://w3id.org/dds/slot/assigner)
Alias: assigner

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:assigner |
| native | dds:assigner |




## LinkML Source

<details>
```yaml
name: assigner
alias: assigner
domain_of:
- Policy
- Rule
range: string

```
</details>