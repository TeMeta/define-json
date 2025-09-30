

# Class: SeriesKey 


_A unique identifier that comprises the cross-product of dimension values including Time to identify observations, representing dimensions shared by all observations in a conceptual series_





URI: [odm:class/SeriesKey](https://cdisc.org/odm2/class/SeriesKey)



```mermaid
erDiagram
SeriesKey {
    string describedBy  
    string keyValues  
    string attributeValues  
}



```




## Inheritance
* [DatasetKey](../classes/DatasetKey.md)
    * **SeriesKey**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [describedBy](../slots/describedBy.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[Dimension](../classes/Dimension.md)&nbsp;or&nbsp;<br />[ComponentList](../classes/ComponentList.md) | Associates the Dimension Descriptor defined in the Data Structure Definition | [DatasetKey](../classes/DatasetKey.md) |
| [keyValues](../slots/keyValues.md) | 0..1 <br/> [String](../types/String.md) | List of Key Values that comprise each key, separated by a dot e | [DatasetKey](../classes/DatasetKey.md) |
| [attributeValues](../slots/attributeValues.md) | 0..1 <br/> [String](../types/String.md) | Association to the Attribute Values relating to Key | [DatasetKey](../classes/DatasetKey.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Dataset](../classes/Dataset.md) | [keys](../slots/keys.md) | any_of[range] | [SeriesKey](../classes/SeriesKey.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:SeriesKey |
| native | odm:SeriesKey |
| exact | sdmx:SeriesKey |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SeriesKey
description: A unique identifier that comprises the cross-product of dimension values
  including Time to identify observations, representing dimensions shared by all observations
  in a conceptual series
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:SeriesKey
is_a: DatasetKey

```
</details>

### Induced

<details>
```yaml
name: SeriesKey
description: A unique identifier that comprises the cross-product of dimension values
  including Time to identify observations, representing dimensions shared by all observations
  in a conceptual series
from_schema: https://cdisc.org/define-json
exact_mappings:
- sdmx:SeriesKey
is_a: DatasetKey
attributes:
  describedBy:
    name: describedBy
    description: Associates the Dimension Descriptor defined in the Data Structure
      Definition
    from_schema: https://cdisc.org/define-json
    alias: describedBy
    owner: SeriesKey
    domain_of:
    - Dataset
    - DatasetKey
    range: string
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
    owner: SeriesKey
    domain_of:
    - DatasetKey
    range: string
  attributeValues:
    name: attributeValues
    description: Association to the Attribute Values relating to Key
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: attributeValues
    owner: SeriesKey
    domain_of:
    - DatasetKey
    range: string

```
</details>