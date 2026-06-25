

# Class: Specification 


_The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here._





URI: [dds:class/Specification](https://w3id.org/dds/class/Specification)


```mermaid
erDiagram
Specification {
    stringList resources  
    string usdmStudyDesignId  
    string studyOID  
    string studyName  
    string studyDescription  
    string protocolName  
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
Display {
    string displayType  
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
Analysis {
    string analysisReason  
    string analysisPurpose  
    stringList inputData  
    string version  
    string href  
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
DataProduct {
    string dataProductOwner  
    string domain  
    DataProductLifecycleStatus lifecycleStatus  
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
Dataset {
    string publishedBy  
    stringList keys  
    string datasetType  
    string conformsTo  
    string informationSensitivityClassification  
    string version  
    string href  
    stringList profile  
    string authenticator  
    string action  
    string reportingBegin  
    string reportingEnd  
    string dataExtractionDate  
    string validFrom  
    string validTo  
    string publicationYear  
    string publicationPeriod  
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
DataService {
    string protocol  
    string securitySchemaType  
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
Standard {
    StandardName name  
    StandardType type  
    PublishingSet publishingSet  
    string version  
    StandardStatus status  
    string OID  
    string uuid  
    string description  
    string label  
    stringList aliases  
}
Dictionary {
    string publishedBy  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Check {
    string publishedBy  
    uriorcurie externalReference  
    SoftHard severity  
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
IdentifiableElement {
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
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
Concept {
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
CodeList {
    DataType dataType  
    string formatName  
    string version  
    string href  
    boolean isNonStandard  
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
CodeListItem {
    string codedValue  
    string decode  
    string description  
    stringList aliases  
    decimal weight  
    boolean other  
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
ApplicabilityCondition {
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
LogicalPredicate {
    string implementsPredicate  
    LogicalOperator operator  
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
Item {
    DataType dataType  
    integer length  
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
Origin {
    OriginType type  
    OriginSource source  
}
RangeCheck {
    Comparator comparator  
    stringList checkValues  
    string item  
    SoftHard softHard  
    LogicalOperator operator  
}
ItemGroup {
    string domain  
    string structure  
    boolean isReferenceData  
    ItemGroupType type  
    boolean hasNoData  
    stringList profile  
    string authenticator  
    boolean isNonStandard  
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
    string relativeTo  
    string relativeFrom  
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
DefClass {
    string name  
}

Specification ||--}o ItemGroup : "itemGroups"
Specification ||--}o Item : "items"
Specification ||--}o LogicalPredicate : "predicates"
Specification ||--}o ApplicabilityCondition : "applicabilityConditions"
Specification ||--}o Method : "methods"
Specification ||--}o Analysis : "analyses"
Specification ||--}o CodeList : "codeLists"
Specification ||--}o Coding : "codings"
Specification ||--}o Concept : "concepts"
Specification ||--}o Relationship : "relationships"
Specification ||--}o Query : "queries"
Specification ||--}o Check : "checks"
Specification ||--}o Dictionary : "dictionaries"
Specification ||--}o Standard : "standards"
Specification ||--}o DocumentReference : "annotatedCRFs"
Specification ||--}o DataProduct : "dataProducts"
Specification ||--}o Display : "displays"
Specification ||--}o Coding : "coding"
Specification ||--}o Comment : "comments"
Specification ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Display ||--|o Analysis : "analysis"
Display ||--}o DocumentReference : "location"
Display ||--}o Coding : "coding"
Display ||--}o Comment : "comments"
Display ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DocumentReference ||--}o Coding : "coding"
Analysis ||--|o Method : "analysisMethod"
Analysis ||--}o ApplicabilityCondition : "applicableWhen"
Analysis ||--}o Dataflow : "inputDataflows"
Analysis ||--}o FormalExpression : "expressions"
Analysis ||--}o DocumentReference : "documents"
Analysis ||--|o Concept : "implementsConcept"
Analysis ||--}o Coding : "coding"
Analysis ||--}o Comment : "comments"
Analysis ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DataProduct ||--}o DataService : "inputPort"
DataProduct ||--}o DataService : "outputPort"
DataProduct ||--}o Dataflow : "inputDataflow"
DataProduct ||--}o Dataflow : "outputDataflow"
DataProduct ||--}o Dataset : "inputDataset"
DataProduct ||--}o Dataset : "outputDataset"
DataProduct ||--}o Policy : "hasPolicy"
DataProduct ||--}o ProvisionAgreement : "provisionAgreement"
DataProduct ||--}o Coding : "coding"
DataProduct ||--}o Comment : "comments"
DataProduct ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
ProvisionAgreement ||--|o DataProvider : "provider"
ProvisionAgreement ||--|o Dataflow : "dataFlow"
ProvisionAgreement ||--|o Resource : "source"
ProvisionAgreement ||--}o Policy : "hasPolicy"
ProvisionAgreement ||--}o Coding : "coding"
ProvisionAgreement ||--}o Comment : "comments"
ProvisionAgreement ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Policy ||--}o Rule : "permission"
Policy ||--}o Rule : "prohibition"
Policy ||--}o Rule : "obligation"
Policy ||--}o Coding : "coding"
Policy ||--}o Comment : "comments"
Policy ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Dataset ||--|o Dataflow : "describedBy"
Dataset ||--|o DataStructureDefinition : "structuredBy"
Dataset ||--}o Distribution : "distribution"
Dataset ||--}o Policy : "hasPolicy"
Dataset ||--}o Coding : "security"
Dataset ||--|o Timing : "validityPeriod"
Dataset ||--}o Coding : "coding"
Dataflow ||--|| DataStructureDefinition : "structure"
Dataflow ||--}o Dimension : "dimensionConstraint"
Dataflow ||--}o Coding : "coding"
Dataflow ||--}o Comment : "comments"
Dataflow ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DataService ||--|o Distribution : "isAccessServiceOf"
DataService ||--}o FormalExpression : "selection"
DataService ||--}o Coding : "coding"
Standard ||--}o Coding : "coding"
Dictionary ||--}o Coding : "terms"
Dictionary ||--}o Coding : "coding"
Check ||--}o IdentifiableElement : "appliesTo"
Check ||--}o FormalExpression : "expressions"
Check ||--}o Coding : "coding"
Check ||--}o Comment : "comments"
Check ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
IdentifiableElement ||--}o Coding : "coding"
Query ||--}| IdentifiableElement : "about"
Query ||--}o Coding : "coding"
Query ||--}o Comment : "comments"
Query ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Relationship ||--|| IdentifiableElement : "subject"
Relationship ||--|| IdentifiableElement : "object"
Relationship ||--}o Coding : "coding"
Concept ||--}o ConceptProperty : "properties"
Concept ||--}o Coding : "coding"
Concept ||--}o Comment : "comments"
Concept ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
ConceptProperty ||--|o CodeList : "codeList"
ConceptProperty ||--}o Coding : "coding"
ConceptProperty ||--}o Comment : "comments"
ConceptProperty ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
CodeList ||--}o CodeListItem : "codeListItems"
CodeList ||--|o Resource : "externalCodeList"
CodeList ||--|o Standard : "standard"
CodeList ||--}o Coding : "coding"
CodeList ||--}o Comment : "comments"
CodeList ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
CodeListItem ||--|o Coding : "coding"
Method ||--}o FormalExpression : "expressions"
Method ||--}o DocumentReference : "documents"
Method ||--|o Concept : "implementsConcept"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comments"
Method ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
ApplicabilityCondition ||--}o LogicalPredicate : "predicates"
ApplicabilityCondition ||--}o Coding : "coding"
ApplicabilityCondition ||--}o Comment : "comments"
ApplicabilityCondition ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
LogicalPredicate ||--}o RangeCheck : "rangeChecks"
LogicalPredicate ||--}o FormalExpression : "expressions"
LogicalPredicate ||--}o LogicalPredicate : "predicates"
LogicalPredicate ||--}o Coding : "coding"
LogicalPredicate ||--}o Comment : "comments"
LogicalPredicate ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Item ||--|o CodeList : "codeList"
Item ||--|o Method : "method"
Item ||--}o RangeCheck : "rangeChecks"
Item ||--}o ApplicabilityCondition : "applicableWhen"
Item ||--|o Origin : "origin"
Item ||--|o ConceptProperty : "conceptProperty"
Item ||--}o Coding : "coding"
Item ||--}o Comment : "comments"
Item ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Origin ||--}o SourceItem : "sourceItems"
Origin ||--}o DocumentReference : "documents"
RangeCheck ||--}o FormalExpression : "expressions"
RangeCheck ||--|o Check : "implementsCheck"
ItemGroup ||--}o Item : "items"
ItemGroup ||--}o Item : "uniqueKey"
ItemGroup ||--}o Item : "keySequence"
ItemGroup ||--}o ItemGroup : "slices"
ItemGroup ||--|o Concept : "implementsConcept"
ItemGroup ||--}o ApplicabilityCondition : "applicableWhen"
ItemGroup ||--|o DefClass : "observationClass"
ItemGroup ||--}o Coding : "security"
ItemGroup ||--|o Timing : "validityPeriod"
ItemGroup ||--|o Standard : "standard"
ItemGroup ||--}o Coding : "coding"
ItemGroup ||--}o Comment : "comments"
ItemGroup ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Timing ||--|o Method : "imputation"
Timing ||--}o Coding : "coding"
DefClass ||--}o SubClass : "subClasses"

```




## Inheritance
* [GovernedElement](../classes/GovernedElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md) [Governed](../classes/Governed.md)]
    * **Specification** [ [StudyMetadata](../classes/StudyMetadata.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [itemGroups](../slots/itemGroups.md) | * <br/> [ItemGroup](../classes/ItemGroup.md) | Item groups, containing items, defined in this version of the metadata | direct |
| [items](../slots/items.md) | * <br/> [Item](../classes/Item.md) | Template or top-level items (not belonging to any item group) defined in this version of the metadata | direct |
| [predicates](../slots/predicates.md) | * <br/> [LogicalPredicate](../classes/LogicalPredicate.md) | Reusable logical predicates defined in this specification. | direct |
| [applicabilityConditions](../slots/applicabilityConditions.md) | * <br/> [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | Named applicability conditions defined in this specification. | direct |
| [methods](../slots/methods.md) | * <br/> [Method](../classes/Method.md) | Methods defined in this version of the metadata. | direct |
| [analyses](../slots/analyses.md) | * <br/> [Analysis](../classes/Analysis.md) | Analyses defined in this version of the metadata. | direct |
| [codeLists](../slots/codeLists.md) | * <br/> [CodeList](../classes/CodeList.md) | Code lists defined in this version of the metadata. | direct |
| [codings](../slots/codings.md) | * <br/> [Coding](../classes/Coding.md) | Codings defined in this version of the metadata | direct |
| [concepts](../slots/concepts.md) | * <br/> [Concept](../classes/Concept.md) | Structured Concepts defined in this version of the metadata | direct |
| [relationships](../slots/relationships.md) | * <br/> [Relationship](../classes/Relationship.md) | Relationships between items, item groups, and other elements in this version of the metadata. | direct |
| [queries](../slots/queries.md) | * <br/> [Query](../classes/Query.md) | Queries raised against metadata and/or data elements in this specification. Each Query references its target element(s) by OID, so the same query can relate to many metadata and data elements (many-to-many). | direct |
| [checks](../slots/checks.md) | * <br/> [Check](../classes/Check.md) | Reusable validation checks (e.g. published CORE rules) included in this metadata package. Each Check references the elements it applies to by OID and may cite an external published rule, enabling reuse and loose coupling. | direct |
| [dictionaries](../slots/dictionaries.md) | * <br/> [Dictionary](../classes/Dictionary.md) | Dictionaries defined in this version of the metadata | direct |
| [standards](../slots/standards.md) | * <br/> [Standard](../classes/Standard.md) | Standards defined in this version of the metadata | direct |
| [annotatedCRFs](../slots/annotatedCRFs.md) | * <br/> [DocumentReference](../classes/DocumentReference.md) | Reference to annotated case report forms | direct |
| [resources](../slots/resources.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[DocumentReference](../classes/DocumentReference.md)&nbsp;or&nbsp;<br />[Resource](../classes/Resource.md) | References to resources and documents that describe this version of the metadata. | direct |
| [dataProducts](../slots/dataProducts.md) | * <br/> [DataProduct](../classes/DataProduct.md) | Indexed data flows with clear ownership | direct |
| [displays](../slots/displays.md) | * <br/> [Display](../classes/Display.md) | Displays defined in this version of the metadata. | direct |
| [usdmStudyDesignId](../slots/usdmStudyDesignId.md) | 0..1 <br/> [String](../types/String.md) | OID or URI reference to the USDM StudyDesign that this specification implements. When present, arms, epochs, and scheduled visit slots are resolved from the referenced USDM instance. The USDM study design is the authoritative source for EPOCH, VISITNUM, ARM, and timing anchors; DDS does not redeclare them. | direct |
| [studyOID](../slots/studyOID.md) | 1 <br/> [String](../types/String.md) | Unique identifier for the study | [StudyMetadata](../classes/StudyMetadata.md) |
| [studyName](../slots/studyName.md) | 0..1 <br/> [String](../types/String.md) | Name of the study | [StudyMetadata](../classes/StudyMetadata.md) |
| [studyDescription](../slots/studyDescription.md) | 0..1 <br/> [String](../types/String.md) | Description of the study | [StudyMetadata](../classes/StudyMetadata.md) |
| [protocolName](../slots/protocolName.md) | 0..1 <br/> [String](../types/String.md) | Protocol name for the study | [StudyMetadata](../classes/StudyMetadata.md) |
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
| [GovernedElement](../classes/GovernedElement.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Governed](../classes/Governed.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Specification](../classes/Specification.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Item](../classes/Item.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [ItemGroup](../classes/ItemGroup.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Query](../classes/Query.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [CodeList](../classes/CodeList.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Comment](../classes/Comment.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Concept](../classes/Concept.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [ConceptProperty](../classes/ConceptProperty.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [LogicalPredicate](../classes/LogicalPredicate.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Check](../classes/Check.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Method](../classes/Method.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Dataflow](../classes/Dataflow.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [CubeComponent](../classes/CubeComponent.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Measure](../classes/Measure.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Dimension](../classes/Dimension.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [DataAttribute](../classes/DataAttribute.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [DataProduct](../classes/DataProduct.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Policy](../classes/Policy.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Analysis](../classes/Analysis.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |
| [Display](../classes/Display.md) | [wasDerivedFrom](../slots/wasDerivedFrom.md) | any_of[range] | [Specification](../classes/Specification.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:Specification |
| native | dds:Specification |
| related | fhir:ImplementationGuide, omop:cdm_source |
| close | usdm:StudyDesign |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Specification
description: 'The root specification container: a versioned, governed definition of
  the data model for a study or data product. Links items, item groups, methods, code
  lists, concepts, and study design references. Projects to Define-XML MetaDataVersion,
  FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied
  by the ODM output generator, not here.'
from_schema: https://w3id.org/dds
close_mappings:
- usdm:StudyDesign
related_mappings:
- fhir:ImplementationGuide
- omop:cdm_source
is_a: GovernedElement
mixins:
- StudyMetadata
attributes:
  itemGroups:
    name: itemGroups
    description: Item groups, containing items, defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: ItemGroup
    multivalued: true
    inlined: true
    inlined_as_list: true
  items:
    name: items
    description: Template or top-level items (not belonging to any item group) defined
      in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    - ItemGroup
    - Parameter
    range: Item
    multivalued: true
    inlined: true
    inlined_as_list: true
  predicates:
    name: predicates
    description: Reusable logical predicates defined in this specification.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    - ApplicabilityCondition
    - LogicalPredicate
    range: LogicalPredicate
    multivalued: true
    inlined: true
    inlined_as_list: true
  applicabilityConditions:
    name: applicabilityConditions
    description: Named applicability conditions defined in this specification.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: ApplicabilityCondition
    multivalued: true
    inlined: true
    inlined_as_list: true
  methods:
    name: methods
    description: Methods defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Method
    multivalued: true
    inlined: true
    inlined_as_list: true
  analyses:
    name: analyses
    description: Analyses defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Analysis
    multivalued: true
    inlined: true
    inlined_as_list: true
  codeLists:
    name: codeLists
    description: Code lists defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: CodeList
    multivalued: true
    inlined: true
    inlined_as_list: true
  codings:
    name: codings
    description: Codings defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  concepts:
    name: concepts
    description: Structured Concepts defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Concept
    multivalued: true
  relationships:
    name: relationships
    description: Relationships between items, item groups, and other elements in this
      version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Relationship
    multivalued: true
    inlined: true
    inlined_as_list: true
  queries:
    name: queries
    description: Queries raised against metadata and/or data elements in this specification.
      Each Query references its target element(s) by OID, so the same query can relate
      to many metadata and data elements (many-to-many).
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Query
    multivalued: true
    inlined: true
    inlined_as_list: true
  checks:
    name: checks
    description: Reusable validation checks (e.g. published CORE rules) included in
      this metadata package. Each Check references the elements it applies to by OID
      and may cite an external published rule, enabling reuse and loose coupling.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Check
    multivalued: true
    inlined: true
    inlined_as_list: true
  dictionaries:
    name: dictionaries
    description: Dictionaries defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Dictionary
    multivalued: true
    inlined: true
    inlined_as_list: true
  standards:
    name: standards
    description: Standards defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Standard
    multivalued: true
    inlined: true
    inlined_as_list: true
  annotatedCRFs:
    name: annotatedCRFs
    description: Reference to annotated case report forms
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: DocumentReference
    multivalued: true
    inlined: true
    inlined_as_list: true
  resources:
    name: resources
    description: References to resources and documents that describe this version
      of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: DocumentReference
    - range: Resource
  dataProducts:
    name: dataProducts
    description: Indexed data flows with clear ownership
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: DataProduct
    multivalued: true
    inlined: true
    inlined_as_list: true
  displays:
    name: displays
    description: Displays defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    range: Display
    multivalued: true
    inlined: true
    inlined_as_list: true
  usdmStudyDesignId:
    name: usdmStudyDesignId
    description: OID or URI reference to the USDM StudyDesign that this specification
      implements. When present, arms, epochs, and scheduled visit slots are resolved
      from the referenced USDM instance. The USDM study design is the authoritative
      source for EPOCH, VISITNUM, ARM, and timing anchors; DDS does not redeclare
      them.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Specification
    required: false
tree_root: true

```
</details>

### Induced

<details>
```yaml
name: Specification
description: 'The root specification container: a versioned, governed definition of
  the data model for a study or data product. Links items, item groups, methods, code
  lists, concepts, and study design references. Projects to Define-XML MetaDataVersion,
  FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied
  by the ODM output generator, not here.'
from_schema: https://w3id.org/dds
close_mappings:
- usdm:StudyDesign
related_mappings:
- fhir:ImplementationGuide
- omop:cdm_source
is_a: GovernedElement
mixins:
- StudyMetadata
attributes:
  itemGroups:
    name: itemGroups
    description: Item groups, containing items, defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: itemGroups
    owner: Specification
    domain_of:
    - Specification
    range: ItemGroup
    multivalued: true
    inlined: true
    inlined_as_list: true
  items:
    name: items
    description: Template or top-level items (not belonging to any item group) defined
      in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: items
    owner: Specification
    domain_of:
    - Specification
    - ItemGroup
    - Parameter
    range: Item
    multivalued: true
    inlined: true
    inlined_as_list: true
  predicates:
    name: predicates
    description: Reusable logical predicates defined in this specification.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: predicates
    owner: Specification
    domain_of:
    - Specification
    - ApplicabilityCondition
    - LogicalPredicate
    range: LogicalPredicate
    multivalued: true
    inlined: true
    inlined_as_list: true
  applicabilityConditions:
    name: applicabilityConditions
    description: Named applicability conditions defined in this specification.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: applicabilityConditions
    owner: Specification
    domain_of:
    - Specification
    range: ApplicabilityCondition
    multivalued: true
    inlined: true
    inlined_as_list: true
  methods:
    name: methods
    description: Methods defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: methods
    owner: Specification
    domain_of:
    - Specification
    range: Method
    multivalued: true
    inlined: true
    inlined_as_list: true
  analyses:
    name: analyses
    description: Analyses defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: analyses
    owner: Specification
    domain_of:
    - Specification
    range: Analysis
    multivalued: true
    inlined: true
    inlined_as_list: true
  codeLists:
    name: codeLists
    description: Code lists defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: codeLists
    owner: Specification
    domain_of:
    - Specification
    range: CodeList
    multivalued: true
    inlined: true
    inlined_as_list: true
  codings:
    name: codings
    description: Codings defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: codings
    owner: Specification
    domain_of:
    - Specification
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  concepts:
    name: concepts
    description: Structured Concepts defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: concepts
    owner: Specification
    domain_of:
    - Specification
    range: Concept
    multivalued: true
  relationships:
    name: relationships
    description: Relationships between items, item groups, and other elements in this
      version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: relationships
    owner: Specification
    domain_of:
    - Specification
    range: Relationship
    multivalued: true
    inlined: true
    inlined_as_list: true
  queries:
    name: queries
    description: Queries raised against metadata and/or data elements in this specification.
      Each Query references its target element(s) by OID, so the same query can relate
      to many metadata and data elements (many-to-many).
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: queries
    owner: Specification
    domain_of:
    - Specification
    range: Query
    multivalued: true
    inlined: true
    inlined_as_list: true
  checks:
    name: checks
    description: Reusable validation checks (e.g. published CORE rules) included in
      this metadata package. Each Check references the elements it applies to by OID
      and may cite an external published rule, enabling reuse and loose coupling.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: checks
    owner: Specification
    domain_of:
    - Specification
    range: Check
    multivalued: true
    inlined: true
    inlined_as_list: true
  dictionaries:
    name: dictionaries
    description: Dictionaries defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: dictionaries
    owner: Specification
    domain_of:
    - Specification
    range: Dictionary
    multivalued: true
    inlined: true
    inlined_as_list: true
  standards:
    name: standards
    description: Standards defined in this version of the metadata
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: standards
    owner: Specification
    domain_of:
    - Specification
    range: Standard
    multivalued: true
    inlined: true
    inlined_as_list: true
  annotatedCRFs:
    name: annotatedCRFs
    description: Reference to annotated case report forms
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: annotatedCRFs
    owner: Specification
    domain_of:
    - Specification
    range: DocumentReference
    multivalued: true
    inlined: true
    inlined_as_list: true
  resources:
    name: resources
    description: References to resources and documents that describe this version
      of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: resources
    owner: Specification
    domain_of:
    - Specification
    range: string
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: DocumentReference
    - range: Resource
  dataProducts:
    name: dataProducts
    description: Indexed data flows with clear ownership
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: dataProducts
    owner: Specification
    domain_of:
    - Specification
    range: DataProduct
    multivalued: true
    inlined: true
    inlined_as_list: true
  displays:
    name: displays
    description: Displays defined in this version of the metadata.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: displays
    owner: Specification
    domain_of:
    - Specification
    range: Display
    multivalued: true
    inlined: true
    inlined_as_list: true
  usdmStudyDesignId:
    name: usdmStudyDesignId
    description: OID or URI reference to the USDM StudyDesign that this specification
      implements. When present, arms, epochs, and scheduled visit slots are resolved
      from the referenced USDM instance. The USDM study design is the authoritative
      source for EPOCH, VISITNUM, ARM, and timing anchors; DDS does not redeclare
      them.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: usdmStudyDesignId
    owner: Specification
    domain_of:
    - Specification
    range: string
    required: false
  studyOID:
    name: studyOID
    description: Unique identifier for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyOID
    owner: Specification
    domain_of:
    - StudyMetadata
    range: string
    required: true
  studyName:
    name: studyName
    description: Name of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyName
    owner: Specification
    domain_of:
    - StudyMetadata
    range: string
  studyDescription:
    name: studyDescription
    description: Description of the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: studyDescription
    owner: Specification
    domain_of:
    - StudyMetadata
    range: string
  protocolName:
    name: protocolName
    description: Protocol name for the study
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: protocolName
    owner: Specification
    domain_of:
    - StudyMetadata
    range: string
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://w3id.org/dds
    rank: 1000
    identifier: true
    alias: OID
    owner: Specification
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
    owner: Specification
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: name
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
    owner: Specification
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
tree_root: true

```
</details>