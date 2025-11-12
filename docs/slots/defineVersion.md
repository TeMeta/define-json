

# Slot: defineVersion 


_Version of Define-XML specification used_





URI: [odm:slot/defineVersion](https://cdisc.org/odm2/slot/defineVersion)
Alias: defineVersion

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |
| [ODMFileMetadata](../classes/ODMFileMetadata.md) | A mixin that provides ODM file-level metadata attributes including file identifiers, timestamps, and system information |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:defineVersion |
| native | odm:defineVersion |




## LinkML Source

<details>
```yaml
name: defineVersion
description: Version of Define-XML specification used
from_schema: https://cdisc.org/define-json
rank: 1000
alias: defineVersion
owner: ODMFileMetadata
domain_of:
- ODMFileMetadata
range: string

```
</details>