

# Slot: standards 


_Standards defined in this version of the metadata_





URI: [odm:slot/standards](https://cdisc.org/odm2/slot/standards)
Alias: standards

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |






## Properties

* Range: [Standard](../classes/Standard.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:standards |
| native | odm:standards |




## LinkML Source

<details>
```yaml
name: standards
description: Standards defined in this version of the metadata
from_schema: https://cdisc.org/define-json
rank: 1000
alias: standards
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: Standard
multivalued: true
inlined: true
inlined_as_list: true

```
</details>