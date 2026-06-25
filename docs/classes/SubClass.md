

# Class: SubClass 


_A specific SubClass within a CDISC model Class._





URI: [odm:class/SubClass](https://cdisc.org/odm2/class/SubClass)


```mermaid
erDiagram
SubClass {
    string name  
    string parentClass  
}

SubClass ||--}o SubClass : "subClasses"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](../slots/name.md) | 1 <br/> [String](../types/String.md) | Name of the SubClass following CDISC Controlled Terminology for SubClass. | direct |
| [parentClass](../slots/parentClass.md) | 0..1 <br/> [String](../types/String.md) | Name of the parent Class or SubClass following CDISC Controlled Terminology. | direct |
| [subClasses](../slots/subClasses.md) | * <br/> [SubClass](../classes/SubClass.md) | Nested SubClass(es) for multi-level SubClass hierarchy. | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [DefClass](../classes/DefClass.md) | [subClasses](../slots/subClasses.md) | range | [SubClass](../classes/SubClass.md) |
| [SubClass](../classes/SubClass.md) | [subClasses](../slots/subClasses.md) | range | [SubClass](../classes/SubClass.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:SubClass |
| native | odm:SubClass |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SubClass
description: A specific SubClass within a CDISC model Class.
from_schema: https://cdisc.org/data-definition-spec
attributes:
  name:
    name: name
    description: Name of the SubClass following CDISC Controlled Terminology for SubClass.
    from_schema: https://cdisc.org/data-definition-spec
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    required: true
  parentClass:
    name: parentClass
    description: Name of the parent Class or SubClass following CDISC Controlled Terminology.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    domain_of:
    - SubClass
    required: false
  subClasses:
    name: subClasses
    description: Nested SubClass(es) for multi-level SubClass hierarchy.
    from_schema: https://cdisc.org/data-definition-spec
    domain_of:
    - DefClass
    - SubClass
    range: SubClass
    required: false
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: SubClass
description: A specific SubClass within a CDISC model Class.
from_schema: https://cdisc.org/data-definition-spec
attributes:
  name:
    name: name
    description: Name of the SubClass following CDISC Controlled Terminology for SubClass.
    from_schema: https://cdisc.org/data-definition-spec
    alias: name
    owner: SubClass
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    range: string
    required: true
  parentClass:
    name: parentClass
    description: Name of the parent Class or SubClass following CDISC Controlled Terminology.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: parentClass
    owner: SubClass
    domain_of:
    - SubClass
    range: string
    required: false
  subClasses:
    name: subClasses
    description: Nested SubClass(es) for multi-level SubClass hierarchy.
    from_schema: https://cdisc.org/data-definition-spec
    alias: subClasses
    owner: SubClass
    domain_of:
    - DefClass
    - SubClass
    range: SubClass
    required: false
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>