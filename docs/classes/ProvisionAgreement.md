

# Class: ProvisionAgreement 


_An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision_





URI: [odm:class/ProvisionAgreement](https://cdisc.org/odm2/class/ProvisionAgreement)



```mermaid
erDiagram
ProvisionAgreement {
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
Dataflow {
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
Dimension {
    integer keySequence  
    string role  
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
DataStructureDefinition {
    boolean evolvingStructure  
    string domain  
    string structure  
    boolean isReferenceData  
    ItemGroupType type  
    stringList children  
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
DataProvider {
    string role  
    OrganizationType type  
    string location  
    string address  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Organization {
    string role  
    OrganizationType type  
    string location  
    string address  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}

ProvisionAgreement ||--|o DataProvider : "provider"
ProvisionAgreement ||--|o Dataflow : "dataFlow"
ProvisionAgreement ||--|o Resource : "source"
ProvisionAgreement ||--}o Coding : "coding"
ProvisionAgreement ||--}o Comment : "comments"
ProvisionAgreement ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
Dataflow ||--|| DataStructureDefinition : "structure"
Dataflow ||--}o Dimension : "dimensionConstraint"
Dataflow ||--}o Coding : "coding"
Dataflow ||--}o Comment : "comments"
Dataflow ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Dimension ||--|| Item : "item"
Dimension ||--|o Method : "missingHandling"
Dimension ||--|o Method : "imputation"
Dimension ||--}o Coding : "coding"
Dimension ||--}o Comment : "comments"
Dimension ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DataStructureDefinition ||--}o Dimension : "dimensions"
DataStructureDefinition ||--}o Measure : "measures"
DataStructureDefinition ||--}o DataAttribute : "attributes"
DataStructureDefinition ||--|o ComponentList : "grouping"
DataStructureDefinition ||--}o Item : "items"
DataStructureDefinition ||--|o ReifiedConcept : "implementsConcept"
DataStructureDefinition ||--}o WhereClause : "applicableWhen"
DataStructureDefinition ||--}o Coding : "security"
DataStructureDefinition ||--|o Timing : "validityPeriod"
DataStructureDefinition ||--}o Coding : "coding"
DataStructureDefinition ||--}o Comment : "comments"
DataStructureDefinition ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DataProvider ||--}o Dataflow : "providesDataFor"
DataProvider ||--}o ProvisionAgreement : "provisionAgreements"
DataProvider ||--}o Resource : "source"
DataProvider ||--|o Organization : "partOfOrganization"
DataProvider ||--}o Coding : "coding"
Organization ||--|o Organization : "partOfOrganization"
Organization ||--}o Coding : "coding"

```




## Inheritance
* [GovernedElement](../classes/GovernedElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md) [Governed](../classes/Governed.md)]
    * **ProvisionAgreement** [ [Versioned](../classes/Versioned.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [provider](../slots/provider.md) | 0..1 <br/> [DataProvider](../classes/DataProvider.md) | The Data Provider that is part of this agreement | direct |
| [dataFlow](../slots/dataFlow.md) | 0..1 <br/> [Dataflow](../classes/Dataflow.md) | The Dataflow that is covered by this agreement | direct |
| [source](../slots/source.md) | 0..1 <br/> [Resource](../classes/Resource.md) | The source of the data provided under this agreement | direct |
| [version](../slots/version.md) | 0..1 <br/> [String](../types/String.md) | The version of the external resources | [Versioned](../classes/Versioned.md) |
| [href](../slots/href.md) | 0..1 <br/> [String](../types/String.md) | Machine-readable instructions to obtain the resource e.g. FHIR path, URL | [Versioned](../classes/Versioned.md) |
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
| [GovernedElement](../classes/GovernedElement.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Governed](../classes/Governed.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [MetaDataVersion](../classes/MetaDataVersion.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Item](../classes/Item.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [ItemGroup](../classes/ItemGroup.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [CodeList](../classes/CodeList.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Comment](../classes/Comment.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [ReifiedConcept](../classes/ReifiedConcept.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [ConceptProperty](../classes/ConceptProperty.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [WhereClause](../classes/WhereClause.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Condition](../classes/Condition.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Method](../classes/Method.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [NominalOccurrence](../classes/NominalOccurrence.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Dataflow](../classes/Dataflow.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [CubeComponent](../classes/CubeComponent.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Measure](../classes/Measure.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [Dimension](../classes/Dimension.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [DataAttribute](../classes/DataAttribute.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [DataProduct](../classes/DataProduct.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [DataProvider](../classes/DataProvider.md) | [provisionAgreements](../slots/provisionAgreements.md) | range | [ProvisionAgreement](../classes/ProvisionAgreement.md) |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [ProvisionAgreement](../classes/ProvisionAgreement.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:ProvisionAgreement |
| native | odm:ProvisionAgreement |
| close | sdmx:ProvisionAgreement |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ProvisionAgreement
description: An agreement element that describes the contractual relationship between
  a Data Provider and a Data Consumer regarding data provision
from_schema: https://cdisc.org/define-json
close_mappings:
- sdmx:ProvisionAgreement
is_a: GovernedElement
mixins:
- Versioned
attributes:
  provider:
    name: provider
    description: The Data Provider that is part of this agreement
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - ProvisionAgreement
    range: DataProvider
  dataFlow:
    name: dataFlow
    description: The Dataflow that is covered by this agreement
    from_schema: https://cdisc.org/define-json
    domain_of:
    - DataflowRelationship
    - ProvisionAgreement
    range: Dataflow
  source:
    name: source
    description: The source of the data provided under this agreement
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Origin
    - SiteOrSponsorComment
    - DataProvider
    - ProvisionAgreement
    range: Resource

```
</details>

### Induced

<details>
```yaml
name: ProvisionAgreement
description: An agreement element that describes the contractual relationship between
  a Data Provider and a Data Consumer regarding data provision
from_schema: https://cdisc.org/define-json
close_mappings:
- sdmx:ProvisionAgreement
is_a: GovernedElement
mixins:
- Versioned
attributes:
  provider:
    name: provider
    description: The Data Provider that is part of this agreement
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: provider
    owner: ProvisionAgreement
    domain_of:
    - ProvisionAgreement
    range: DataProvider
  dataFlow:
    name: dataFlow
    description: The Dataflow that is covered by this agreement
    from_schema: https://cdisc.org/define-json
    alias: dataFlow
    owner: ProvisionAgreement
    domain_of:
    - DataflowRelationship
    - ProvisionAgreement
    range: Dataflow
  source:
    name: source
    description: The source of the data provided under this agreement
    from_schema: https://cdisc.org/define-json
    alias: source
    owner: ProvisionAgreement
    domain_of:
    - Origin
    - SiteOrSponsorComment
    - DataProvider
    - ProvisionAgreement
    range: Resource
  version:
    name: version
    description: The version of the external resources
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: version
    owner: ProvisionAgreement
    domain_of:
    - Versioned
    - Standard
    range: string
  href:
    name: href
    description: Machine-readable instructions to obtain the resource e.g. FHIR path,
      URL
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: href
    owner: ProvisionAgreement
    domain_of:
    - Versioned
    range: string
    required: false
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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
    owner: ProvisionAgreement
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