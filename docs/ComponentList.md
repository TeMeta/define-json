

# Class: ComponentList 


_An abstract definition that specifies a list of components within a data structure definition, including various descriptor types_





URI: [odm:ComponentList](https://cdisc.org/odm2/ComponentList)



```mermaid
erDiagram
ComponentList {
    stringList components  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
}

ComponentList ||--}o Coding : "coding"

```




## Inheritance
* [IdentifiableElement](IdentifiableElement.md) [ [Identifiable](Identifiable.md) [Labelled](Labelled.md)]
    * **ComponentList**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [components](components.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[Measure](Measure.md)&nbsp;or&nbsp;<br />[Dimension](Dimension.md)&nbsp;or&nbsp;<br />[DataAttribute](DataAttribute.md) | The components that make up this component list | direct |
| [OID](OID.md) | 1 <br/> [String](String.md) | Local identifier within this study/context | [Identifiable](Identifiable.md) |
| [uuid](uuid.md) | 0..1 <br/> [String](String.md) | Universal unique identifier | [Identifiable](Identifiable.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | Short name or identifier, used for field names | [Labelled](Labelled.md) |
| [description](description.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](Labelled.md) |
| [coding](coding.md) | * <br/> [Coding](Coding.md) | Semantic tags for this element | [Labelled](Labelled.md) |
| [label](label.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](Labelled.md) |
| [aliases](aliases.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Alternative name or identifier | [Labelled](Labelled.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [DataStructureDefinition](DataStructureDefinition.md) | [grouping](grouping.md) | range | [ComponentList](ComponentList.md) |
| [DatasetKey](DatasetKey.md) | [describedBy](describedBy.md) | any_of[range] | [ComponentList](ComponentList.md) |
| [GroupKey](GroupKey.md) | [describedBy](describedBy.md) | any_of[range] | [ComponentList](ComponentList.md) |
| [SeriesKey](SeriesKey.md) | [describedBy](describedBy.md) | any_of[range] | [ComponentList](ComponentList.md) |
| [GroupRelationship](GroupRelationship.md) | [groupKey](groupKey.md) | range | [ComponentList](ComponentList.md) |
| [DimensionRelationship](DimensionRelationship.md) | [groupKey](groupKey.md) | range | [ComponentList](ComponentList.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:ComponentList |
| native | odm:ComponentList |
| exact | sdmx:ComponentList |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ComponentList
description: An abstract definition that specifies a list of components within a data
  structure definition, including various descriptor types
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:ComponentList
is_a: IdentifiableElement
attributes:
  components:
    name: components
    description: The components that make up this component list
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - ComponentList
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: Measure
    - range: Dimension
    - range: DataAttribute

```
</details>

### Induced

<details>
```yaml
name: ComponentList
description: An abstract definition that specifies a list of components within a data
  structure definition, including various descriptor types
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:ComponentList
is_a: IdentifiableElement
attributes:
  components:
    name: components
    description: The components that make up this component list
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: components
    owner: ComponentList
    domain_of:
    - ComponentList
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: Measure
    - range: Dimension
    - range: DataAttribute
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: ComponentList
    domain_of:
    - Identifiable
    range: string
    required: true
    pattern: ^[A-Za-z][A-Za-z0-9._-]*$
  uuid:
    name: uuid
    description: Universal unique identifier
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: uuid
    owner: ComponentList
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: ComponentList
    domain_of:
    - Labelled
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: description
    owner: ComponentList
    domain_of:
    - Labelled
    - CodeListItem
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  coding:
    name: coding
    description: Semantic tags for this element
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: coding
    owner: ComponentList
    domain_of:
    - Labelled
    - CodeListItem
    - SourceItem
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  label:
    name: label
    description: Human-readable label, shown in UIs
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    alias: label
    owner: ComponentList
    domain_of:
    - Labelled
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  aliases:
    name: aliases
    description: Alternative name or identifier
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - skos:altLabel
    rank: 1000
    alias: aliases
    owner: ComponentList
    domain_of:
    - Labelled
    - CodeListItem
    range: string
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: string
    - range: TranslatedText

```
</details>