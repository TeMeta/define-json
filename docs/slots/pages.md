

# Slot: pages 


_Reference to specific pages in a PDF document_





URI: [odm:slot/pages](https://cdisc.org/odm2/slot/pages)
Alias: pages

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |







## Properties

* Range: [Integer](../types/Integer.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:pages |
| native | odm:pages |




## LinkML Source

<details>
```yaml
name: pages
description: Reference to specific pages in a PDF document
from_schema: https://cdisc.org/define-json
rank: 1000
alias: pages
owner: DocumentReference
domain_of:
- DocumentReference
range: integer
required: false
multivalued: true

```
</details>