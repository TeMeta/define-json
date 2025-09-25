

# Slot: linkingPhrase 


_Variable relationship descriptive linking phrase._





URI: [odm:linkingPhrase](https://cdisc.org/odm2/linkingPhrase)
Alias: linkingPhrase

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Relationship](Relationship.md) | A semantic link that defines connections between elements such as Items or It... |  no  |







## Properties

* Range: [LinkingPhraseEnum](LinkingPhraseEnum.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:linkingPhrase |
| native | odm:linkingPhrase |




## LinkML Source

<details>
```yaml
name: linkingPhrase
description: Variable relationship descriptive linking phrase.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: linkingPhrase
owner: Relationship
domain_of:
- Relationship
range: LinkingPhraseEnum
required: true

```
</details>