

# Slot: hasNoData 


_Set to Yes if this is a manifest and there is no data for this item_





URI: [odm:slot/hasNoData](https://cdisc.org/odm2/slot/hasNoData)
Alias: hasNoData

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [IsODMItem](../classes/IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |  no  |







## Properties

* Range: [Boolean](../types/Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:hasNoData |
| native | odm:hasNoData |




## LinkML Source

<details>
```yaml
name: hasNoData
description: Set to Yes if this is a manifest and there is no data for this item
from_schema: https://cdisc.org/define-json
rank: 1000
alias: hasNoData
owner: IsODMItem
domain_of:
- IsODMItem
range: boolean

```
</details>