

# Class: DefClass 


_The predefined CDISC model Class that applies to an ItemGroupDef._





URI: [odm:class/DefClass](https://cdisc.org/odm2/class/DefClass)


```mermaid
erDiagram
DefClass {
    string name  
}
SubClass {
    string name  
    string parentClass  
}

DefClass ||--}o SubClass : "subClasses"
SubClass ||--}o SubClass : "subClasses"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](../slots/name.md) | 1 <br/> [String](../types/String.md) | Name of the General Observation Class following CDISC Controlled Terminology. | direct |
| [subClasses](../slots/subClasses.md) | * <br/> [SubClass](../classes/SubClass.md) | One or more SubClasses that further identify the specific SubClass within a Class. | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ItemGroup](../classes/ItemGroup.md) | [observationClass](../slots/observationClass.md) | range | [DefClass](../classes/DefClass.md) |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | [observationClass](../slots/observationClass.md) | range | [DefClass](../classes/DefClass.md) |







## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:DefClass |
| native | odm:DefClass |






## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefClass
description: The predefined CDISC model Class that applies to an ItemGroupDef.
from_schema: https://cdisc.org/data-definition-spec
attributes:
  name:
    name: name
    description: Name of the General Observation Class following CDISC Controlled
      Terminology.
    from_schema: https://cdisc.org/data-definition-spec
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    required: true
  subClasses:
    name: subClasses
    description: One or more SubClasses that further identify the specific SubClass
      within a Class.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
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
name: DefClass
description: The predefined CDISC model Class that applies to an ItemGroupDef.
from_schema: https://cdisc.org/data-definition-spec
attributes:
  name:
    name: name
    description: Name of the General Observation Class following CDISC Controlled
      Terminology.
    from_schema: https://cdisc.org/data-definition-spec
    alias: name
    owner: DefClass
    domain_of:
    - Labelled
    - DefClass
    - SubClass
    - Standard
    range: string
    required: true
  subClasses:
    name: subClasses
    description: One or more SubClasses that further identify the specific SubClass
      within a Class.
    from_schema: https://cdisc.org/data-definition-spec
    rank: 1000
    alias: subClasses
    owner: DefClass
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