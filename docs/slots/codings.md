

# Slot: codings 


_Codings defined in this version of the metadata_





URI: [odm:slot/codings](https://cdisc.org/odm2/slot/codings)
Alias: codings

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |







## Properties

* Range: [Coding](../classes/Coding.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:codings |
| native | odm:codings |




## LinkML Source

<details>
```yaml
name: codings
description: Codings defined in this version of the metadata
from_schema: https://cdisc.org/define-json
rank: 1000
alias: codings
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: Coding
multivalued: true
inlined: true
inlined_as_list: true

```
</details>