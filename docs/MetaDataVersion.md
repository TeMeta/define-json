

# Class: MetaDataVersion 


_A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument._





URI: [odm:MetaDataVersion](https://cdisc.org/odm2/MetaDataVersion)



```mermaid
erDiagram
MetaDataVersion {
    stringList resources  
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
}
DocumentReference {
    string title  
    integerList pages  
    string relationship  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Relationship {
    PredicateTermEnum predicateTerm  
    LinkingPhraseEnum linkingPhrase  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
IdentifiableElement {
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
ReifiedConcept {
    string version  
    string href  
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
ConceptProperty {
    integer minOccurs  
    integer maxOccurs  
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
CodingMapping {
    AliasPredicateEnum relationship  
    float confidence  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
CodeList {
    DataType dataType  
    string formatName  
    stringList codeListItems  
    string version  
    string href  
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
Resource {
    string resourceType  
    string attribute  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Method {
    MethodType type  
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
WhereClause {
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
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
ItemGroup {
    string domain  
    string structure  
    boolean isReferenceData  
    ItemGroupType type  
    stringList profile  
    string authenticator  
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
    string version  
    string href  
}
Timing {
    TimingType type  
    boolean isNominal  
    string value  
    datetime windowLower  
    datetime windowUpper  
    boolean recalled  
    string frequency  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Item {
    DataType dataType  
    integer length  
    string role  
    boolean hasNoData  
    string crfCompletionInstructions  
    string cdiscNotes  
    string implementationNotes  
    string preSpecifiedValue  
    integer decimalDigits  
    string displayFormat  
    integer significantDigits  
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

MetaDataVersion ||--}o Item : "items"
MetaDataVersion ||--}o ItemGroup : "itemGroups"
MetaDataVersion ||--}o Condition : "conditions"
MetaDataVersion ||--}o WhereClause : "whereClauses"
MetaDataVersion ||--}o Method : "methods"
MetaDataVersion ||--}o CodeList : "codeLists"
MetaDataVersion ||--}o Coding : "codings"
MetaDataVersion ||--}o CodingMapping : "mappings"
MetaDataVersion ||--}o ReifiedConcept : "concepts"
MetaDataVersion ||--}o Relationship : "relationships"
MetaDataVersion ||--}o Coding : "coding"
MetaDataVersion ||--}o Comment : "comment"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
DocumentReference ||--}o Coding : "coding"
Relationship ||--|| IdentifiableElement : "subject"
Relationship ||--|| IdentifiableElement : "object"
Relationship ||--}o Coding : "coding"
IdentifiableElement ||--}o Coding : "coding"
ReifiedConcept ||--}o ConceptProperty : "properties"
ReifiedConcept ||--}o Coding : "coding"
ReifiedConcept ||--}o Comment : "comment"
ConceptProperty ||--|o CodeList : "codeList"
ConceptProperty ||--}o Coding : "coding"
ConceptProperty ||--}o Comment : "comment"
CodingMapping ||--|| Coding : "source"
CodingMapping ||--|| Coding : "target"
CodingMapping ||--}o Coding : "coding"
CodeList ||--|o Resource : "externalCodeList"
CodeList ||--}o Coding : "coding"
CodeList ||--}o Comment : "comment"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
Method ||--}o FormalExpression : "formalExpressions"
Method ||--|o DocumentReference : "document"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comment"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
WhereClause ||--}o Condition : "conditions"
WhereClause ||--}o Coding : "coding"
Condition ||--}o RangeCheck : "rangeChecks"
Condition ||--}o FormalExpression : "formalExpression"
Condition ||--}o Coding : "coding"
Condition ||--}o Comment : "comment"
ItemGroup ||--}o Item : "items"
ItemGroup ||--}o ItemGroup : "children"
ItemGroup ||--|o ReifiedConcept : "implementsConcept"
ItemGroup ||--|o WhereClause : "whereClause"
ItemGroup ||--}o Coding : "security"
ItemGroup ||--|o Timing : "validityPeriod"
ItemGroup ||--}o Coding : "coding"
ItemGroup ||--}o Comment : "comment"
Timing ||--|o NominalOccurrence : "relativeTo"
Timing ||--|o NominalOccurrence : "relativeFrom"
Timing ||--|o Method : "imputation"
Timing ||--}o Coding : "coding"
Item ||--|o CodeList : "codeList"
Item ||--|o Method : "method"
Item ||--}o RangeCheck : "rangeChecks"
Item ||--|o WhereClause : "whereClause"
Item ||--|o Origin : "origin"
Item ||--|o ConceptProperty : "conceptProperty"
Item ||--|o CodeList : "roleCodeList"
Item ||--|o Condition : "collectionExceptionCondition"
Item ||--}o Coding : "coding"
Item ||--}o Comment : "comment"

```




## Inheritance
* [GovernedElement](GovernedElement.md) [ [Identifiable](Identifiable.md) [Labelled](Labelled.md) [Governed](Governed.md)]
    * **MetaDataVersion**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [items](items.md) | * <br/> [Item](Item.md) | Items defined in this version of the metadata | direct |
| [itemGroups](itemGroups.md) | * <br/> [ItemGroup](ItemGroup.md) | Item groups defined in this version of the metadata | direct |
| [resources](resources.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[DocumentReference](DocumentReference.md)&nbsp;or&nbsp;<br />[Resource](Resource.md) | References to documents that describe this version of the metadata | direct |
| [conditions](conditions.md) | * <br/> [Condition](Condition.md) | Logical conditions that apply to this version of the metadata | direct |
| [whereClauses](whereClauses.md) | * <br/> [WhereClause](WhereClause.md) | Data contexts that apply to this version of the metadata | direct |
| [methods](methods.md) | * <br/> [Method](Method.md) | Methods defined in this version of the metadata | direct |
| [codeLists](codeLists.md) | * <br/> [CodeList](CodeList.md) | Code lists defined in this version of the metadata | direct |
| [codings](codings.md) | * <br/> [Coding](Coding.md) | Codings defined in this version of the metadata | direct |
| [mappings](mappings.md) | * <br/> [CodingMapping](CodingMapping.md) | Coding mappings in this version of the metadata | direct |
| [concepts](concepts.md) | * <br/> [ReifiedConcept](ReifiedConcept.md) | Structured Concepts defined in this version of the metadata | direct |
| [relationships](relationships.md) | * <br/> [Relationship](Relationship.md) | Relationships between items, item groups, and other elements in this version ... | direct |
| [OID](OID.md) | 1 <br/> [String](String.md) | Local identifier within this study/context | [Identifiable](Identifiable.md) |
| [uuid](uuid.md) | 0..1 <br/> [String](String.md) | Universal unique identifier | [Identifiable](Identifiable.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | Short name or identifier, used for field names | [Labelled](Labelled.md) |
| [description](description.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](Labelled.md) |
| [coding](coding.md) | * <br/> [Coding](Coding.md) | Semantic tags for this element | [Labelled](Labelled.md) |
| [label](label.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](Labelled.md) |
| [aliases](aliases.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Alternative name or identifier | [Labelled](Labelled.md) |
| [mandatory](mandatory.md) | 0..1 <br/> [Boolean](Boolean.md) | Is this element required? | [Governed](Governed.md) |
| [comment](comment.md) | * <br/> [Comment](Comment.md) | Comment on the element, such as a rationale for its inclusion or exclusion | [Governed](Governed.md) |
| [purpose](purpose.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Purpose or rationale for this data element | [Governed](Governed.md) |
| [lastUpdated](lastUpdated.md) | 0..1 <br/> [Datetime](Datetime.md) | When the resource was last updated | [Governed](Governed.md) |
| [owner](owner.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[User](User.md)&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md) | Party responsible for this element | [Governed](Governed.md) |
| [wasDerivedFrom](wasDerivedFrom.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[Item](Item.md)&nbsp;or&nbsp;<br />[ItemGroup](ItemGroup.md)&nbsp;or&nbsp;<br />[MetaDataVersion](MetaDataVersion.md)&nbsp;or&nbsp;<br />[CodeList](CodeList.md)&nbsp;or&nbsp;<br />[ReifiedConcept](ReifiedConcept.md)&nbsp;or&nbsp;<br />[ConceptProperty](ConceptProperty.md)&nbsp;or&nbsp;<br />[Condition](Condition.md)&nbsp;or&nbsp;<br />[Method](Method.md)&nbsp;or&nbsp;<br />[NominalOccurrence](NominalOccurrence.md)&nbsp;or&nbsp;<br />[Dataflow](Dataflow.md)&nbsp;or&nbsp;<br />[CubeComponent](CubeComponent.md)&nbsp;or&nbsp;<br />[DataProduct](DataProduct.md)&nbsp;or&nbsp;<br />[ProvisionAgreement](ProvisionAgreement.md) | Reference to another item that this item implements or extends, e | [Governed](Governed.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GovernedElement](GovernedElement.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Governed](Governed.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [MetaDataVersion](MetaDataVersion.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Item](Item.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [ItemGroup](ItemGroup.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [CodeList](CodeList.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [ReifiedConcept](ReifiedConcept.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [ConceptProperty](ConceptProperty.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Condition](Condition.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Method](Method.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [NominalOccurrence](NominalOccurrence.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [DataStructureDefinition](DataStructureDefinition.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Dataflow](Dataflow.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [CubeComponent](CubeComponent.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Measure](Measure.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [Dimension](Dimension.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [DataAttribute](DataAttribute.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [DataProduct](DataProduct.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |
| [ProvisionAgreement](ProvisionAgreement.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [MetaDataVersion](MetaDataVersion.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:MetaDataVersion |
| native | odm:MetaDataVersion |
| close | usdm:StudyDesign |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MetaDataVersion
description: A container element that represents a given version of a specification,
  linking to a particular usage context such as a study, dataset, or data collection
  instrument.
from_schema: https://cdisc.org/define-json
close_mappings:
- usdm:StudyDesign
is_a: GovernedElement
attributes:
  items:
    name: items
    description: Items defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    - ItemGroup
    - Parameter
    range: Item
    multivalued: true
    inlined: true
    inlined_as_list: true
  itemGroups:
    name: itemGroups
    description: Item groups defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: ItemGroup
    multivalued: true
    inlined: true
    inlined_as_list: true
  resources:
    name: resources
    description: References to documents that describe this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: DocumentReference
    - range: Resource
  conditions:
    name: conditions
    description: Logical conditions that apply to this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    - WhereClause
    range: Condition
    multivalued: true
    inlined: true
    inlined_as_list: true
  whereClauses:
    name: whereClauses
    description: Data contexts that apply to this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: WhereClause
    multivalued: true
    inlined: true
    inlined_as_list: true
  methods:
    name: methods
    description: Methods defined in this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: Method
    multivalued: true
    inlined: true
    inlined_as_list: true
  codeLists:
    name: codeLists
    description: Code lists defined in this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: CodeList
    multivalued: true
    inlined: true
    inlined_as_list: true
  codings:
    name: codings
    description: Codings defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  mappings:
    name: mappings
    description: Coding mappings in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: CodingMapping
    multivalued: true
    inlined: true
    inlined_as_list: true
  concepts:
    name: concepts
    description: Structured Concepts defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: ReifiedConcept
    multivalued: true
  relationships:
    name: relationships
    description: Relationships between items, item groups, and other elements in this
      version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - MetaDataVersion
    range: Relationship
    multivalued: true
    inlined: true
    inlined_as_list: true
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: MetaDataVersion
description: A container element that represents a given version of a specification,
  linking to a particular usage context such as a study, dataset, or data collection
  instrument.
from_schema: https://cdisc.org/define-json
close_mappings:
- usdm:StudyDesign
is_a: GovernedElement
attributes:
  items:
    name: items
    description: Items defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: items
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    - ItemGroup
    - Parameter
    range: Item
    multivalued: true
    inlined: true
    inlined_as_list: true
  itemGroups:
    name: itemGroups
    description: Item groups defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: itemGroups
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: ItemGroup
    multivalued: true
    inlined: true
    inlined_as_list: true
  resources:
    name: resources
    description: References to documents that describe this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: resources
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: DocumentReference
    - range: Resource
  conditions:
    name: conditions
    description: Logical conditions that apply to this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: conditions
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    - WhereClause
    range: Condition
    multivalued: true
    inlined: true
    inlined_as_list: true
  whereClauses:
    name: whereClauses
    description: Data contexts that apply to this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: whereClauses
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: WhereClause
    multivalued: true
    inlined: true
    inlined_as_list: true
  methods:
    name: methods
    description: Methods defined in this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: methods
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: Method
    multivalued: true
    inlined: true
    inlined_as_list: true
  codeLists:
    name: codeLists
    description: Code lists defined in this version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: codeLists
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: CodeList
    multivalued: true
    inlined: true
    inlined_as_list: true
  codings:
    name: codings
    description: Codings defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: codings
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  mappings:
    name: mappings
    description: Coding mappings in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: mappings
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: CodingMapping
    multivalued: true
    inlined: true
    inlined_as_list: true
  concepts:
    name: concepts
    description: Structured Concepts defined in this version of the metadata
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: concepts
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: ReifiedConcept
    multivalued: true
  relationships:
    name: relationships
    description: Relationships between items, item groups, and other elements in this
      version of the metadata.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: relationships
    owner: MetaDataVersion
    domain_of:
    - MetaDataVersion
    range: Relationship
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
    owner: MetaDataVersion
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
    owner: MetaDataVersion
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: MetaDataVersion
    domain_of:
    - Labelled
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: description
    owner: MetaDataVersion
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
    owner: MetaDataVersion
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
    owner: MetaDataVersion
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
    owner: MetaDataVersion
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
  mandatory:
    name: mandatory
    description: Is this element required?
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: mandatory
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: boolean
  comment:
    name: comment
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: comment
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: Comment
    multivalued: true
  purpose:
    name: purpose
    description: Purpose or rationale for this data element
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: purpose
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  lastUpdated:
    name: lastUpdated
    description: When the resource was last updated
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: lastUpdated
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: datetime
  owner:
    name: owner
    description: Party responsible for this element
    from_schema: https://cdisc.org/define-json
    narrow_mappings:
    - prov:wasAttributedTo
    - prov:wasAssociatedBy
    rank: 1000
    alias: owner
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: string
    any_of:
    - range: User
    - range: Organization
    - range: string
  wasDerivedFrom:
    name: wasDerivedFrom
    description: Reference to another item that this item implements or extends, e.g.
      a template Item definition.
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - prov:wasDerivedFrom
    rank: 1000
    alias: wasDerivedFrom
    owner: MetaDataVersion
    domain_of:
    - Governed
    range: string
    any_of:
    - range: Item
    - range: ItemGroup
    - range: MetaDataVersion
    - range: CodeList
    - range: ReifiedConcept
    - range: ConceptProperty
    - range: Condition
    - range: Method
    - range: NominalOccurrence
    - range: Dataflow
    - range: CubeComponent
    - range: DataProduct
    - range: ProvisionAgreement
tree_root: true

```
</details>