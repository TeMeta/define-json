

# Slot: implementationNotes 


_ImplementationNotes reference: Further information, such as rationale and implementation instructions, on how to implement the CRF data collection fields_





URI: [dds:slot/implementationNotes](https://w3id.org/dds/slot/implementationNotes)
Alias: implementationNotes

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
| self | dds:implementationNotes |
| native | dds:implementationNotes |




## LinkML Source

<details>
```yaml
name: implementationNotes
description: 'ImplementationNotes reference: Further information, such as rationale
  and implementation instructions, on how to implement the CRF data collection fields'
from_schema: https://w3id.org/dds
rank: 1000
alias: implementationNotes
owner: ODMItemSerialization
domain_of:
- ODMItemSerialization
range: string
any_of:
- range: string
- range: TranslatedText

```
</details>