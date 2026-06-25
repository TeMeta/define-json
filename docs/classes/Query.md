

# Class: Query 


_A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source._





URI: [dds:class/Query](https://w3id.org/dds/class/Query)


```mermaid
erDiagram
Query {
    QueryType queryType  
    string text  
    string status  
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
IdentifiableElement {
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}

Query ||--}| IdentifiableElement : "about"
Query ||--}o Coding : "coding"
Query ||--}o Comment : "comments"
Query ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
IdentifiableElement ||--}o Coding : "coding"

```




## Inheritance
* [GovernedElement](../classes/GovernedElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md) [Governed](../classes/Governed.md)]
    * **Query**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [about](../slots/about.md) | 1..* <br/> [IdentifiableElement](../classes/IdentifiableElement.md) | The metadata and/or data element(s) this query concerns, referenced by OID. Multivalued and non-inlined to support many-to-many linkage across both metadata (e.g. Item, ItemGroup) and data (e.g. Dataset) elements. | direct |
| [queryType](../slots/queryType.md) | 0..1 <br/> [QueryType](../enums/QueryType.md) | Whether the query is internal or external (e.g. site or sponsor originated). | direct |
| [text](../slots/text.md) | 1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | The query content. | direct |
| [status](../slots/status.md) | 0..1 <br/> [String](../types/String.md) | Workflow status of the query (e.g. open, answered, closed). | direct |
| [source](../slots/source.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[User](../classes/User.md)&nbsp;or&nbsp;<br />[Organization](../classes/Organization.md)&nbsp;or&nbsp;<br />[String](../types/String.md) | The party that raised the query. | direct |
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
| [wasDerivedFrom](../slots/wasDerivedFrom.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Item](../classes/Item.md)&nbsp;or&nbsp;<br />[ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[Specification](../classes/Specification.md)&nbsp;or&nbsp;<br />[CodeList](../classes/CodeList.md)&nbsp;or&nbsp;<br />[Concept](../classes/Concept.md)&nbsp;or&nbsp;<br />[ConceptProperty](../classes/ConceptProperty.md)&nbsp;or&nbsp;<br />[LogicalPredicate](../classes/LogicalPredicate.md)&nbsp;or&nbsp;<br />[Method](../classes/Method.md)&nbsp;or&nbsp;<br />[Dataflow](../classes/Dataflow.md)&nbsp;or&nbsp;<br />[CubeComponent](../classes/CubeComponent.md)&nbsp;or&nbsp;<br />[DataProduct](../classes/DataProduct.md)&nbsp;or&nbsp;<br />[ProvisionAgreement](../classes/ProvisionAgreement.md) | Reference to another item that this item implements or extends, e.g. a template Item definition. | [Governed](../classes/Governed.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Specification](../classes/Specification.md) | [queries](../slots/queries.md) | range | [Query](../classes/Query.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:Query |
| native | dds:Query |
| close | odm:Query |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Query
description: A reified query (discrepancy, request for clarification, or annotation)
  raised against one or more metadata and/or data elements. Modelled as an intermediate
  relationship node so a single query can relate to many elements (many-to-many) and
  be referenced rather than embedded. Internal queries originate within the organization;
  external queries (e.g. site or sponsor) carry their source.
from_schema: https://w3id.org/dds
close_mappings:
- odm:Query
is_a: GovernedElement
attributes:
  about:
    name: about
    description: The metadata and/or data element(s) this query concerns, referenced
      by OID. Multivalued and non-inlined to support many-to-many linkage across both
      metadata (e.g. Item, ItemGroup) and data (e.g. Dataset) elements.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Query
    range: IdentifiableElement
    required: true
    multivalued: true
    inlined: false
  queryType:
    name: queryType
    description: Whether the query is internal or external (e.g. site or sponsor originated).
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Query
    range: QueryType
  text:
    name: text
    description: The query content.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Query
    - Comment
    - SiteOrSponsorComment
    required: true
    any_of:
    - range: string
    - range: TranslatedText
  status:
    name: status
    description: Workflow status of the query (e.g. open, answered, closed).
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Query
    - Standard
  source:
    name: source
    description: The party that raised the query.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Query
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
name: Query
description: A reified query (discrepancy, request for clarification, or annotation)
  raised against one or more metadata and/or data elements. Modelled as an intermediate
  relationship node so a single query can relate to many elements (many-to-many) and
  be referenced rather than embedded. Internal queries originate within the organization;
  external queries (e.g. site or sponsor) carry their source.
from_schema: https://w3id.org/dds
close_mappings:
- odm:Query
is_a: GovernedElement
attributes:
  about:
    name: about
    description: The metadata and/or data element(s) this query concerns, referenced
      by OID. Multivalued and non-inlined to support many-to-many linkage across both
      metadata (e.g. Item, ItemGroup) and data (e.g. Dataset) elements.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: about
    owner: Query
    domain_of:
    - Query
    range: IdentifiableElement
    required: true
    multivalued: true
    inlined: false
  queryType:
    name: queryType
    description: Whether the query is internal or external (e.g. site or sponsor originated).
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: queryType
    owner: Query
    domain_of:
    - Query
    range: QueryType
  text:
    name: text
    description: The query content.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: text
    owner: Query
    domain_of:
    - Query
    - Comment
    - SiteOrSponsorComment
    range: string
    required: true
    any_of:
    - range: string
    - range: TranslatedText
  status:
    name: status
    description: Workflow status of the query (e.g. open, answered, closed).
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: status
    owner: Query
    domain_of:
    - Query
    - Standard
    range: string
  source:
    name: source
    description: The party that raised the query.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: source
    owner: Query
    domain_of:
    - Query
    - Origin
    - SiteOrSponsorComment
    - DataProvider
    - ProvisionAgreement
    range: string
    any_of:
    - range: User
    - range: Organization
    - range: string
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://w3id.org/dds
    rank: 1000
    identifier: true
    alias: OID
    owner: Query
    domain_of:
    - Identifiable
    range: string
    required: true
  uuid:
    name: uuid
    description: Universal unique identifier
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: uuid
    owner: Query
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: name
    owner: Query
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: description
    owner: Query
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
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: coding
    owner: Query
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
    from_schema: https://w3id.org/dds
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    alias: label
    owner: Query
    domain_of:
    - Labelled
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  aliases:
    name: aliases
    description: Alternative name or identifier
    from_schema: https://w3id.org/dds
    exact_mappings:
    - skos:altLabel
    rank: 1000
    alias: aliases
    owner: Query
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
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: mandatory
    owner: Query
    domain_of:
    - Governed
    range: boolean
  comments:
    name: comments
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: comments
    owner: Query
    domain_of:
    - Governed
    range: Comment
    multivalued: true
    inlined: false
  siteOrSponsorComments:
    name: siteOrSponsorComments
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: siteOrSponsorComments
    owner: Query
    domain_of:
    - Governed
    range: SiteOrSponsorComment
    multivalued: true
    inlined: false
  purpose:
    name: purpose
    description: Purpose or rationale for this data element
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: purpose
    owner: Query
    domain_of:
    - Governed
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  lastUpdated:
    name: lastUpdated
    description: When the resource was last updated
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: lastUpdated
    owner: Query
    domain_of:
    - Governed
    range: datetime
  owner:
    name: owner
    description: Party responsible for this element
    from_schema: https://w3id.org/dds
    narrow_mappings:
    - prov:wasAttributedTo
    - prov:wasAssociatedBy
    rank: 1000
    alias: owner
    owner: Query
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
    from_schema: https://w3id.org/dds
    exact_mappings:
    - prov:wasDerivedFrom
    rank: 1000
    alias: wasDerivedFrom
    owner: Query
    domain_of:
    - Governed
    range: string
    any_of:
    - range: Item
    - range: ItemGroup
    - range: Specification
    - range: CodeList
    - range: Concept
    - range: ConceptProperty
    - range: LogicalPredicate
    - range: Method
    - range: Dataflow
    - range: CubeComponent
    - range: DataProduct
    - range: ProvisionAgreement

```
</details>