

# Slot: cdiscNotes 


_CDISCNotes reference: Explanatory text for the variable_





URI: [odm:cdiscNotes](https://cdisc.org/odm2/cdiscNotes)
Alias: cdiscNotes

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [IsODMItem](IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |  no  |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:cdiscNotes |
| native | odm:cdiscNotes |




## LinkML Source

<details>
```yaml
name: cdiscNotes
description: 'CDISCNotes reference: Explanatory text for the variable'
from_schema: https://cdisc.org/define-json
rank: 1000
alias: cdiscNotes
owner: IsODMItem
domain_of:
- IsODMItem
any_of:
- range: string
- range: TranslatedText

```
</details>