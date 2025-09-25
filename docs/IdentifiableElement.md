

# Class: IdentifiableElement 


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [odm:IdentifiableElement](https://cdisc.org/odm2/IdentifiableElement)



```mermaid
erDiagram
IdentifiableElement {
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

IdentifiableElement ||--}o Coding : "coding"

```




## Inheritance
* **IdentifiableElement** [ [Identifiable](Identifiable.md) [Labelled](Labelled.md)]
    * [Relationship](Relationship.md)
    * [Comment](Comment.md)
    * [CodingMapping](CodingMapping.md)
    * [WhereClause](WhereClause.md)
    * [FormalExpression](FormalExpression.md)
    * [Parameter](Parameter.md)
    * [ReturnValue](ReturnValue.md)
    * [SiteOrSponsorComment](SiteOrSponsorComment.md)
    * [User](User.md)
    * [Organization](Organization.md)
    * [Resource](Resource.md) [ [Versioned](Versioned.md)]
    * [DocumentReference](DocumentReference.md) [ [Versioned](Versioned.md)]
    * [Timing](Timing.md)
    * [Dataset](Dataset.md) [ [Versioned](Versioned.md) [IsProfile](IsProfile.md) [IsSdmxDataset](IsSdmxDataset.md)]
    * [ComponentList](ComponentList.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
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
| [Relationship](Relationship.md) | [subject](subject.md) | range | [IdentifiableElement](IdentifiableElement.md) |
| [Relationship](Relationship.md) | [object](object.md) | range | [IdentifiableElement](IdentifiableElement.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:IdentifiableElement |
| native | odm:IdentifiableElement |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: IdentifiableElement
from_schema: https://cdisc.org/define-json
abstract: true
mixins:
- Identifiable
- Labelled

```
</details>

### Induced

<details>
```yaml
name: IdentifiableElement
from_schema: https://cdisc.org/define-json
abstract: true
mixins:
- Identifiable
- Labelled
attributes:
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: IdentifiableElement
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
    owner: IdentifiableElement
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: IdentifiableElement
    domain_of:
    - Labelled
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: description
    owner: IdentifiableElement
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
    owner: IdentifiableElement
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
    owner: IdentifiableElement
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
    owner: IdentifiableElement
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