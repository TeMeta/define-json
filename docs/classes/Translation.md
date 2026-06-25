

# Class: Translation 


_A text representation that provides content in a specific language, used for multilingual support_





URI: [dds:class/Translation](https://w3id.org/dds/class/Translation)


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
| [language](../slots/language.md) | 1 <br/> [String](../types/String.md) | The language of the translation | direct |
| [value](../slots/value.md) | 1 <br/> [String](../types/String.md) | The translated text | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TranslatedText](../classes/TranslatedText.md) | [translations](../slots/translations.md) | range | [Translation](../classes/Translation.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:Translation |
| native | dds:Translation |
| exact | odm:TranslatedText, sdmx:InternationalString |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Translation
description: A text representation that provides content in a specific language, used
  for multilingual support
from_schema: https://w3id.org/dds
exact_mappings:
- odm:TranslatedText
- sdmx:InternationalString
attributes:
  language:
    name: language
    description: The language of the translation
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Translation
    required: true
  value:
    name: value
    description: The translated text
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Translation
    - Parameter
    - Timing
    required: true

```
</details>

### Induced

<details>
```yaml
name: Translation
description: A text representation that provides content in a specific language, used
  for multilingual support
from_schema: https://w3id.org/dds
exact_mappings:
- odm:TranslatedText
- sdmx:InternationalString
attributes:
  language:
    name: language
    description: The language of the translation
    from_schema: https://w3id.org/dds
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
    from_schema: https://w3id.org/dds
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