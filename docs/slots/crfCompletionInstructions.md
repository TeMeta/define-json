

# Slot: crfCompletionInstructions 


_CRFCompletionInstructions reference: Instructions for the clinical site on how to enter collected information on the CRF_





URI: [dds:slot/crfCompletionInstructions](https://w3id.org/dds/slot/crfCompletionInstructions)
Alias: crfCompletionInstructions

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMItemSerialization](../classes/ODMItemSerialization.md) | A mixin providing ODM/CDISC-specific item attributes meaningful only in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation notes, collection exception predicates, and pre-specified values. Applied by the ODM output generator. Not part of the canonical Item. |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:crfCompletionInstructions |
| native | dds:crfCompletionInstructions |




## LinkML Source

<details>
```yaml
name: crfCompletionInstructions
description: 'CRFCompletionInstructions reference: Instructions for the clinical site
  on how to enter collected information on the CRF'
from_schema: https://w3id.org/dds
rank: 1000
alias: crfCompletionInstructions
owner: ODMItemSerialization
domain_of:
- ODMItemSerialization
range: string
any_of:
- range: string
- range: TranslatedText

```
</details>