

# Class: User 


_An entity that represents information about a specific user of a clinical data collection or data management system_





URI: [odm:class/User](https://cdisc.org/odm2/class/User)


```mermaid
erDiagram
User {
    UserType userType  
    string userName  
    string fullName  
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

User ||--|o Organization : "organization"
User ||--}o Coding : "coding"
Organization ||--|o Organization : "partOfOrganization"
Organization ||--}o Coding : "coding"

```




## Inheritance
* [IdentifiableElement](../classes/IdentifiableElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md)]
    * **User**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [userType](../slots/userType.md) | 0..1 <br/> [UserType](../enums/UserType.md) | User's role in the study. | direct |
| [userName](../slots/userName.md) | 0..1 <br/> [String](../types/String.md) | The username of the user. | direct |
| [fullName](../slots/fullName.md) | 0..1 <br/> [String](../types/String.md) | The full name of the user. | direct |
| [organization](../slots/organization.md) | 0..1 <br/> [Organization](../classes/Organization.md) | The organization the user belongs to. | direct |
| [OID](../slots/OID.md) | 1 <br/> [String](../types/String.md) | Local identifier within this study/context. Use CDISC OID format for regulatory submissions, or simple strings for internal use. | [Identifiable](../classes/Identifiable.md) |
| [uuid](../slots/uuid.md) | 0..1 <br/> [String](../types/String.md) | Universal unique identifier | [Identifiable](../classes/Identifiable.md) |
| [name](../slots/name.md) | 0..1 <br/> [String](../types/String.md) | Short name or identifier, used for field names | [Labelled](../classes/Labelled.md) |
| [description](../slots/description.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](../classes/Labelled.md) |
| [coding](../slots/coding.md) | * <br/> [Coding](../classes/Coding.md) | Semantic tags for this element | [Labelled](../classes/Labelled.md) |
| [label](../slots/label.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](../classes/Labelled.md) |
| [aliases](../slots/aliases.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Alternative name or identifier | [Labelled](../classes/Labelled.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GovernedElement](../classes/GovernedElement.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Governed](../classes/Governed.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [IsProfile](../classes/IsProfile.md) | [authenticator](../slots/authenticator.md) | any_of[range] | [User](../classes/User.md) |
| [MetaDataVersion](../classes/MetaDataVersion.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Item](../classes/Item.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [ItemGroup](../classes/ItemGroup.md) | [authenticator](../slots/authenticator.md) | any_of[range] | [User](../classes/User.md) |
| [ItemGroup](../classes/ItemGroup.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [CodeList](../classes/CodeList.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Comment](../classes/Comment.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [ReifiedConcept](../classes/ReifiedConcept.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [ConceptProperty](../classes/ConceptProperty.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [WhereClause](../classes/WhereClause.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Condition](../classes/Condition.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Method](../classes/Method.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | [source](../slots/source.md) | any_of[range] | [User](../classes/User.md) |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [NominalOccurrence](../classes/NominalOccurrence.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [authenticator](../slots/authenticator.md) | any_of[range] | [User](../classes/User.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Dataflow](../classes/Dataflow.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Dataset](../classes/Dataset.md) | [authenticator](../slots/authenticator.md) | any_of[range] | [User](../classes/User.md) |
| [CubeComponent](../classes/CubeComponent.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Measure](../classes/Measure.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Dimension](../classes/Dimension.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [DataAttribute](../classes/DataAttribute.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [DataProduct](../classes/DataProduct.md) | [dataProductOwner](../slots/dataProductOwner.md) | any_of[range] | [User](../classes/User.md) |
| [DataProduct](../classes/DataProduct.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Analysis](../classes/Analysis.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |
| [Display](../classes/Display.md) | [owner](../slots/owner.md) | any_of[range] | [User](../classes/User.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:User |
| native | odm:User |
| exact | odm:User |
| broad | prov:Agent |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: User
description: An entity that represents information about a specific user of a clinical
  data collection or data management system
from_schema: https://cdisc.org/define-json
exact_mappings:
- odm:User
broad_mappings:
- prov:Agent
is_a: IdentifiableElement
attributes:
  userType:
    name: userType
    description: User's role in the study.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - User
    range: UserType
  userName:
    name: userName
    description: The username of the user.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - User
    range: string
  fullName:
    name: fullName
    description: The full name of the user.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - User
    range: string
  organization:
    name: organization
    description: The organization the user belongs to.
    from_schema: https://cdisc.org/define-json
    close_mappings:
    - prov:actedOnBehalfOf
    rank: 1000
    domain_of:
    - User
    range: Organization

```
</details>

### Induced

<details>
```yaml
name: User
description: An entity that represents information about a specific user of a clinical
  data collection or data management system
from_schema: https://cdisc.org/define-json
exact_mappings:
- odm:User
broad_mappings:
- prov:Agent
is_a: IdentifiableElement
attributes:
  userType:
    name: userType
    description: User's role in the study.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: userType
    owner: User
    domain_of:
    - User
    range: UserType
  userName:
    name: userName
    description: The username of the user.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: userName
    owner: User
    domain_of:
    - User
    range: string
  fullName:
    name: fullName
    description: The full name of the user.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: fullName
    owner: User
    domain_of:
    - User
    range: string
  organization:
    name: organization
    description: The organization the user belongs to.
    from_schema: https://cdisc.org/define-json
    close_mappings:
    - prov:actedOnBehalfOf
    rank: 1000
    alias: organization
    owner: User
    domain_of:
    - User
    range: Organization
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: User
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
    owner: User
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: User
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
    owner: User
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
    owner: User
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
    owner: User
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
    owner: User
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