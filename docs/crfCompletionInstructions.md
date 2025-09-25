

# Slot: crfCompletionInstructions 


_CRFCompletionInstructions reference: Instructions for the clinical site on how to enter collected information on the CRF_





URI: [odm:crfCompletionInstructions](https://cdisc.org/odm2/crfCompletionInstructions)
Alias: crfCompletionInstructions

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](Item.md) | A data element that represents a specific piece of information within a defin... |  no  |
| [IsODMItem](IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:crfCompletionInstructions |
| native | odm:crfCompletionInstructions |




## LinkML Source

<details>
```yaml
name: crfCompletionInstructions
description: 'CRFCompletionInstructions reference: Instructions for the clinical site
  on how to enter collected information on the CRF'
from_schema: https://cdisc.org/define-json
rank: 1000
alias: crfCompletionInstructions
owner: IsODMItem
domain_of:
- IsODMItem
any_of:
- range: string
- range: TranslatedText

```
</details>