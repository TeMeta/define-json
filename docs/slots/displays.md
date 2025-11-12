

# Slot: displays 


_Displays defined in this version of the metadata._





URI: [odm:slot/displays](https://cdisc.org/odm2/slot/displays)
Alias: displays

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |







## Properties

* Range: [Display](../classes/Display.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:displays |
| native | odm:displays |




## LinkML Source

<details>
```yaml
name: displays
description: Displays defined in this version of the metadata.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: displays
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: Display
multivalued: true
inlined: true
inlined_as_list: true

```
</details>