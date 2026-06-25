

# Class: RangeCheck 


_A validation element that performs a simple comparison check between a referenced item's value and specified values, resolving to a boolean result_





URI: [dds:class/RangeCheck](https://w3id.org/dds/class/RangeCheck)


```mermaid
erDiagram
RangeCheck {
    Comparator comparator  
    stringList checkValues  
    string item  
    SoftHard softHard  
    LogicalOperator operator  
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
IdentifiableElement {
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}

RangeCheck ||--}o FormalExpression : "expressions"
RangeCheck ||--|o Check : "implementsCheck"
Check ||--}o IdentifiableElement : "appliesTo"
Check ||--}o FormalExpression : "expressions"
Check ||--}o Coding : "coding"
Check ||--}o Comment : "comments"
Check ||--}o SiteOrSponsorComment : "siteOrSponsorComments"
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
IdentifiableElement ||--}o Coding : "coding"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [comparator](../slots/comparator.md) | 0..1 <br/> [Comparator](../enums/Comparator.md) | The type of comparison to be performed | direct |
| [checkValues](../slots/checkValues.md) | * <br/> [String](../types/String.md) | Values to compare against | direct |
| [item](../slots/item.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Item](../classes/Item.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[Measure](../classes/Measure.md)&nbsp;or&nbsp;<br />[DataAttribute](../classes/DataAttribute.md) | Reference to the Item element whose value is being checked. If not specified, check applies to the enclosing context | direct |
| [softHard](../slots/softHard.md) | 0..1 <br/> [SoftHard](../enums/SoftHard.md) | Indicates whether a validation check is an error ("Hard") or a warning ("Soft") | direct |
| [expressions](../slots/expressions.md) | * <br/> [FormalExpression](../classes/FormalExpression.md) | A formal expression for complex checks | direct |
| [operator](../slots/operator.md) | 0..1 <br/> [LogicalOperator](../enums/LogicalOperator.md) | Logical operator for combining child conditions or range checks. Defaults to ALL if not specified. | direct |
| [implementsCheck](../slots/implementsCheck.md) | 0..1 <br/> [Check](../classes/Check.md) | Optional reference (by OID) to a reusable Check (e.g. a published CORE rule) that this inline RangeCheck implements. | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Item](../classes/Item.md) | [rangeChecks](../slots/rangeChecks.md) | range | [RangeCheck](../classes/RangeCheck.md) |
| [LogicalPredicate](../classes/LogicalPredicate.md) | [rangeChecks](../slots/rangeChecks.md) | range | [RangeCheck](../classes/RangeCheck.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:RangeCheck |
| native | dds:RangeCheck |
| related | qb:SliceKey, sdmx:DataKey |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RangeCheck
description: A validation element that performs a simple comparison check between
  a referenced item's value and specified values, resolving to a boolean result
from_schema: https://w3id.org/dds
related_mappings:
- qb:SliceKey
- sdmx:DataKey
attributes:
  comparator:
    name: comparator
    description: The type of comparison to be performed
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - RangeCheck
    range: Comparator
  checkValues:
    name: checkValues
    description: Values to compare against
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - RangeCheck
    multivalued: true
    inlined: true
    inlined_as_list: true
  item:
    name: item
    description: Reference to the Item element whose value is being checked. If not
      specified, check applies to the enclosing context
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    any_of:
    - range: Item
    - range: Dimension
    - range: Measure
    - range: DataAttribute
  softHard:
    name: softHard
    description: Indicates whether a validation check is an error ("Hard") or a warning
      ("Soft")
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - RangeCheck
    range: SoftHard
  expressions:
    name: expressions
    description: A formal expression for complex checks
    from_schema: https://w3id.org/dds
    domain_of:
    - LogicalPredicate
    - RangeCheck
    - Check
    - Method
    range: FormalExpression
    multivalued: true
    inlined: true
    inlined_as_list: true
  operator:
    name: operator
    description: Logical operator for combining child conditions or range checks.
      Defaults to ALL if not specified.
    from_schema: https://w3id.org/dds
    ifabsent: LogicalOperator(AND)
    domain_of:
    - LogicalPredicate
    - RangeCheck
    - Constraint
    range: LogicalOperator
    required: false
  implementsCheck:
    name: implementsCheck
    description: Optional reference (by OID) to a reusable Check (e.g. a published
      CORE rule) that this inline RangeCheck implements.
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - RangeCheck
    range: Check
    inlined: false

```
</details>

### Induced

<details>
```yaml
name: RangeCheck
description: A validation element that performs a simple comparison check between
  a referenced item's value and specified values, resolving to a boolean result
from_schema: https://w3id.org/dds
related_mappings:
- qb:SliceKey
- sdmx:DataKey
attributes:
  comparator:
    name: comparator
    description: The type of comparison to be performed
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: comparator
    owner: RangeCheck
    domain_of:
    - RangeCheck
    range: Comparator
  checkValues:
    name: checkValues
    description: Values to compare against
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: checkValues
    owner: RangeCheck
    domain_of:
    - RangeCheck
    range: string
    multivalued: true
    inlined: true
    inlined_as_list: true
  item:
    name: item
    description: Reference to the Item element whose value is being checked. If not
      specified, check applies to the enclosing context
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: item
    owner: RangeCheck
    domain_of:
    - RangeCheck
    - SourceItem
    - CubeComponent
    - ObservationRelationship
    range: string
    any_of:
    - range: Item
    - range: Dimension
    - range: Measure
    - range: DataAttribute
  softHard:
    name: softHard
    description: Indicates whether a validation check is an error ("Hard") or a warning
      ("Soft")
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: softHard
    owner: RangeCheck
    domain_of:
    - RangeCheck
    range: SoftHard
  expressions:
    name: expressions
    description: A formal expression for complex checks
    from_schema: https://w3id.org/dds
    alias: expressions
    owner: RangeCheck
    domain_of:
    - LogicalPredicate
    - RangeCheck
    - Check
    - Method
    range: FormalExpression
    multivalued: true
    inlined: true
    inlined_as_list: true
  operator:
    name: operator
    description: Logical operator for combining child conditions or range checks.
      Defaults to ALL if not specified.
    from_schema: https://w3id.org/dds
    ifabsent: LogicalOperator(AND)
    alias: operator
    owner: RangeCheck
    domain_of:
    - LogicalPredicate
    - RangeCheck
    - Constraint
    range: LogicalOperator
    required: false
  implementsCheck:
    name: implementsCheck
    description: Optional reference (by OID) to a reusable Check (e.g. a published
      CORE rule) that this inline RangeCheck implements.
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: implementsCheck
    owner: RangeCheck
    domain_of:
    - RangeCheck
    range: Check
    inlined: false

```
</details>