

# Class: Parameter 


_A variable element that describes an input used in a formal expression_





URI: [dds:class/Parameter](https://w3id.org/dds/class/Parameter)


```mermaid
erDiagram
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
    AliasPredicate aliasType  
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
    LogicalOperator operator  
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

Parameter ||--}o CodeList : "codeList"
Parameter ||--}o ConceptProperty : "conceptProperty"
Parameter ||--}o ApplicabilityCondition : "applicableWhen"
Parameter ||--}o LogicalPredicate : "validationPredicates"
Parameter ||--}o Coding : "coding"
LogicalPredicate ||--}o RangeCheck : "rangeChecks"
LogicalPredicate ||--}o FormalExpression : "expressions"
LogicalPredicate ||--}o LogicalPredicate : "predicates"
LogicalPredicate ||--}o Coding : "coding"
LogicalPredicate ||--}o Comment : "comments"
LogicalPredicate ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
SiteOrSponsorComment ||--}o Coding : "coding"
SiteOrSponsorComment ||--}o Comment : "comments"
SiteOrSponsorComment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
RangeCheck ||--}o FormalExpression : "expressions"
RangeCheck ||--|o Check : "implementsCheck"
ApplicabilityCondition ||--}o LogicalPredicate : "predicates"
ApplicabilityCondition ||--}o Coding : "coding"
ApplicabilityCondition ||--}o Comment : "comments"
ApplicabilityCondition ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
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

```




## Inheritance
* [IdentifiableElement](../classes/IdentifiableElement.md) [ [Identifiable](../classes/Identifiable.md) [Labelled](../classes/Labelled.md)]
    * **Parameter**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [dataType](../slots/dataType.md) | 0..1 <br/> [DataType](../enums/DataType.md) | The data type of the parameter. | direct |
| [codeList](../slots/codeList.md) | * <br/> [CodeList](../classes/CodeList.md) | A list of allowed values for the parameter. | direct |
| [value](../slots/value.md) | 0..1 <br/> [String](../types/String.md) | A specific bound value for the parameter. | direct |
| [defaultValue](../slots/defaultValue.md) | 0..1 <br/> [String](../types/String.md) | A default value for the parameter. | direct |
| [items](../slots/items.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Item](../classes/Item.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[Measure](../classes/Measure.md)&nbsp;or&nbsp;<br />[DataAttribute](../classes/DataAttribute.md) | A list of item dependencies for the parameter. | direct |
| [conceptProperty](../slots/conceptProperty.md) | * <br/> [ConceptProperty](../classes/ConceptProperty.md) | Reference to a specific concept property that this parameter represents or modifies. | direct |
| [applicableWhen](../slots/applicableWhen.md) | * <br/> [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | References to different situations that define when this parameter  is applicable or required in the containing expression. Multiple applicabilityConditions are combined with OR logic: the parameter applies  if ANY referenced ApplicabilityCondition matches.<br>Within each ApplicabilityCondition, conditions are combined with AND logic. Example: applicableWhen: ["WC.ADULT", "WC.PEDIATRIC"] means the parameter  is needed when (all conditions in WC.ADULT are true) OR  (all conditions in WC.PEDIATRIC are true). | direct |
| [validationPredicates](../slots/validationPredicates.md) | * <br/> [LogicalPredicate](../classes/LogicalPredicate.md) | Validation predicates that constrain this parameter's value beyond controlled terminology. All must be satisfied (AND logic). Distinct from applicableWhen which determines if the parameter is needed at all. | direct |
| [required](../slots/required.md) | 0..1 <br/> [Boolean](../types/Boolean.md) | Indicates whether this parameter must be provided when the  containing expression is evaluated (technical constraint). | direct |
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
| [FormalExpression](../classes/FormalExpression.md) | [parameters](../slots/parameters.md) | range | [Parameter](../classes/Parameter.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:Parameter |
| native | dds:Parameter |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Parameter
description: A variable element that describes an input used in a formal expression
from_schema: https://w3id.org/dds
is_a: IdentifiableElement
attributes:
  dataType:
    name: dataType
    description: The data type of the parameter.
    from_schema: https://w3id.org/dds
    domain_of:
    - Item
    - CodeList
    - Parameter
    - ReturnValue
    range: DataType
  codeList:
    name: codeList
    description: A list of allowed values for the parameter.
    from_schema: https://w3id.org/dds
    domain_of:
    - Item
    - ConceptProperty
    - Parameter
    range: CodeList
    multivalued: true
  value:
    name: value
    description: A specific bound value for the parameter.
    from_schema: https://w3id.org/dds
    domain_of:
    - Translation
    - Parameter
    - Timing
  defaultValue:
    name: defaultValue
    description: A default value for the parameter.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Parameter
  items:
    name: items
    description: A list of item dependencies for the parameter.
    from_schema: https://w3id.org/dds
    domain_of:
    - Specification
    - ItemGroup
    - Parameter
    multivalued: true
    inlined: false
    any_of:
    - range: Item
    - range: Dimension
    - range: Measure
    - range: DataAttribute
  conceptProperty:
    name: conceptProperty
    description: Reference to a specific concept property that this parameter represents
      or modifies.
    from_schema: https://w3id.org/dds
    domain_of:
    - Item
    - Parameter
    range: ConceptProperty
    multivalued: true
    inlined: false
  applicableWhen:
    name: applicableWhen
    description: 'References to different situations that define when this parameter  is
      applicable or required in the containing expression. Multiple applicabilityConditions
      are combined with OR logic: the parameter applies  if ANY referenced ApplicabilityCondition
      matches.

      Within each ApplicabilityCondition, conditions are combined with AND logic.
      Example: applicableWhen: ["WC.ADULT", "WC.PEDIATRIC"] means the parameter  is
      needed when (all conditions in WC.ADULT are true) OR  (all conditions in WC.PEDIATRIC
      are true).'
    from_schema: https://w3id.org/dds
    domain_of:
    - Item
    - ItemGroup
    - Parameter
    - Analysis
    range: ApplicabilityCondition
    multivalued: true
    inlined: false
  validationPredicates:
    name: validationPredicates
    description: Validation predicates that constrain this parameter's value beyond
      controlled terminology. All must be satisfied (AND logic). Distinct from applicableWhen
      which determines if the parameter is needed at all.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - Parameter
    range: LogicalPredicate
    multivalued: true
    inlined: false
  required:
    name: required
    description: Indicates whether this parameter must be provided when the  containing
      expression is evaluated (technical constraint).
    from_schema: https://w3id.org/dds
    rank: 1000
    ifabsent: 'False'
    domain_of:
    - Parameter
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: Parameter
description: A variable element that describes an input used in a formal expression
from_schema: https://w3id.org/dds
is_a: IdentifiableElement
attributes:
  dataType:
    name: dataType
    description: The data type of the parameter.
    from_schema: https://w3id.org/dds
    alias: dataType
    owner: Parameter
    domain_of:
    - Item
    - CodeList
    - Parameter
    - ReturnValue
    range: DataType
  codeList:
    name: codeList
    description: A list of allowed values for the parameter.
    from_schema: https://w3id.org/dds
    alias: codeList
    owner: Parameter
    domain_of:
    - Item
    - ConceptProperty
    - Parameter
    range: CodeList
    multivalued: true
  value:
    name: value
    description: A specific bound value for the parameter.
    from_schema: https://w3id.org/dds
    alias: value
    owner: Parameter
    domain_of:
    - Translation
    - Parameter
    - Timing
    range: string
  defaultValue:
    name: defaultValue
    description: A default value for the parameter.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: defaultValue
    owner: Parameter
    domain_of:
    - Parameter
    range: string
  items:
    name: items
    description: A list of item dependencies for the parameter.
    from_schema: https://w3id.org/dds
    alias: items
    owner: Parameter
    domain_of:
    - Specification
    - ItemGroup
    - Parameter
    range: string
    multivalued: true
    inlined: false
    any_of:
    - range: Item
    - range: Dimension
    - range: Measure
    - range: DataAttribute
  conceptProperty:
    name: conceptProperty
    description: Reference to a specific concept property that this parameter represents
      or modifies.
    from_schema: https://w3id.org/dds
    alias: conceptProperty
    owner: Parameter
    domain_of:
    - Item
    - Parameter
    range: ConceptProperty
    multivalued: true
    inlined: false
  applicableWhen:
    name: applicableWhen
    description: 'References to different situations that define when this parameter  is
      applicable or required in the containing expression. Multiple applicabilityConditions
      are combined with OR logic: the parameter applies  if ANY referenced ApplicabilityCondition
      matches.

      Within each ApplicabilityCondition, conditions are combined with AND logic.
      Example: applicableWhen: ["WC.ADULT", "WC.PEDIATRIC"] means the parameter  is
      needed when (all conditions in WC.ADULT are true) OR  (all conditions in WC.PEDIATRIC
      are true).'
    from_schema: https://w3id.org/dds
    alias: applicableWhen
    owner: Parameter
    domain_of:
    - Item
    - ItemGroup
    - Parameter
    - Analysis
    range: ApplicabilityCondition
    multivalued: true
    inlined: false
  validationPredicates:
    name: validationPredicates
    description: Validation predicates that constrain this parameter's value beyond
      controlled terminology. All must be satisfied (AND logic). Distinct from applicableWhen
      which determines if the parameter is needed at all.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: validationPredicates
    owner: Parameter
    domain_of:
    - Parameter
    range: LogicalPredicate
    multivalued: true
    inlined: false
  required:
    name: required
    description: Indicates whether this parameter must be provided when the  containing
      expression is evaluated (technical constraint).
    from_schema: https://w3id.org/dds
    rank: 1000
    ifabsent: 'False'
    alias: required
    owner: Parameter
    domain_of:
    - Parameter
    range: boolean
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://w3id.org/dds
    rank: 1000
    identifier: true
    alias: OID
    owner: Parameter
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
    owner: Parameter
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: name
    owner: Parameter
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
    owner: Parameter
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
    owner: Parameter
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
    owner: Parameter
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
    owner: Parameter
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