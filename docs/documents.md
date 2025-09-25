

# Slot: documents 


_References to documents that contain or are referenced by this comment_





URI: [odm:documents](https://cdisc.org/odm2/documents)
Alias: documents

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Comment](Comment.md) | A descriptive element that contains explanatory text provided by a data or me... |  no  |







## Properties

* Range: [DocumentReference](DocumentReference.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:documents |
| native | odm:documents |




## LinkML Source

<details>
```yaml
name: documents
description: References to documents that contain or are referenced by this comment
from_schema: https://cdisc.org/define-json
rank: 1000
alias: documents
owner: Comment
domain_of:
- Comment
range: DocumentReference
multivalued: true

```
</details>