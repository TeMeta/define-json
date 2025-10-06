

# Class: ObservationRelationship 


_A relationship element that associates a DataAttribute with an Observation, allowing value-level Items to be reused across multiple different Views_





URI: [odm:class/ObservationRelationship](https://cdisc.org/odm2/class/ObservationRelationship)



```mermaid
erDiagram
ObservationRelationship {

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

ObservationRelationship ||--|o Item : "item"
ObservationRelationship ||--|o DataAttribute : "attribute"
DataAttribute ||--|| Item : "item"
DataAttribute ||--|o Method : "missingHandling"
DataAttribute ||--|o Method : "imputation"
DataAttribute ||--}o Coding : "coding"
DataAttribute ||--}o Comment : "comments"
DataAttribute ||--}o Comment : "siteOrSponsorComments"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
Comment ||--}o Comment : "comments"
Comment ||--}o Comment : "siteOrSponsorComments"
Method ||--}o FormalExpression : "expressions"
Method ||--|o DocumentReference : "document"
Method ||--}o Coding : "coding"
Method ||--}o Comment : "comments"
Method ||--}o Comment : "siteOrSponsorComments"
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

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [item](../slots/item.md) | 0..1 <br/> [Item](../classes/Item.md) | Reference to the Item in an observation context that this definition applies to. e.g. the SDTM Variable Specialisation for a given Biomedical Concept Property. | direct |
| [attribute](../slots/attribute.md) | 0..1 <br/> [DataAttribute](../classes/DataAttribute.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:ObservationRelationship |
| native | odm:ObservationRelationship |
| exact | sdmx:ObservationRelationship |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ObservationRelationship
description: A relationship element that associates a DataAttribute with an Observation,
  allowing value-level Items to be reused across multiple different Views
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:ObservationRelationship
attributes:
  item:
    name: item
    description: Reference to the Item in an observation context that this definition
      applies to. e.g. the SDTM Variable Specialisation for a given Biomedical Concept
      Property.
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - sdmx:ObservationDescriptor
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    range: Item
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
name: ObservationRelationship
description: A relationship element that associates a DataAttribute with an Observation,
  allowing value-level Items to be reused across multiple different Views
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:ObservationRelationship
attributes:
  item:
    name: item
    description: Reference to the Item in an observation context that this definition
      applies to. e.g. the SDTM Variable Specialisation for a given Biomedical Concept
      Property.
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - sdmx:ObservationDescriptor
    alias: item
    owner: ObservationRelationship
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    range: Item
  attribute:
    name: attribute
    from_schema: https://cdisc.org/define-json
    alias: attribute
    owner: ObservationRelationship
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