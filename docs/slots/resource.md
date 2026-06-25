

# Slot: resource 


_Path to a resource (e.g. File, FHIR datasource) that is the source of this item_





URI: [dds:slot/resource](https://w3id.org/dds/slot/resource)
Alias: resource

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SourceItem](../classes/SourceItem.md) | A data source that provides the origin of information for an item |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[Resource](../classes/Resource.md)&nbsp;or&nbsp;<br />[String](../types/String.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:resource |
| native | dds:resource |




## LinkML Source

<details>
```yaml
name: resource
description: Path to a resource (e.g. File, FHIR datasource) that is the source of
  this item
from_schema: https://w3id.org/dds
rank: 1000
alias: resource
owner: SourceItem
domain_of:
- SourceItem
range: string
multivalued: true
inlined: false
any_of:
- range: Resource
- range: string

```
</details>