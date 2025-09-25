

# Class: GroupRelationship 


_A relationship element that associates a DataAttribute with a set of Dimensions, used when attribute values vary based on all group dimension values_





URI: [odm:GroupRelationship](https://cdisc.org/odm2/GroupRelationship)



```mermaid
erDiagram
GroupRelationship {

}
DataAttribute {
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
ComponentList {
    stringList components  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}

GroupRelationship ||--|o ComponentList : "groupKey"
GroupRelationship ||--|o DataAttribute : "attribute"
DataAttribute ||--|| Item : "item"
DataAttribute ||--|o Method : "missingHandling"
DataAttribute ||--|o Method : "imputation"
DataAttribute ||--}o Coding : "coding"
DataAttribute ||--}o Comment : "comment"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Method ||--}o FormalExpression : "formalExpressions"
Method ||--|o DocumentReference : "document"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comment"
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
ComponentList ||--}o Coding : "coding"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [groupKey](groupKey.md) | 0..1 <br/> [ComponentList](ComponentList.md) | Set of dimensions that this definition depends on | direct |
| [attribute](attribute.md) | 0..1 <br/> [DataAttribute](DataAttribute.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:GroupRelationship |
| native | odm:GroupRelationship |
| exact | sdmx:GroupRelationship |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GroupRelationship
description: A relationship element that associates a DataAttribute with a set of
  Dimensions, used when attribute values vary based on all group dimension values
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:GroupRelationship
attributes:
  groupKey:
    name: groupKey
    description: Set of dimensions that this definition depends on
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - sdmx:GroupDimensionDescriptor
    rank: 1000
    domain_of:
    - GroupRelationship
    - DimensionRelationship
    range: ComponentList
  attribute:
    name: attribute
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Resource
    - MeasureRelationship
    - DataflowRelationship
    - GroupRelationship
    - DimensionRelationship
    - ObservationRelationship
    range: DataAttribute

```
</details>

### Induced

<details>
```yaml
name: GroupRelationship
description: A relationship element that associates a DataAttribute with a set of
  Dimensions, used when attribute values vary based on all group dimension values
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:GroupRelationship
attributes:
  groupKey:
    name: groupKey
    description: Set of dimensions that this definition depends on
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - sdmx:GroupDimensionDescriptor
    rank: 1000
    alias: groupKey
    owner: GroupRelationship
    domain_of:
    - GroupRelationship
    - DimensionRelationship
    range: ComponentList
  attribute:
    name: attribute
    from_schema: https://cdisc.org/define-json
    alias: attribute
    owner: GroupRelationship
    domain_of:
    - Resource
    - MeasureRelationship
    - DataflowRelationship
    - GroupRelationship
    - DimensionRelationship
    - ObservationRelationship
    range: DataAttribute

```
</details>