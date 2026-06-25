

# Slot: document 


_Reference to an external document_





URI: [dds:slot/document](https://w3id.org/dds/slot/document)
Alias: document

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SourceItem](../classes/SourceItem.md) | A data source that provides the origin of information for an item |  no  |






## Properties

* Range: [DocumentReference](../classes/DocumentReference.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:document |
| native | dds:document |




## LinkML Source

<details>
```yaml
name: document
description: Reference to an external document
from_schema: https://w3id.org/dds
rank: 1000
alias: document
owner: SourceItem
domain_of:
- SourceItem
range: DocumentReference
multivalued: true
inlined: true
inlined_as_list: true

```
</details>