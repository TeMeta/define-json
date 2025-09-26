# Define-JSON

Data model for supply and demand data contracts to complement CDISC USDM, ODM, and Dataset-JSON. This LinkML version includes semantics to act as Rosetta Stone for SDMX, FHIR, OMOP, RDF, and CDISC.

URI: https://cdisc.org/define-json

Name: Define-JSON



## Schema Diagram

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
    AliasPredicate aliasType  
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
Dictionary {
    string publishedBy  
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
ReturnValue {
    DataType dataType  
    stringList valueList  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Parameter {
    DataType dataType  
    string value  
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
RangeCheck {
    Comparator comparator  
    stringList checkValues  
    string item  
    SoftHard softHard  
}
Origin {
    OriginType type  
    OriginSource source  
}
SourceItem {
    stringList resource  
}
WhereClause {
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
NominalOccurrence {
    string event  
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

MetaDataVersion ||--}o ItemGroup : "itemGroups"
MetaDataVersion ||--}o Item : "items"
MetaDataVersion ||--}o Condition : "conditions"
MetaDataVersion ||--}o WhereClause : "whereClauses"
MetaDataVersion ||--}o Method : "methods"
MetaDataVersion ||--}o CodeList : "codeLists"
MetaDataVersion ||--}o Coding : "codings"
MetaDataVersion ||--}o ReifiedConcept : "concepts"
MetaDataVersion ||--}o Relationship : "relationships"
MetaDataVersion ||--}o Dictionary : "dictionaries"
MetaDataVersion ||--}o Coding : "coding"
MetaDataVersion ||--}o Comment : "comment"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
DocumentReference ||--}o Coding : "coding"
Dictionary ||--}o Coding : "terms"
Dictionary ||--}o Coding : "coding"
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
CodeList ||--|o Resource : "externalCodeList"
CodeList ||--}o Coding : "coding"
CodeList ||--}o Comment : "comment"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
ReturnValue ||--}o Coding : "coding"
Parameter ||--}o CodeList : "codeList"
Parameter ||--}o Item : "items"
Parameter ||--}o ConceptProperty : "conceptProperty"
Parameter ||--}o Coding : "coding"
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
Condition ||--}o RangeCheck : "rangeChecks"
Condition ||--}o FormalExpression : "formalExpression"
Condition ||--}o Coding : "coding"
Condition ||--}o Comment : "comment"
RangeCheck ||--}o FormalExpression : "formalExpression"
Origin ||--}o SourceItem : "sourceItems"
Origin ||--|o DocumentReference : "document"
SourceItem ||--|o Item : "item"
SourceItem ||--|o DocumentReference : "document"
SourceItem ||--}o Coding : "coding"
WhereClause ||--}o Condition : "conditions"
WhereClause ||--}o Coding : "coding"
Method ||--}o FormalExpression : "formalExpressions"
Method ||--|o DocumentReference : "document"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comment"
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
NominalOccurrence ||--|| Timing : "timing"
NominalOccurrence ||--}o Condition : "condition"
NominalOccurrence ||--}o Coding : "coding"
NominalOccurrence ||--}o Comment : "comment"

```


## Classes

| Class | Description |
| --- | --- |
| [CodeListItem](classes/CodeListItem.md) | A structured member of a CodeList that extends the Coding class with addition... |
| [Coding](classes/Coding.md) | A semantic reference that provides standardized codes and their meanings from... |
| [DataflowRelationship](classes/DataflowRelationship.md) | A relationship element that associates a DataAttribute with a Dataflow, repor... |
| [DatasetKey](classes/DatasetKey.md) | An abstract identifier that comprises the cross-product of dimension values t... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GroupKey](classes/GroupKey.md) | A dimension subset that represents collections of dimensions that are subsets... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SeriesKey](classes/SeriesKey.md) | A unique identifier that comprises the cross-product of dimension values incl... |
| [DimensionRelationship](classes/DimensionRelationship.md) | A relationship element that associates a DataAttribute with a specific Dimens... |
| [Distribution](classes/Distribution.md) | A technical representation that provides a specific format or access method f... |
| [Formatted](classes/Formatted.md) | A mixin that provides slots for reporting, exchange, or storage formatting |
| [Governed](classes/Governed.md) | A mixin that provides slots for audit trail and standards governance, includi... |
| [GovernedElement](classes/GovernedElement.md) |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CodeList](classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an i... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ConceptProperty](classes/ConceptProperty.md) | A reified property concept that exists within the context of its containing t... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Condition](classes/Condition.md) | A reusable logical construct that combines multiple components using AND logi... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[CubeComponent](classes/CubeComponent.md) | An abstract data field that represents a component in a data structure defini... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataAttribute](classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata ab... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dimension](classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Measure](classes/Measure.md) | A data cube property that describes a measurable quantity or value |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dataflow](classes/Dataflow.md) | An abstract representation that defines data provision for different referenc... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataProduct](classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets a... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Item](classes/Item.md) | A data element that represents a specific piece of information within a defin... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ItemGroup](classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataStructureDefinition](classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysi... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MetaDataVersion](classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Method](classes/Method.md) | A reusable computational procedure that describes how to derive values and ca... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[NominalOccurrence](classes/NominalOccurrence.md) | An event element that represents occurrences such as planned or unplanned enc... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ProvisionAgreement](classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ReifiedConcept](classes/ReifiedConcept.md) | A canonical information layer that makes abstract concepts explicit and refer... |
| [GroupRelationship](classes/GroupRelationship.md) | A relationship element that associates a DataAttribute with a set of Dimensio... |
| [Identifiable](classes/Identifiable.md) | A mixin that provides slots for making an entity addressable within a study o... |
| [IdentifiableElement](classes/IdentifiableElement.md) |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Comment](classes/Comment.md) | A descriptive element that contains explanatory text provided by a data or me... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ComponentList](classes/ComponentList.md) | An abstract definition that specifies a list of components within a data stru... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dataset](classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dictionary](classes/Dictionary.md) | A dictionary that defines a set of codes and their meanings |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DocumentReference](classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combin... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FormalExpression](classes/FormalExpression.md) | A computational element that defines the execution of a data derivation withi... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Organization](classes/Organization.md) | An entity that represents organizational information, such as a site or spons... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataProvider](classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Parameter](classes/Parameter.md) | A variable element that describes an input used in a formal expression |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Relationship](classes/Relationship.md) | A semantic link that defines connections between elements such as Items or It... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Resource](classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DataService](classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ReturnValue](classes/ReturnValue.md) | An output specification that defines the details of what a formal expression ... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[SiteOrSponsorComment](classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct fr... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Timing](classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[User](classes/User.md) | An entity that represents information about a specific user of a clinical dat... |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[WhereClause](classes/WhereClause.md) | A conditional element that describes the circumstances under which a containi... |
| [IsODMItem](classes/IsODMItem.md) | A mixin that provides additional attributes for CDISC Operational Data Model ... |
| [IsProfile](classes/IsProfile.md) | A mixin that provides additional metadata for FHIR resources and Data Product... |
| [IsSdmxDataset](classes/IsSdmxDataset.md) | A mixin that provides additional metadata specific to SDMX Datasets |
| [Labelled](classes/Labelled.md) | A mixin that provides slots for detailing meanings and multilingual descripti... |
| [MeasureRelationship](classes/MeasureRelationship.md) | A relationship element that associates a DataAttribute with a Measure |
| [ObservationRelationship](classes/ObservationRelationship.md) | A relationship element that associates a DataAttribute with an Observation, a... |
| [Origin](classes/Origin.md) | A provenance element that describes the source of data for an item |
| [RangeCheck](classes/RangeCheck.md) | A validation element that performs a simple comparison check between a refere... |
| [SourceItem](classes/SourceItem.md) | A data source that provides the origin of information for an item |
| [TranslatedText](classes/TranslatedText.md) |  |
| [Translation](classes/Translation.md) | A text representation that provides content in a specific language, used for ... |
| [Versioned](classes/Versioned.md) | A mixin that provides version and connectivity information, including version... |



## Slots

| Slot | Description |
| --- | --- |
| [OID](slots/OID.md) | Local identifier within this study/context |
| [uuid](slots/uuid.md) | Universal unique identifier |
| [mandatory](slots/mandatory.md) | Is this element required? |
| [comment](slots/comment.md) | Comment on the element, such as a rationale for its inclusion or exclusion |
| [purpose](slots/purpose.md) | Purpose or rationale for this data element |
| [lastUpdated](slots/lastUpdated.md) | When the resource was last updated |
| [owner](slots/owner.md) | Party responsible for this element |
| [wasDerivedFrom](slots/wasDerivedFrom.md) | Reference to another item that this item implements or extends, e |
| [name](slots/name.md) | Short name or identifier, used for field names |
| [description](slots/description.md) | Detailed description, shown in tooltips |
| [coding](slots/coding.md) | Semantic tags for this element |
| [label](slots/label.md) | Human-readable label, shown in UIs |
| [aliases](slots/aliases.md) | Alternative name or identifier |
| [decimalDigits](slots/decimalDigits.md) | For decimal values, the number of digits after the decimal point |
| [displayFormat](slots/displayFormat.md) | A display format for the item |
| [significantDigits](slots/significantDigits.md) | For numeric values, the number of significant digits |
| [version](slots/version.md) | The version of the external resources |
| [href](slots/href.md) | Machine-readable instructions to obtain the resource e |
| [profile](slots/profile.md) | Profiles this resource claims to conform to |
| [security](slots/security.md) | Security tags applied to this resource |
| [authenticator](slots/authenticator.md) | Who/what authenticated the resource |
| [validityPeriod](slots/validityPeriod.md) | Time period during which the resouce is valid |
| [role](slots/role.md) | Identifies the role of the item within the containing context, taken from the... |
| [roleCodeList](slots/roleCodeList.md) | Reference to the CodeList that defines the roles for this item |
| [hasNoData](slots/hasNoData.md) | Set to Yes if this is a manifest and there is no data for this item |
| [crfCompletionInstructions](slots/crfCompletionInstructions.md) | CRFCompletionInstructions reference: Instructions for the clinical site on ho... |
| [cdiscNotes](slots/cdiscNotes.md) | CDISCNotes reference: Explanatory text for the variable |
| [implementationNotes](slots/implementationNotes.md) | ImplementationNotes reference: Further information, such as rationale and imp... |
| [collectionExceptionCondition](slots/collectionExceptionCondition.md) | Condition that defines when collection may be exempted |
| [preSpecifiedValue](slots/preSpecifiedValue.md) | Prefill value or a default value for a field that is automatically populated |
| [itemGroups](slots/itemGroups.md) | Item groups, containing items, defined in this version of the metadata |
| [items](slots/items.md) | Template or top-level items (not belonging to any item group) defined in this... |
| [resources](slots/resources.md) | References to documents that describe this version of the metadata |
| [conditions](slots/conditions.md) | Logical conditions that apply to this version of the metadata |
| [whereClauses](slots/whereClauses.md) | Data contexts that apply to this version of the metadata |
| [methods](slots/methods.md) | Methods defined in this version of the metadata |
| [codeLists](slots/codeLists.md) | Code lists defined in this version of the metadata |
| [codings](slots/codings.md) | Codings defined in this version of the metadata |
| [concepts](slots/concepts.md) | Structured Concepts defined in this version of the metadata |
| [relationships](slots/relationships.md) | Relationships between items, item groups, and other elements in this version ... |
| [dictionaries](slots/dictionaries.md) | Dictionaries defined in this version of the metadata |
| [dataType](slots/dataType.md) | The data type of the item |
| [length](slots/length.md) | The maximum length of the data item in characters |
| [codeList](slots/codeList.md) | Reference to the CodeList that constrains the item values |
| [method](slots/method.md) | Reference to the Method element that describes how to derive this item's valu... |
| [rangeChecks](slots/rangeChecks.md) | Range checks applied to this item (e |
| [whereClause](slots/whereClause.md) | Conditions for when this item definition applies |
| [origin](slots/origin.md) | The origin of the data |
| [conceptProperty](slots/conceptProperty.md) | Reference to a abstract concept property that this item is a specialization /... |
| [domain](slots/domain.md) | Domain abbreviation for the dataset |
| [structure](slots/structure.md) | Data structure of the item group, indicating how the records are organized |
| [isReferenceData](slots/isReferenceData.md) | Set to Yes if this is a reference item group |
| [type](slots/type.md) | Type of item group |
| [children](slots/children.md) | Child item groups within this item group |
| [implementsConcept](slots/implementsConcept.md) | Reference to a abstract concept topic that this item group is a specializatio... |
| [subject](slots/subject.md) | The starting element of the relationship (e |
| [object](slots/object.md) | The ending element of the relationship |
| [predicateTerm](slots/predicateTerm.md) | Short variable relationship linking phrase for programming purposes |
| [linkingPhrase](slots/linkingPhrase.md) | Variable relationship descriptive linking phrase |
| [language](slots/language.md) | The language of the translation |
| [value](slots/value.md) | The translated text |
| [translations](slots/translations.md) |  |
| [formatName](slots/formatName.md) | Name of a standard format definition |
| [codeListItems](slots/codeListItems.md) | The individual values that make up this CodeList |
| [externalCodeList](slots/externalCodeList.md) | Reference to a code list that is defined externally to this study |
| [codedValue](slots/codedValue.md) | The value of the CodeListItem before decoding |
| [decode](slots/decode.md) | The decoded value of the CodeListItem |
| [weight](slots/weight.md) | Numeric significance of the code (e |
| [other](slots/other.md) | Flag to indicate that the term represents "other" content |
| [text](slots/text.md) | The comment text |
| [documents](slots/documents.md) | References to documents that contain or are referenced by this comment |
| [code](slots/code.md) | The code value |
| [codeSystem](slots/codeSystem.md) | The code system identifier |
| [codeSystemVersion](slots/codeSystemVersion.md) | The code system version |
| [aliasType](slots/aliasType.md) | How this coding is related in the context of its parent element |
| [terms](slots/terms.md) | Terms in this dictionary - leave this empty in most cases to keep the file sm... |
| [publishedBy](slots/publishedBy.md) | Associates the Data Provider that reports/publishes the data |
| [properties](slots/properties.md) | Properties of the reified object, which can be other governed elements or sim... |
| [minOccurs](slots/minOccurs.md) | Minimum number of occurrences of this property in the context |
| [maxOccurs](slots/maxOccurs.md) | Maximum number of occurrences of this property in the context |
| [implementsCondition](slots/implementsCondition.md) | Reference to a external (e |
| [formalExpression](slots/formalExpression.md) | A formal expression for complex checks |
| [comparator](slots/comparator.md) | The type of comparison to be performed |
| [checkValues](slots/checkValues.md) | Values to compare against |
| [item](slots/item.md) | Reference to the Item element whose value is being checked |
| [softHard](slots/softHard.md) | Indicates whether a validation check is an error ("Hard") or a warning ("Soft... |
| [context](slots/context.md) | The specific context within the containing element to which this formal expre... |
| [expression](slots/expression.md) | The actual text of the formal expression (renamed from 'code' for disambiguat... |
| [returnType](slots/returnType.md) | Return type of the expression |
| [parameters](slots/parameters.md) | Parameters used in the expression |
| [returnValue](slots/returnValue.md) | Return value details |
| [externalCodeLibs](slots/externalCodeLibs.md) | External code libraries referenced |
| [formalExpressions](slots/formalExpressions.md) | Formal expressions used by this method |
| [document](slots/document.md) | Reference to a document that describes this method in detail |
| [resource](slots/resource.md) | Path to a resource (e |
| [valueList](slots/valueList.md) | A list of possible return values |
| [source](slots/source.md) | The source of the data, such as Investigator, Sponsor, Subject, or Vendor |
| [sourceItems](slots/sourceItems.md) | Source items for this origin |
| [sourceType](slots/sourceType.md) | who made the comment, such as Investigator, Sponsor |
| [userType](slots/userType.md) | User's role in the study |
| [userName](slots/userName.md) | The username of the user |
| [fullName](slots/fullName.md) | The full name of the user |
| [organization](slots/organization.md) | The organization the user belongs to |
| [location](slots/location.md) | The physical location of the organization |
| [address](slots/address.md) | The address of the organization |
| [partOfOrganization](slots/partOfOrganization.md) | Reference to a parent organization if this organization is part of a larger e... |
| [resourceType](slots/resourceType.md) | Type of resource (e |
| [attribute](slots/attribute.md) | Field provided by the Name attribute where the data or information can be obt... |
| [selection](slots/selection.md) | Machine-executable instructions for selecting data from the resource |
| [title](slots/title.md) | Document title |
| [pages](slots/pages.md) | Reference to specific pages in a PDF document |
| [relationship](slots/relationship.md) | Relationship to the referencing entity |
| [isNominal](slots/isNominal.md) | Indicates whether the timing is nominal (event-based) or not |
| [relativeTo](slots/relativeTo.md) | Reference to the event or occurrence that this timing is relative to |
| [relativeFrom](slots/relativeFrom.md) | Reference to the event or occurrence that this timing is relative to |
| [windowLower](slots/windowLower.md) | Start date/time of the timing |
| [windowUpper](slots/windowUpper.md) | End date/time of the timing |
| [recalled](slots/recalled.md) | Indicates whether the timing is recalled or not (recalled timings are less re... |
| [frequency](slots/frequency.md) | Frequency |
| [imputation](slots/imputation.md) | The imputation method used for the Timing |
| [timing](slots/timing.md) | A named event reference, that can nest further named timing references |
| [event](slots/event.md) | The ID of the event in a Schedule |
| [condition](slots/condition.md) | A condition that must be met for this occurrence to be valid |
| [dimensions](slots/dimensions.md) |  |
| [measures](slots/measures.md) |  |
| [attributes](slots/attributes.md) |  |
| [grouping](slots/grouping.md) | An association to a set of metadata concepts that have an identified structur... |
| [evolvingStructure](slots/evolvingStructure.md) |  |
| [dimensionConstraint](slots/dimensionConstraint.md) |  |
| [action](slots/action.md) | Defines the action to be taken by the recipient system (information, append, ... |
| [reportingBegin](slots/reportingBegin.md) | A specific time period in a known system of time periods that identifies the ... |
| [reportingEnd](slots/reportingEnd.md) | A specific time period in a known system of time periods that identifies the ... |
| [dataExtractionDate](slots/dataExtractionDate.md) | A specific time period that identifies the date and time that the data are ex... |
| [validFrom](slots/validFrom.md) | Indicates the inclusive start time indicating the validity of the information... |
| [validTo](slots/validTo.md) | Indicates the inclusive end time indicating the validity of the information i... |
| [publicationYear](slots/publicationYear.md) | Specifies the year of publication of the data or metadata in terms of whateve... |
| [publicationPeriod](slots/publicationPeriod.md) | Specifies the period of publication of the data or metadata in terms of whate... |
| [describedBy](slots/describedBy.md) | Associates a Dataflow and thereby a Data Structure Definition to the data set |
| [structuredBy](slots/structuredBy.md) | Associates the Data Structure Definition that defines the structure of the Da... |
| [keys](slots/keys.md) | Series and Group keys in the data that are associated with dimensions in this... |
| [datasetType](slots/datasetType.md) | Type or classification of the dataset |
| [distribution](slots/distribution.md) | Representations of this dataset in various formats or access methods |
| [conformsTo](slots/conformsTo.md) | Specification or standard that this dataset conforms to |
| [hasPolicy](slots/hasPolicy.md) | Access or usage policy applied to this dataset |
| [informationSensitivityClassification](slots/informationSensitivityClassification.md) | Classification of the dataset's sensitivity or confidentiality |
| [keyValues](slots/keyValues.md) | List of Key Values that comprise each key, separated by a dot e |
| [attributeValues](slots/attributeValues.md) | Association to the Attribute Values relating to Key |
| [missingHandling](slots/missingHandling.md) | The method for handling missing values in the measure property |
| [keySequence](slots/keySequence.md) |  |
| [components](slots/components.md) | The components that make up this component list |
| [measure](slots/measure.md) |  |
| [dataFlow](slots/dataFlow.md) |  |
| [groupKey](slots/groupKey.md) | Set of dimensions that this definition depends on |
| [dataProductOwner](slots/dataProductOwner.md) | The person or team accountable for this data product |
| [lifecycleStatus](slots/lifecycleStatus.md) | Current lifecycle status of the data product |
| [inputPort](slots/inputPort.md) | Services that provide input into this data product |
| [outputPort](slots/outputPort.md) | Services that expose output from this data product |
| [inputDataset](slots/inputDataset.md) | Source datasets used by the data product |
| [outputDataset](slots/outputDataset.md) | Output datasets produced by the data product |
| [accessService](slots/accessService.md) | Service that provides access to this distribution |
| [isDistributionOf](slots/isDistributionOf.md) | Dataset this distribution represents |
| [format](slots/format.md) | File format or serialization used in the distribution |
| [isAccessServiceOf](slots/isAccessServiceOf.md) | Distribution(s) for which this service provides access |
| [protocol](slots/protocol.md) | Protocol used by the service (e |
| [securitySchemaType](slots/securitySchemaType.md) | Security or authentication method used (e |
| [providesDataFor](slots/providesDataFor.md) | The Dataflows that this provider supplies data for |
| [provisionAgreements](slots/provisionAgreements.md) | The ProvisionAgreements that this provider has with Data Consumers |
| [provider](slots/provider.md) | The Data Provider that is part of this agreement |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [AliasPredicate](enums/AliasPredicate.md) | An enumeration that defines permissible values for the relationship between a... |
| [Comparator](enums/Comparator.md) | An enumeration that defines the types of comparison operations available for ... |
| [UserType](enums/UserType.md) | An enumeration that defines the types of users in a clinical data collection ... |
| [OrganizationType](enums/OrganizationType.md) | An enumeration that defines the types of organizations involved in clinical r... |
| [SoftHard](enums/SoftHard.md) | An enumeration that indicates whether a validation check should be treated as... |
| [MethodType](enums/MethodType.md) | An enumeration that defines the types of computational methods available for ... |
| [DataType](enums/DataType.md) | An enumeration that defines the fundamental data types available for items |
| [OriginType](enums/OriginType.md) | An enumeration that defines the types of origins for data items |
| [OriginSource](enums/OriginSource.md) | An enumeration that defines the sources of data origin |
| [ItemGroupType](enums/ItemGroupType.md) | An enumeration that defines the roles of an item group within a specific cont... |
| [TimingType](enums/TimingType.md) | An enumeration that defines CDISC timing type values indicating the temporal ... |
| [LinkingPhraseEnum](enums/LinkingPhraseEnum.md) | An enumeration that defines variable relationship descriptive linking phrases... |
| [PredicateTermEnum](enums/PredicateTermEnum.md) | An enumeration that defines short variable relationship linking phrases for p... |
| [DataProductLifecycleStatus](enums/DataProductLifecycleStatus.md) | An enumeration that defines the lifecycle stages for a DataProduct |


## Types

| Type | Description |
| --- | --- |
| [String](types/String.md) | A character string |
| [Integer](types/Integer.md) | An integer |
| [Boolean](types/Boolean.md) | A binary (true or false) value |
| [Float](types/Float.md) | A real number that conforms to the xsd:float specification |
| [Double](types/Double.md) | A real number that conforms to the xsd:double specification |
| [Decimal](types/Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Time](types/Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Date](types/Date.md) | a date (year, month and day) in an idealized calendar |
| [Datetime](types/Datetime.md) | The combination of a date and time |
| [DateOrDatetime](types/DateOrDatetime.md) | Either a date or a datetime |
| [Uriorcurie](types/Uriorcurie.md) | a URI or a CURIE |
| [Curie](types/Curie.md) | a compact URI |
| [Uri](types/Uri.md) | a complete URI |
| [Ncname](types/Ncname.md) | Prefix part of CURIE |
| [Objectidentifier](types/Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Nodeidentifier](types/Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Jsonpointer](types/Jsonpointer.md) | A string encoding a JSON Pointer |
| [Jsonpath](types/Jsonpath.md) | A string encoding a JSON Path |
| [Sparqlpath](types/Sparqlpath.md) | A string encoding a SPARQL Property Path |


## Subsets

| Subset | Description |
| --- | --- |
