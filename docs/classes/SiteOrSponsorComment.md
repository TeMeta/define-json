

# Class: SiteOrSponsorComment 


_A feedback element that contains comments from a site or sponsor, distinct from the general Comment class_





URI: [odm:class/SiteOrSponsorComment](https://cdisc.org/odm2/class/SiteOrSponsorComment)


```mermaid
erDiagram
SiteOrSponsorComment {
    string text  
    OriginSource sourceType  
    string source  
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
    boolean mandatory  
    string purpose  
    datetime lastUpdated  
    string owner  
    string wasDerivedFrom  
}
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
    AliasPredicate aliasType  
}
DocumentReference {
    string title  
    string leafID  
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

SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DocumentReference ||--}o Coding : "coding"

```




## Inheritance
* [GovernedElement](../classes/GovernedElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md) [Governed](../classes/Governed.md)]
    * **SiteOrSponsorComment**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [text](../slots/text.md) | 1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | The comment text. | direct |
| [sourceType](../slots/sourceType.md) | 0..1 <br/> [OriginSource](../enums/OriginSource.md) | who made the comment, such as Investigator, Sponsor. | direct |
| [source](../slots/source.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md) | ID of the comment provider | direct |
| [OID](../slots/OID.md) | 1 <br/> [String](../types/String.md) | Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use. | [Identifiable](../classes/Identifiable.md) |
| [uuid](../slots/uuid.md) | 0..1 <br/> [String](../types/String.md) | Universal unique identifier | [Identifiable](../classes/Identifiable.md) |
| [name](../slots/name.md) | 0..1 <br/> [String](../types/String.md) | Short name or identifier, used for field names | [Labelled](../classes/Labelled.md) |
| [description](../slots/description.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](../classes/Labelled.md) |
| [coding](../slots/coding.md) | * <br/> [Coding](../classes/Coding.md) | Semantic tags for this element | [Labelled](../classes/Labelled.md) |
| [label](../slots/label.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](../classes/Labelled.md) |
| [aliases](../slots/aliases.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Alternative name or identifier | [Labelled](../classes/Labelled.md) |
| [mandatory](../slots/mandatory.md) | 0..1 <br/> [Boolean](../types/Boolean.md) | Is this element required? | [Governed](../classes/Governed.md) |
| [comments](../slots/comments.md) | * <br/> [Comment](../classes/Comment.md) | Comment on the element, such as a rationale for its inclusion or exclusion | [Governed](../classes/Governed.md) |
| [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | * <br/> [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | Comment on the element, such as a rationale for its inclusion or exclusion | [Governed](../classes/Governed.md) |
| [purpose](../slots/purpose.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Purpose or rationale for this data element | [Governed](../classes/Governed.md) |
| [lastUpdated](../slots/lastUpdated.md) | 0..1 <br/> [Datetime](../types/Datetime.md) | When the resource was last updated | [Governed](../classes/Governed.md) |
| [owner](../slots/owner.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md) | Party responsible for this element | [Governed](../classes/Governed.md) |
| [wasDerivedFrom](../slots/wasDerivedFrom.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Item](../classes/Item.md)&nbsp;or&nbsp;<br />[ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[MetaDataVersion](../classes/MetaDataVersion.md)&nbsp;or&nbsp;<br />[CodeList](../classes/CodeList.md)&nbsp;or&nbsp;<br />[ReifiedConcept](../classes/ReifiedConcept.md)&nbsp;or&nbsp;<br />[ConceptProperty](../classes/ConceptProperty.md)&nbsp;or&nbsp;<br />[Condition](../classes/Condition.md)&nbsp;or&nbsp;<br />[Method](../classes/Method.md)&nbsp;or&nbsp;<br />[NominalOccurrence](../classes/NominalOccurrence.md)&nbsp;or&nbsp;<br />[Dataflow](../classes/Dataflow.md)&nbsp;or&nbsp;<br />[CubeComponent](../classes/CubeComponent.md)&nbsp;or&nbsp;<br />[DataProduct](../classes/DataProduct.md)&nbsp;or&nbsp;<br />[ProvisionAgreement](../classes/ProvisionAgreement.md) | Reference to another item that this item implements or extends, e.g. a template Item definition. | [Governed](../classes/Governed.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GovernedElement](../classes/GovernedElement.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Governed](../classes/Governed.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [MetaDataVersion](../classes/MetaDataVersion.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Item](../classes/Item.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [ItemGroup](../classes/ItemGroup.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [CodeList](../classes/CodeList.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Comment](../classes/Comment.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [ReifiedConcept](../classes/ReifiedConcept.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [ConceptProperty](../classes/ConceptProperty.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [WhereClause](../classes/WhereClause.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Condition](../classes/Condition.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Method](../classes/Method.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [NominalOccurrence](../classes/NominalOccurrence.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Dataflow](../classes/Dataflow.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [CubeComponent](../classes/CubeComponent.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Measure](../classes/Measure.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Dimension](../classes/Dimension.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [DataAttribute](../classes/DataAttribute.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [DataProduct](../classes/DataProduct.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Analysis](../classes/Analysis.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |
| [Display](../classes/Display.md) | [siteOrSponsorComments](../slots/siteOrSponsorComments.md) | range | [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:SiteOrSponsorComment |
| native | odm:SiteOrSponsorComment |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SiteOrSponsorComment
description: A feedback element that contains comments from a site or sponsor, distinct
  from the general Comment class
from_schema: https://cdisc.org/define-json
is_a: GovernedElement
attributes:
  text:
    name: text
    description: The comment text.
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Comment
    - SiteOrSponsorComment
    required: true
    any_of:
    - range: string
    - range: TranslatedText
  sourceType:
    name: sourceType
    description: who made the comment, such as Investigator, Sponsor.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - SiteOrSponsorComment
    range: OriginSource
  source:
    name: source
    description: ID of the comment provider
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Origin
    - SiteOrSponsorComment
    - DataProvider
    - ProvisionAgreement
    any_of:
    - range: User
    - range: Organization
    - range: string

```
</details>

### Induced

<details>
```yaml
name: SiteOrSponsorComment
description: A feedback element that contains comments from a site or sponsor, distinct
  from the general Comment class
from_schema: https://cdisc.org/define-json
is_a: GovernedElement
attributes:
  text:
    name: text
    description: The comment text.
    from_schema: https://cdisc.org/define-json
    alias: text
    owner: SiteOrSponsorComment
    domain_of:
    - Comment
    - SiteOrSponsorComment
    required: true
    any_of:
    - range: string
    - range: TranslatedText
  sourceType:
    name: sourceType
    description: who made the comment, such as Investigator, Sponsor.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: sourceType
    owner: SiteOrSponsorComment
    domain_of:
    - SiteOrSponsorComment
    range: OriginSource
  source:
    name: source
    description: ID of the comment provider
    from_schema: https://cdisc.org/define-json
    alias: source
    owner: SiteOrSponsorComment
    domain_of:
    - Origin
    - SiteOrSponsorComment
    - DataProvider
    - ProvisionAgreement
    any_of:
    - range: User
    - range: Organization
    - range: string
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: SiteOrSponsorComment
    domain_of:
    - Identifiable
    range: string
    required: true
  uuid:
    name: uuid
    description: Universal unique identifier
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: uuid
    owner: SiteOrSponsorComment
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
    domain_of:
    - Governed
    range: boolean
  comments:
    name: comments
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: comments
    owner: SiteOrSponsorComment
    domain_of:
    - Governed
    range: Comment
    multivalued: true
    inlined: false
  siteOrSponsorComments:
    name: siteOrSponsorComments
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: siteOrSponsorComments
    owner: SiteOrSponsorComment
    domain_of:
    - Governed
    range: SiteOrSponsorComment
    multivalued: true
    inlined: false
  purpose:
    name: purpose
    description: Purpose or rationale for this data element
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: purpose
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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
    owner: SiteOrSponsorComment
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

```
</details>