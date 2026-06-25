

# Slot: pages 


_Reference to specific pages in a PDF document_





URI: [dds:slot/pages](https://w3id.org/dds/slot/pages)
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


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:pages |
| native | dds:pages |




## LinkML Source

<details>
```yaml
name: pages
description: Reference to specific pages in a PDF document
from_schema: https://w3id.org/dds
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