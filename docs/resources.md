

# Slot: resources 


_References to documents that describe this version of the metadata._





URI: [odm:resources](https://cdisc.org/odm2/resources)
Alias: resources

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[DocumentReference](DocumentReference.md)&nbsp;or&nbsp;<br />[Resource](Resource.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:resources |
| native | odm:resources |




## LinkML Source

<details>
```yaml
name: resources
description: References to documents that describe this version of the metadata.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: resources
owner: MetaDataVersion
domain_of:
- MetaDataVersion
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: DocumentReference
- range: Resource

```
</details>