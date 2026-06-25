

# Slot: preSpecifiedValue 


_Prefill value or a default value for a field that is automatically populated._





URI: [dds:slot/preSpecifiedValue](https://w3id.org/dds/slot/preSpecifiedValue)
Alias: preSpecifiedValue

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
| self | dds:preSpecifiedValue |
| native | dds:preSpecifiedValue |




## LinkML Source

<details>
```yaml
name: preSpecifiedValue
description: Prefill value or a default value for a field that is automatically populated.
from_schema: https://w3id.org/dds
rank: 1000
alias: preSpecifiedValue
owner: ODMItemSerialization
domain_of:
- ODMItemSerialization
range: string
any_of:
- range: string
- range: TranslatedText

```
</details>