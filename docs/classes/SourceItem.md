

# Class: SourceItem 


_A data source that provides the origin of information for an item_





URI: [odm:class/SourceItem](https://cdisc.org/odm2/class/SourceItem)



```mermaid
erDiagram
SourceItem {
    stringList resource  
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
Condition {
    string implementsCondition  
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
CodeList {
    DataType dataType  
    string formatName  
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
Origin {
    OriginType type  
    OriginSource source  
}
WhereClause {
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
    LogicalOperator operator  
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

SourceItem ||--|o Item : "item"
SourceItem ||--|o DocumentReference : "document"
SourceItem ||--}o Coding : "coding"
DocumentReference ||--}o Coding : "coding"
Item ||--|o CodeList : "codeList"
Item ||--|o Method : "method"
Item ||--}o RangeCheck : "rangeChecks"
Item ||--}o WhereClause : "applicableWhen"
Item ||--|o Origin : "origin"
Item ||--|o ConceptProperty : "conceptProperty"
Item ||--|o CodeList : "roleCodeList"
Item ||--|o Condition : "collectionExceptionCondition"
Item ||--}o Coding : "coding"
Item ||--}o Comment : "comments"
Item ||--}o Comment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o Comment : "siteOrSponsorComments"
Condition ||--}o RangeCheck : "rangeChecks"
Condition ||--}o FormalExpression : "expressions"
Condition ||--}o Condition : "conditions"
Condition ||--}o Coding : "coding"
Condition ||--}o Comment : "comments"
Condition ||--}o Comment : "siteOrSponsorComments"
CodeList ||--}o CodeListItem : "codeListItems"
CodeList ||--|o Resource : "externalCodeList"
CodeList ||--}o Coding : "coding"
CodeList ||--}o Comment : "comments"
CodeList ||--}o Comment : "siteOrSponsorComments"
ConceptProperty ||--|o CodeList : "codeList"
ConceptProperty ||--}o Coding : "coding"
ConceptProperty ||--}o Comment : "comments"
ConceptProperty ||--}o Comment : "siteOrSponsorComments"
Origin ||--}o SourceItem : "sourceItems"
Origin ||--|o DocumentReference : "document"
WhereClause ||--}o Condition : "conditions"
WhereClause ||--}o Coding : "coding"
WhereClause ||--}o Comment : "comments"
WhereClause ||--}o Comment : "siteOrSponsorComments"
RangeCheck ||--}o FormalExpression : "expressions"
Method ||--}o FormalExpression : "expressions"
Method ||--|o DocumentReference : "document"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comments"
Method ||--}o Comment : "siteOrSponsorComments"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [item](../slots/item.md) | 0..1 <br/> [Item](../classes/Item.md) | Reference to an item | direct |
| [document](../slots/document.md) | 0..1 <br/> [DocumentReference](../classes/DocumentReference.md) | Reference to an external document | direct |
| [resource](../slots/resource.md) | * <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Resource](../classes/Resource.md)&nbsp;or&nbsp;<br />[String](../types/String.md) | Path to a resource (e.g. File, FHIR datasource) that is the source of this item | direct |
| [coding](../slots/coding.md) | * <br/> [Coding](../classes/Coding.md) | A coding that describes the source of the item | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Origin](../classes/Origin.md) | [sourceItems](../slots/sourceItems.md) | range | [SourceItem](../classes/SourceItem.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:SourceItem |
| native | odm:SourceItem |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SourceItem
description: A data source that provides the origin of information for an item
from_schema: https://cdisc.org/define-json
attributes:
  item:
    name: item
    description: Reference to an item
    from_schema: https://cdisc.org/define-json
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    range: Item
    inlined: false
  document:
    name: document
    description: Reference to an external document
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Method
    - SourceItem
    - Origin
    range: DocumentReference
  resource:
    name: resource
    description: Path to a resource (e.g. File, FHIR datasource) that is the source
      of this item
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - SourceItem
    multivalued: true
    inlined: false
    any_of:
    - range: Resource
    - range: string
  coding:
    name: coding
    description: A coding that describes the source of the item
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Labelled
    - CodeListItem
    - SourceItem
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: SourceItem
description: A data source that provides the origin of information for an item
from_schema: https://cdisc.org/define-json
attributes:
  item:
    name: item
    description: Reference to an item
    from_schema: https://cdisc.org/define-json
    alias: item
    owner: SourceItem
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    range: Item
    inlined: false
  document:
    name: document
    description: Reference to an external document
    from_schema: https://cdisc.org/define-json
    alias: document
    owner: SourceItem
    domain_of:
    - Method
    - SourceItem
    - Origin
    range: DocumentReference
  resource:
    name: resource
    description: Path to a resource (e.g. File, FHIR datasource) that is the source
      of this item
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: resource
    owner: SourceItem
    domain_of:
    - SourceItem
    multivalued: true
    inlined: false
    any_of:
    - range: Resource
    - range: string
  coding:
    name: coding
    description: A coding that describes the source of the item
    from_schema: https://cdisc.org/define-json
    alias: coding
    owner: SourceItem
    domain_of:
    - Labelled
    - CodeListItem
    - SourceItem
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>