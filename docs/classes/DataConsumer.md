

# Class: DataConsumer 


_An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider._





URI: [odm:class/DataConsumer](https://cdisc.org/odm2/class/DataConsumer)


```mermaid
erDiagram
DataConsumer {
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
ProvisionAgreement {
    string consumer  
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
Policy {
    PolicyType policyType  
    string profile  
    string assigner  
    string assignee  
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
Dataflow {
    stringList deliverySchedule  
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

DataConsumer ||--}o Dataflow : "consumesDataFrom"
DataConsumer ||--}o ProvisionAgreement : "provisionAgreements"
DataConsumer ||--|o Organization : "partOfOrganization"
DataConsumer ||--}o Coding : "coding"
Organization ||--|o Organization : "partOfOrganization"
Organization ||--}o Coding : "coding"
ProvisionAgreement ||--|o DataProvider : "provider"
ProvisionAgreement ||--|o Dataflow : "dataFlow"
ProvisionAgreement ||--|o Resource : "source"
ProvisionAgreement ||--}o Policy : "hasPolicy"
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
Policy ||--}o Rule : "permission"
Policy ||--}o Rule : "prohibition"
Policy ||--}o Rule : "obligation"
Policy ||--}o Coding : "coding"
Policy ||--}o Comment : "comments"
Policy ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
Dataflow ||--|| DataStructureDefinition : "structure"
Dataflow ||--}o Dimension : "dimensionConstraint"
Dataflow ||--|o Analysis : "analysisMethod"
Dataflow ||--}o Coding : "coding"
Dataflow ||--}o Comment : "comments"
Dataflow ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DataProvider ||--}o Dataflow : "providesDataFor"
DataProvider ||--}o ProvisionAgreement : "provisionAgreements"
DataProvider ||--}o Resource : "source"
DataProvider ||--|o Organization : "partOfOrganization"
DataProvider ||--}o Coding : "coding"

```




## Inheritance
* [IdentifiableElement](../classes/IdentifiableElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md)]
    * [Organization](../classes/Organization.md)
        * **DataConsumer**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [consumesDataFrom](../slots/consumesDataFrom.md) | * <br/> [Dataflow](../classes/Dataflow.md) | The Dataflows that this consumer receives data from | direct |
| [provisionAgreements](../slots/provisionAgreements.md) | * <br/> [ProvisionAgreement](../classes/ProvisionAgreement.md) | The ProvisionAgreements that this consumer has with Data Providers | direct |
| [role](../slots/role.md) | 0..1 <br/> [String](../types/String.md) | The role of the organization in the study. | [Organization](../classes/Organization.md) |
| [type](../slots/type.md) | 0..1 <br/> [OrganizationType](../enums/OrganizationType.md) | The type of organization (e.g., site, sponsor, vendor). | [Organization](../classes/Organization.md) |
| [location](../slots/location.md) | 0..1 <br/> [String](../types/String.md) | The physical location of the organization. | [Organization](../classes/Organization.md) |
| [address](../slots/address.md) | 0..1 <br/> [String](../types/String.md) | The address of the organization. | [Organization](../classes/Organization.md) |
| [partOfOrganization](../slots/partOfOrganization.md) | 0..1 <br/> [Organization](../classes/Organization.md) | Reference to a parent organization if this organization is part of a larger entity. | [Organization](../classes/Organization.md) |
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
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | [consumer](../slots/consumer.md) | any_of[range] | [DataConsumer](../classes/DataConsumer.md) |
| [Policy](../classes/Policy.md) | [assignee](../slots/assignee.md) | any_of[range] | [DataConsumer](../classes/DataConsumer.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:DataConsumer |
| native | odm:DataConsumer |
| close | sdmx:DataConsumer |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataConsumer
description: An organization element that receives data from a Data Provider under
  a ProvisionAgreement; the demand-side counterpart of DataProvider.
from_schema: https://cdisc.org/data-definition-spec
close_mappings:
- sdmx:DataConsumer
is_a: Organization
attributes:
  consumesDataFrom:
    name: consumesDataFrom
    description: The Dataflows that this consumer receives data from
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    domain_of:
    - DataConsumer
    range: Dataflow
    multivalued: true
  provisionAgreements:
    name: provisionAgreements
    description: The ProvisionAgreements that this consumer has with Data Providers
    from_schema: https://cdisc.org/data-definition-spec
    domain_of:
    - DataProvider
    - DataConsumer
    range: ProvisionAgreement
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: DataConsumer
description: An organization element that receives data from a Data Provider under
  a ProvisionAgreement; the demand-side counterpart of DataProvider.
from_schema: https://cdisc.org/data-definition-spec
close_mappings:
- sdmx:DataConsumer
is_a: Organization
attributes:
  consumesDataFrom:
    name: consumesDataFrom
    description: The Dataflows that this consumer receives data from
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: consumesDataFrom
    owner: DataConsumer
    domain_of:
    - DataConsumer
    range: Dataflow
    multivalued: true
  provisionAgreements:
    name: provisionAgreements
    description: The ProvisionAgreements that this consumer has with Data Providers
    from_schema: https://cdisc.org/data-definition-spec
    alias: provisionAgreements
    owner: DataConsumer
    domain_of:
    - DataProvider
    - DataConsumer
    range: ProvisionAgreement
    multivalued: true
  role:
    name: role
    description: The role of the organization in the study.
    from_schema: https://cdisc.org/data-definition-spec
    alias: role
    owner: DataConsumer
    domain_of:
    - IsODMItem
    - Organization
    - CubeComponent
    range: string
  type:
    name: type
    description: The type of organization (e.g., site, sponsor, vendor).
    from_schema: https://cdisc.org/data-definition-spec
    alias: type
    owner: DataConsumer
    domain_of:
    - ItemGroup
    - Method
    - Origin
    - Organization
    - Standard
    - Timing
    range: OrganizationType
  location:
    name: location
    description: The physical location of the organization.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: location
    owner: DataConsumer
    domain_of:
    - Organization
    - Display
    range: string
  address:
    name: address
    description: The address of the organization.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: address
    owner: DataConsumer
    domain_of:
    - Organization
    range: string
  partOfOrganization:
    name: partOfOrganization
    description: Reference to a parent organization if this organization is part of
      a larger entity.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: partOfOrganization
    owner: DataConsumer
    domain_of:
    - Organization
    range: Organization
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    identifier: true
    alias: OID
    owner: DataConsumer
    domain_of:
    - Identifiable
    range: string
    required: true
  uuid:
    name: uuid
    description: Universal unique identifier
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: uuid
    owner: DataConsumer
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: name
    owner: DataConsumer
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: description
    owner: DataConsumer
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
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: coding
    owner: DataConsumer
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
    from_schema: https://cdisc.org/data-definition-spec
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    alias: label
    owner: DataConsumer
    domain_of:
    - Labelled
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  aliases:
    name: aliases
    description: Alternative name or identifier
    from_schema: https://cdisc.org/data-definition-spec
    exact_mappings:
    - skos:altLabel
    rank: 1000
    alias: aliases
    owner: DataConsumer
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