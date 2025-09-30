

# Class: ComponentList 


_An abstract definition that specifies a list of components within a data structure definition, including various descriptor types_





URI: [odm:class/ComponentList](https://cdisc.org/odm2/class/ComponentList)



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
    AliasPredicate aliasType  
}

ComponentList ||--}o Coding : "coding"

```




## Inheritance
* [IdentifiableElement](../classes/IdentifiableElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md)]
    * **ComponentList**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [components](../slots/components.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Measure](../classes/Measure.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[DataAttribute](../classes/DataAttribute.md) | The components that make up this component list | direct |
| [OID](../slots/OID.md) | 1 <br/> [String](../types/String.md) | Local identifier within this study/context | [Identifiable](../classes/Identifiable.md) |
| [uuid](../slots/uuid.md) | 0..1 <br/> [String](../types/String.md) | Universal unique identifier | [Identifiable](../classes/Identifiable.md) |
| [name](../slots/name.md) | 0..1 <br/> [String](../types/String.md) | Short name or identifier, used for field names | [Labelled](../classes/Labelled.md) |
| [description](../slots/description.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](../classes/Labelled.md) |
| [coding](../slots/coding.md) | * <br/> [Coding](../classes/Coding.md) | Semantic tags for this element | [Labelled](../classes/Labelled.md) |
| [label](../slots/label.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](../classes/Labelled.md) |
| [aliases](../slots/aliases.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Alternative name or identifier | [Labelled](../classes/Labelled.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [grouping](../slots/grouping.md) | range | [ComponentList](../classes/ComponentList.md) |
| [DatasetKey](../classes/DatasetKey.md) | [describedBy](../slots/describedBy.md) | any_of[range] | [ComponentList](../classes/ComponentList.md) |
| [GroupKey](../classes/GroupKey.md) | [describedBy](../slots/describedBy.md) | any_of[range] | [ComponentList](../classes/ComponentList.md) |
| [SeriesKey](../classes/SeriesKey.md) | [describedBy](../slots/describedBy.md) | any_of[range] | [ComponentList](../classes/ComponentList.md) |
| [GroupRelationship](../classes/GroupRelationship.md) | [groupKey](../slots/groupKey.md) | range | [ComponentList](../classes/ComponentList.md) |
| [DimensionRelationship](../classes/DimensionRelationship.md) | [groupKey](../slots/groupKey.md) | range | [ComponentList](../classes/ComponentList.md) |






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
    - Standard
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