

# Slot: annotatedCRF 


_Reference to annotated case report forms_





URI: [odm:slot/annotatedCRF](https://cdisc.org/odm2/slot/annotatedCRF)
Alias: annotatedCRF

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linki... |  no  |







## Properties

* Range: [DocumentReference](../classes/DocumentReference.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:annotatedCRF |
| native | odm:annotatedCRF |




## LinkML Source

<details>
```yaml
name: annotatedCRF
description: Reference to annotated case report forms
from_schema: https://cdisc.org/define-json
rank: 1000
alias: annotatedCRF
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: DocumentReference
multivalued: true
inlined: true
inlined_as_list: true

```
</details>