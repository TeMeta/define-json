

# Slot: codeListItems 


_The individual values that make up this CodeList. The type of CodeListItem included determines its behaviour_





URI: [odm:slot/codeListItems](https://cdisc.org/odm2/slot/codeListItems)
Alias: codeListItems

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |






## Properties

* Range: [CodeListItem](../classes/CodeListItem.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:codeListItems |
| native | odm:codeListItems |




## LinkML Source

<details>
```yaml
name: codeListItems
description: The individual values that make up this CodeList. The type of CodeListItem
  included determines its behaviour
from_schema: https://cdisc.org/define-json
rank: 1000
alias: codeListItems
owner: CodeList
domain_of:
- CodeList
range: CodeListItem
multivalued: true
inlined: true
inlined_as_list: true

```
</details>