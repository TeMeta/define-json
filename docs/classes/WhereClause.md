

# Class: WhereClause 


_A conditional element that describes the circumstances under which a containing context applies, linking conditions to structures where they are used_





URI: [odm:class/WhereClause](https://cdisc.org/odm2/class/WhereClause)



```mermaid
erDiagram
WhereClause {
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
Condition {
    string implementsCondition  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
    boolean mandatory  
    string purpose  
    datetime lastUpdated  
    string owner  
    string wasDerivedFrom  
}
Comment {
    string text  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
FormalExpression {
    string context  
    string expression  
    string returnType  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
RangeCheck {
    Comparator comparator  
    stringList checkValues  
    string item  
    SoftHard softHard  
}

WhereClause ||--}o Condition : "conditions"
WhereClause ||--}o Coding : "coding"
Condition ||--}o RangeCheck : "rangeChecks"
Condition ||--}o FormalExpression : "formalExpression"
Condition ||--}o Coding : "coding"
Condition ||--}o Comment : "comment"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
RangeCheck ||--}o FormalExpression : "formalExpression"

```




## Inheritance
* [IdentifiableElement](../classes/IdentifiableElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md)]
    * **WhereClause**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [conditions](../slots/conditions.md) | * <br/> [Condition](../classes/Condition.md) | Logical conditions that apply in this context (combined with AND) | direct |
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
| [MetaDataVersion](../classes/MetaDataVersion.md) | [whereClauses](../slots/whereClauses.md) | range | [WhereClause](../classes/WhereClause.md) |
| [Item](../classes/Item.md) | [whereClause](../slots/whereClause.md) | range | [WhereClause](../classes/WhereClause.md) |
| [ItemGroup](../classes/ItemGroup.md) | [whereClause](../slots/whereClause.md) | range | [WhereClause](../classes/WhereClause.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [whereClause](../slots/whereClause.md) | range | [WhereClause](../classes/WhereClause.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:WhereClause |
| native | odm:WhereClause |
| related | fhir:StructureDefinition/context, qb:ObservationGroup, qb:Slice, sdmx:CubeRegion, sdmx:MetadataTargetRegion |
| close | sdmx:AttachmentConstraint |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: WhereClause
description: A conditional element that describes the circumstances under which a
  containing context applies, linking conditions to structures where they are used
from_schema: https://cdisc.org/define-json
close_mappings:
- sdmx:AttachmentConstraint
related_mappings:
- fhir:StructureDefinition/context
- qb:ObservationGroup
- qb:Slice
- sdmx:CubeRegion
- sdmx:MetadataTargetRegion
is_a: IdentifiableElement
attributes:
  conditions:
    name: conditions
    description: Logical conditions that apply in this context (combined with AND)
    from_schema: https://cdisc.org/define-json
    domain_of:
    - MetaDataVersion
    - WhereClause
    range: Condition
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: WhereClause
description: A conditional element that describes the circumstances under which a
  containing context applies, linking conditions to structures where they are used
from_schema: https://cdisc.org/define-json
close_mappings:
- sdmx:AttachmentConstraint
related_mappings:
- fhir:StructureDefinition/context
- qb:ObservationGroup
- qb:Slice
- sdmx:CubeRegion
- sdmx:MetadataTargetRegion
is_a: IdentifiableElement
attributes:
  conditions:
    name: conditions
    description: Logical conditions that apply in this context (combined with AND)
    from_schema: https://cdisc.org/define-json
    alias: conditions
    owner: WhereClause
    domain_of:
    - MetaDataVersion
    - WhereClause
    range: Condition
    multivalued: true
    inlined: true
    inlined_as_list: true
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: WhereClause
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
    owner: WhereClause
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: WhereClause
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
    owner: WhereClause
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
    owner: WhereClause
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
    owner: WhereClause
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
    owner: WhereClause
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