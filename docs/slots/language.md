

# Slot: language 


_The language of the translation_





URI: [odm:slot/language](https://cdisc.org/odm2/slot/language)
Alias: language

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Translation](../classes/Translation.md) | A text representation that provides content in a specific language, used for multilingual support |  no  |







## Properties

* Range: [String](../types/String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:language |
| native | odm:language |




## LinkML Source

<details>
```yaml
name: language
description: The language of the translation
from_schema: https://cdisc.org/define-json
rank: 1000
alias: language
owner: Translation
domain_of:
- Translation
range: string
required: true

```
</details>