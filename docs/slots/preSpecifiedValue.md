

# Slot: preSpecifiedValue 


_Prefill value or a default value for a field that is automatically populated._





URI: [odm:slot/preSpecifiedValue](https://cdisc.org/odm2/slot/preSpecifiedValue)
Alias: preSpecifiedValue

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [IsODMItem](../classes/IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:preSpecifiedValue |
| native | odm:preSpecifiedValue |




## LinkML Source

<details>
```yaml
name: preSpecifiedValue
description: Prefill value or a default value for a field that is automatically populated.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: preSpecifiedValue
owner: IsODMItem
domain_of:
- IsODMItem
any_of:
- range: string
- range: TranslatedText

```
</details>