

# Slot: relationships 


_Relationships between items, item groups, and other elements in this version of the metadata._





URI: [odm:slot/relationships](https://cdisc.org/odm2/slot/relationships)
Alias: relationships

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |






## Properties

* Range: [Relationship](../classes/Relationship.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:relationships |
| native | odm:relationships |




## LinkML Source

<details>
```yaml
name: relationships
description: Relationships between items, item groups, and other elements in this
  version of the metadata.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: relationships
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: Relationship
multivalued: true
inlined: true
inlined_as_list: true

```
</details>