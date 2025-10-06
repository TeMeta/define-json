

# Class: DatasetKey 


_An abstract identifier that comprises the cross-product of dimension values to identify a specific cross-section_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [odm:class/DatasetKey](https://cdisc.org/odm2/class/DatasetKey)



```mermaid
erDiagram
DatasetKey {
    string describedBy  
    string keyValues  
    string attributeValues  
}



```




## Inheritance
* **DatasetKey**
    * [GroupKey](../classes/GroupKey.md)
    * [SeriesKey](../classes/SeriesKey.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [describedBy](../slots/describedBy.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[ComponentList](../classes/ComponentList.md) | Associates the Dimension Descriptor defined in the Data Structure Definition | direct |
| [keyValues](../slots/keyValues.md) | 0..1 <br/> [String](../types/String.md) | List of Key Values that comprise each key, separated by a dot e.g. SUBJ001.VISIT2.BMI | direct |
| [attributeValues](../slots/attributeValues.md) | 0..1 <br/> [String](../types/String.md) | Association to the Attribute Values relating to Key | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:DatasetKey |
| native | odm:DatasetKey |
| exact | sdmx:Key |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DatasetKey
description: An abstract identifier that comprises the cross-product of dimension
  values to identify a specific cross-section
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:Key
abstract: true
attributes:
  describedBy:
    name: describedBy
    description: Associates the Dimension Descriptor defined in the Data Structure
      Definition
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Dataset
    - DatasetKey
    any_of:
    - range: Dimension
    - range: ComponentList
  keyValues:
    name: keyValues
    description: List of Key Values that comprise each key, separated by a dot e.g.
      SUBJ001.VISIT2.BMI
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DatasetKey
  attributeValues:
    name: attributeValues
    description: Association to the Attribute Values relating to Key
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DatasetKey

```
</details>

### Induced

<details>
```yaml
name: DatasetKey
description: An abstract identifier that comprises the cross-product of dimension
  values to identify a specific cross-section
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:Key
abstract: true
attributes:
  describedBy:
    name: describedBy
    description: Associates the Dimension Descriptor defined in the Data Structure
      Definition
    from_schema: https://cdisc.org/define-json
    alias: describedBy
    owner: DatasetKey
    domain_of:
    - Dataset
    - DatasetKey
    any_of:
    - range: Dimension
    - range: ComponentList
  keyValues:
    name: keyValues
    description: List of Key Values that comprise each key, separated by a dot e.g.
      SUBJ001.VISIT2.BMI
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: keyValues
    owner: DatasetKey
    domain_of:
    - DatasetKey
  attributeValues:
    name: attributeValues
    description: Association to the Attribute Values relating to Key
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: attributeValues
    owner: DatasetKey
    domain_of:
    - DatasetKey

```
</details>