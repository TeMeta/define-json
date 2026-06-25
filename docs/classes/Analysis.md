

# Class: Analysis 


_Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used._

_Expressions and parameters from Method can be generic or implementation-specific._





URI: [dds:class/Analysis](https://w3id.org/dds/class/Analysis)


```mermaid
erDiagram
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
    string defaultValue  
    stringList items  
    boolean required  
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
Dimension {
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

Analysis ||--|o Method : "analysisMethod"
Analysis ||--}o ApplicabilityCondition : "applicableWhen"
Analysis ||--}o Dataflow : "inputDataflows"
Analysis ||--}o FormalExpression : "expressions"
Analysis ||--}o DocumentReference : "documents"
Analysis ||--|o Concept : "implementsConcept"
Analysis ||--}o Coding : "coding"
Analysis ||--}o Comment : "comments"
Analysis ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Concept ||--}o ConceptProperty : "properties"
Concept ||--}o Coding : "coding"
Concept ||--}o Comment : "comments"
Concept ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
ConceptProperty ||--|o CodeList : "codeList"
ConceptProperty ||--}o Coding : "coding"
ConceptProperty ||--}o Comment : "comments"
ConceptProperty ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
DocumentReference ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
ReturnValue ||--}o Coding : "coding"
Parameter ||--}o CodeList : "codeList"
Parameter ||--}o ConceptProperty : "conceptProperty"
Parameter ||--}o ApplicabilityCondition : "applicableWhen"
Parameter ||--}o LogicalPredicate : "validationPredicates"
Parameter ||--}o Coding : "coding"
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
DataStructureDefinition ||--}o Item : "uniqueKey"
DataStructureDefinition ||--}o Item : "keySequence"
DataStructureDefinition ||--}o ItemGroup : "slices"
DataStructureDefinition ||--|o Concept : "implementsConcept"
DataStructureDefinition ||--}o ApplicabilityCondition : "applicableWhen"
DataStructureDefinition ||--|o DefClass : "observationClass"
DataStructureDefinition ||--}o Coding : "security"
DataStructureDefinition ||--|o Timing : "validityPeriod"
DataStructureDefinition ||--|o Standard : "standard"
DataStructureDefinition ||--}o Coding : "coding"
DataStructureDefinition ||--}o Comment : "comments"
DataStructureDefinition ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
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
Method ||--}o FormalExpression : "expressions"
Method ||--}o DocumentReference : "documents"
Method ||--|o Concept : "implementsConcept"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comments"
Method ||--}o SiteOrSponsorComment : "siteOrSponsorComments"

```




## Inheritance
* [GovernedElement](../classes/GovernedElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md) [Governed](../classes/Governed.md)]
    * [Method](../classes/Method.md)
        * **Analysis** [ [Versioned](../classes/Versioned.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [analysisReason](../slots/analysisReason.md) | 0..1 <br/> [String](../types/String.md) | The reason this analysis was performed. | direct |
| [analysisPurpose](../slots/analysisPurpose.md) | 0..1 <br/> [String](../types/String.md) | The purpose or role of this analysis in the study. | direct |
| [analysisMethod](../slots/analysisMethod.md) | 0..1 <br/> [Method](../classes/Method.md) | Generic method used to perform this analysis. | direct |
| [applicableWhen](../slots/applicableWhen.md) | * <br/> [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | The conditions (e.g. population, time period etc.) that must be met for this analysis to be applicable. | direct |
| [inputData](../slots/inputData.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[Dataset](../classes/Dataset.md) | Datasets or slices/subsets of datasets asked for by this analysis. If a Item is referenced by a Parameter e.g. Analysis Variable, make sure to include its parent ItemGroup here. | direct |
| [inputDataflows](../slots/inputDataflows.md) | * <br/> [Dataflow](../classes/Dataflow.md) | Dataflows that supply input data for this analysis. Replaces Dataflow.analysisMethod (which had the dependency backwards — a data contract should not know which analyses consume it). | direct |
| [version](../slots/version.md) | 0..1 <br/> [String](../types/String.md) | The version of the external resources | [Versioned](../classes/Versioned.md) |
| [href](../slots/href.md) | 0..1 <br/> [String](../types/String.md) | Machine-readable instructions to obtain the resource e.g. FHIR path, URL | [Versioned](../classes/Versioned.md) |
| [type](../slots/type.md) | 0..1 <br/> [MethodType](../enums/MethodType.md) | The type of method e.g. Computation, Imputation, Transformation. | [Method](../classes/Method.md) |
| [expressions](../slots/expressions.md) | * <br/> [FormalExpression](../classes/FormalExpression.md) | Formal expressions used by this method | [Method](../classes/Method.md) |
| [documents](../slots/documents.md) | * <br/> [DocumentReference](../classes/DocumentReference.md) | Reference to a document that describes this method in detail. | [Method](../classes/Method.md) |
| [implementsConcept](../slots/implementsConcept.md) | 0..1 <br/> [Concept](../classes/Concept.md) | Reference to a specific concept that this Method implements. | [Method](../classes/Method.md) |
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
| [Specification](../classes/Specification.md) | [analyses](../slots/analyses.md) | range | [Analysis](../classes/Analysis.md) |
| [Display](../classes/Display.md) | [analysis](../slots/analysis.md) | range | [Analysis](../classes/Analysis.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:Analysis |
| native | dds:Analysis |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Analysis
description: 'Analysis extends Method to capture analysis-specific metadata including
  the reason for analysis, its purpose, and data traceability for the results used.

  Expressions and parameters from Method can be generic or implementation-specific.'
from_schema: https://w3id.org/dds
is_a: Method
mixins:
- Versioned
attributes:
  analysisReason:
    name: analysisReason
    description: 'The reason this analysis was performed.  '
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Analysis
  analysisPurpose:
    name: analysisPurpose
    description: The purpose or role of this analysis in the study.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Analysis
  analysisMethod:
    name: analysisMethod
    description: Generic method used to perform this analysis.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Analysis
    range: Method
  applicableWhen:
    name: applicableWhen
    description: The conditions (e.g. population, time period etc.) that must be met
      for this analysis to be applicable.
    from_schema: https://w3id.org/dds
    domain_of:
    - Item
    - ItemGroup
    - Parameter
    - Analysis
    range: ApplicabilityCondition
    multivalued: true
    inlined: false
  inputData:
    name: inputData
    description: Datasets or slices/subsets of datasets asked for by this analysis.
      If a Item is referenced by a Parameter e.g. Analysis Variable, make sure to
      include its parent ItemGroup here.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Analysis
    multivalued: true
    inlined: false
    any_of:
    - range: ItemGroup
    - range: Dataset
  inputDataflows:
    name: inputDataflows
    description: Dataflows that supply input data for this analysis. Replaces Dataflow.analysisMethod
      (which had the dependency backwards — a data contract should not know which
      analyses consume it).
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Analysis
    range: Dataflow
    multivalued: true
    inlined: false

```
</details>

### Induced

<details>
```yaml
name: Analysis
description: 'Analysis extends Method to capture analysis-specific metadata including
  the reason for analysis, its purpose, and data traceability for the results used.

  Expressions and parameters from Method can be generic or implementation-specific.'
from_schema: https://w3id.org/dds
is_a: Method
mixins:
- Versioned
attributes:
  analysisReason:
    name: analysisReason
    description: 'The reason this analysis was performed.  '
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: analysisReason
    owner: Analysis
    domain_of:
    - Analysis
    range: string
  analysisPurpose:
    name: analysisPurpose
    description: The purpose or role of this analysis in the study.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: analysisPurpose
    owner: Analysis
    domain_of:
    - Analysis
    range: string
  analysisMethod:
    name: analysisMethod
    description: Generic method used to perform this analysis.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: analysisMethod
    owner: Analysis
    domain_of:
    - Analysis
    range: Method
  applicableWhen:
    name: applicableWhen
    description: The conditions (e.g. population, time period etc.) that must be met
      for this analysis to be applicable.
    from_schema: https://w3id.org/dds
    alias: applicableWhen
    owner: Analysis
    domain_of:
    - Item
    - ItemGroup
    - Parameter
    - Analysis
    range: ApplicabilityCondition
    multivalued: true
    inlined: false
  inputData:
    name: inputData
    description: Datasets or slices/subsets of datasets asked for by this analysis.
      If a Item is referenced by a Parameter e.g. Analysis Variable, make sure to
      include its parent ItemGroup here.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: inputData
    owner: Analysis
    domain_of:
    - Analysis
    range: string
    multivalued: true
    inlined: false
    any_of:
    - range: ItemGroup
    - range: Dataset
  inputDataflows:
    name: inputDataflows
    description: Dataflows that supply input data for this analysis. Replaces Dataflow.analysisMethod
      (which had the dependency backwards — a data contract should not know which
      analyses consume it).
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: inputDataflows
    owner: Analysis
    domain_of:
    - Analysis
    range: Dataflow
    multivalued: true
    inlined: false
  version:
    name: version
    description: The version of the external resources
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: version
    owner: Analysis
    domain_of:
    - Versioned
    - Standard
    range: string
  href:
    name: href
    description: Machine-readable instructions to obtain the resource e.g. FHIR path,
      URL
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: href
    owner: Analysis
    domain_of:
    - Versioned
    range: string
    required: false
  type:
    name: type
    description: The type of method e.g. Computation, Imputation, Transformation.
    from_schema: https://w3id.org/dds
    alias: type
    owner: Analysis
    domain_of:
    - ItemGroup
    - Method
    - Origin
    - Organization
    - Standard
    - Timing
    range: MethodType
  expressions:
    name: expressions
    description: Formal expressions used by this method
    from_schema: https://w3id.org/dds
    alias: expressions
    owner: Analysis
    domain_of:
    - LogicalPredicate
    - RangeCheck
    - Check
    - Method
    range: FormalExpression
    multivalued: true
    inlined: true
    inlined_as_list: true
  documents:
    name: documents
    description: Reference to a document that describes this method in detail.
    from_schema: https://w3id.org/dds
    alias: documents
    owner: Analysis
    domain_of:
    - Comment
    - Method
    - Origin
    range: DocumentReference
    multivalued: true
    inlined: true
    inlined_as_list: true
  implementsConcept:
    name: implementsConcept
    description: Reference to a specific concept that this Method implements.
    from_schema: https://w3id.org/dds
    alias: implementsConcept
    owner: Analysis
    domain_of:
    - ItemGroup
    - Method
    range: Concept
    inlined: false
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://w3id.org/dds
    rank: 1000
    identifier: true
    alias: OID
    owner: Analysis
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
    owner: Analysis
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: name
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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
    owner: Analysis
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