

# Class: ODMItemSerialization 


_A mixin providing ODM/CDISC-specific item attributes meaningful only in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation notes, collection exception predicates, and pre-specified values. Applied by the ODM output generator. Not part of the canonical Item._





URI: [dds:class/ODMItemSerialization](https://w3id.org/dds/class/ODMItemSerialization)


```mermaid
erDiagram
ODMItemSerialization {
    string role  
    boolean hasNoData  
    string crfCompletionInstructions  
    string cdiscNotes  
    string implementationNotes  
    string preSpecifiedValue  
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
    AliasPredicate aliasType  
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

ODMItemSerialization ||--|o CodeList : "roleCodeList"
ODMItemSerialization ||--|o LogicalPredicate : "collectionExceptionPredicate"
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
CodeList ||--}o CodeListItem : "codeListItems"
CodeList ||--|o Resource : "externalCodeList"
CodeList ||--|o Standard : "standard"
CodeList ||--}o Coding : "coding"
CodeList ||--}o Comment : "comments"
CodeList ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
Standard ||--}o Coding : "coding"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
CodeListItem ||--|o Coding : "coding"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [role](../slots/role.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Identifies the role of the item within the containing context, taken from the roleCodeList | direct |
| [roleCodeList](../slots/roleCodeList.md) | 0..1 <br/> [CodeList](../classes/CodeList.md) | Reference to the CodeList that defines the roles for this item | direct |
| [hasNoData](../slots/hasNoData.md) | 0..1 <br/> [Boolean](../types/Boolean.md) | True if this is a manifest and there is no data for this item | direct |
| [crfCompletionInstructions](../slots/crfCompletionInstructions.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | CRFCompletionInstructions reference: Instructions for the clinical site on how to enter collected information on the CRF | direct |
| [cdiscNotes](../slots/cdiscNotes.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | CDISCNotes reference: Explanatory text for the variable | direct |
| [implementationNotes](../slots/implementationNotes.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | ImplementationNotes reference: Further information, such as rationale and implementation instructions, on how to implement the CRF data collection fields | direct |
| [collectionExceptionPredicate](../slots/collectionExceptionPredicate.md) | 0..1 <br/> [LogicalPredicate](../classes/LogicalPredicate.md) | Logical predicate defining when data collection for this item may be exempted. | direct |
| [preSpecifiedValue](../slots/preSpecifiedValue.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[TranslatedText](../classes/TranslatedText.md) | Prefill value or a default value for a field that is automatically populated. | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |









## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:ODMItemSerialization |
| native | dds:ODMItemSerialization |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ODMItemSerialization
description: 'A mixin providing ODM/CDISC-specific item attributes meaningful only
  in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation
  notes, collection exception predicates, and pre-specified values. Applied by the
  ODM output generator. Not part of the canonical Item.'
from_schema: https://w3id.org/dds
mixin: true
attributes:
  role:
    name: role
    description: Identifies the role of the item within the containing context, taken
      from the roleCodeList
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    - Organization
    - CubeComponent
    any_of:
    - range: string
    - range: TranslatedText
  roleCodeList:
    name: roleCodeList
    description: Reference to the CodeList that defines the roles for this item
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    range: CodeList
  hasNoData:
    name: hasNoData
    description: True if this is a manifest and there is no data for this item
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    - ItemGroup
    range: boolean
  crfCompletionInstructions:
    name: crfCompletionInstructions
    description: 'CRFCompletionInstructions reference: Instructions for the clinical
      site on how to enter collected information on the CRF'
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    any_of:
    - range: string
    - range: TranslatedText
  cdiscNotes:
    name: cdiscNotes
    description: 'CDISCNotes reference: Explanatory text for the variable'
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    any_of:
    - range: string
    - range: TranslatedText
  implementationNotes:
    name: implementationNotes
    description: 'ImplementationNotes reference: Further information, such as rationale
      and implementation instructions, on how to implement the CRF data collection
      fields'
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    any_of:
    - range: string
    - range: TranslatedText
  collectionExceptionPredicate:
    name: collectionExceptionPredicate
    description: Logical predicate defining when data collection for this item may
      be exempted.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    range: LogicalPredicate
  preSpecifiedValue:
    name: preSpecifiedValue
    description: Prefill value or a default value for a field that is automatically
      populated.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMItemSerialization
    any_of:
    - range: string
    - range: TranslatedText

```
</details>

### Induced

<details>
```yaml
name: ODMItemSerialization
description: 'A mixin providing ODM/CDISC-specific item attributes meaningful only
  in ODM/Define-XML serialization: CRF completion instructions, CDISC notes, implementation
  notes, collection exception predicates, and pre-specified values. Applied by the
  ODM output generator. Not part of the canonical Item.'
from_schema: https://w3id.org/dds
mixin: true
attributes:
  role:
    name: role
    description: Identifies the role of the item within the containing context, taken
      from the roleCodeList
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: role
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    - Organization
    - CubeComponent
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  roleCodeList:
    name: roleCodeList
    description: Reference to the CodeList that defines the roles for this item
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: roleCodeList
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: CodeList
  hasNoData:
    name: hasNoData
    description: True if this is a manifest and there is no data for this item
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: hasNoData
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    - ItemGroup
    range: boolean
  crfCompletionInstructions:
    name: crfCompletionInstructions
    description: 'CRFCompletionInstructions reference: Instructions for the clinical
      site on how to enter collected information on the CRF'
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: crfCompletionInstructions
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  cdiscNotes:
    name: cdiscNotes
    description: 'CDISCNotes reference: Explanatory text for the variable'
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: cdiscNotes
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  implementationNotes:
    name: implementationNotes
    description: 'ImplementationNotes reference: Further information, such as rationale
      and implementation instructions, on how to implement the CRF data collection
      fields'
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: implementationNotes
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  collectionExceptionPredicate:
    name: collectionExceptionPredicate
    description: Logical predicate defining when data collection for this item may
      be exempted.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: collectionExceptionPredicate
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: LogicalPredicate
  preSpecifiedValue:
    name: preSpecifiedValue
    description: Prefill value or a default value for a field that is automatically
      populated.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: preSpecifiedValue
    owner: ODMItemSerialization
    domain_of:
    - ODMItemSerialization
    range: string
    any_of:
    - range: string
    - range: TranslatedText

```
</details>