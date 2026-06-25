

# Class: ODMStandardReference 


_A mixin providing attributes for CDISC standards compliance indication. Applied when serializing to Define-XML context. Not canonical._





URI: [dds:class/ODMStandardReference](https://w3id.org/dds/class/ODMStandardReference)


```mermaid
erDiagram
ODMStandardReference {
    boolean isNonStandard  
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
    AliasPredicate aliasType  
}

ODMStandardReference ||--|o Standard : "standard"
Standard ||--}o Coding : "coding"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [standard](../slots/standard.md) | 0..1 <br/> [Standard](../classes/Standard.md) | Reference to the standard being implemented | direct |
| [isNonStandard](../slots/isNonStandard.md) | 0..1 <br/> [Boolean](../types/Boolean.md) | One or more members of this set are non-standard extensions | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |









## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:ODMStandardReference |
| native | dds:ODMStandardReference |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ODMStandardReference
description: A mixin providing attributes for CDISC standards compliance indication.
  Applied when serializing to Define-XML context. Not canonical.
from_schema: https://w3id.org/dds
mixin: true
attributes:
  standard:
    name: standard
    description: Reference to the standard being implemented
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMStandardReference
    range: Standard
  isNonStandard:
    name: isNonStandard
    description: One or more members of this set are non-standard extensions
    from_schema: https://w3id.org/dds
    rank: 1000
    domain_of:
    - ODMStandardReference
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: ODMStandardReference
description: A mixin providing attributes for CDISC standards compliance indication.
  Applied when serializing to Define-XML context. Not canonical.
from_schema: https://w3id.org/dds
mixin: true
attributes:
  standard:
    name: standard
    description: Reference to the standard being implemented
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: standard
    owner: ODMStandardReference
    domain_of:
    - ODMStandardReference
    range: Standard
  isNonStandard:
    name: isNonStandard
    description: One or more members of this set are non-standard extensions
    from_schema: https://w3id.org/dds
    rank: 1000
    alias: isNonStandard
    owner: ODMStandardReference
    domain_of:
    - ODMStandardReference
    range: boolean

```
</details>