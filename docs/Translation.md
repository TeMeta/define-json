

# Class: Translation 


_A text representation that provides content in a specific language, used for multilingual support_





URI: [odm:Translation](https://cdisc.org/odm2/Translation)



```mermaid
erDiagram
Translation {
    string language  
    string value  
}



```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [language](language.md) | 1 <br/> [String](String.md) | The language of the translation | direct |
| [value](value.md) | 1 <br/> [String](String.md) | The translated text | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TranslatedText](TranslatedText.md) | [translations](translations.md) | range | [Translation](Translation.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:Translation |
| native | odm:Translation |
| exact | odm:TranslatedText, sdmx:InternationalString |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Translation
description: A text representation that provides content in a specific language, used
  for multilingual support
from_schema: https://cdisc.org/define-json
exact_mappings:
- odm:TranslatedText
- sdmx:InternationalString
attributes:
  language:
    name: language
    description: The language of the translation
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - Translation
    range: string
    required: true
  value:
    name: value
    description: The translated text
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - Translation
    - Parameter
    - Timing
    range: string
    required: true

```
</details>

### Induced

<details>
```yaml
name: Translation
description: A text representation that provides content in a specific language, used
  for multilingual support
from_schema: https://cdisc.org/define-json
exact_mappings:
- odm:TranslatedText
- sdmx:InternationalString
attributes:
  language:
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
  value:
    name: value
    description: The translated text
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: value
    owner: Translation
    domain_of:
    - Translation
    - Parameter
    - Timing
    range: string
    required: true

```
</details>