

# Slot: annotatedCRFs 


_Reference to annotated case report forms_





URI: [odm:slot/annotatedCRFs](https://cdisc.org/odm2/slot/annotatedCRFs)
Alias: annotatedCRFs

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MetaDataVersion](../classes/MetaDataVersion.md) | A container element that represents a given version of a specification, linking to a particular usage context such as a study, dataset, or data collection instrument. |  no  |







## Properties

* Range: [DocumentReference](../classes/DocumentReference.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:annotatedCRFs |
| native | odm:annotatedCRFs |




## LinkML Source

<details>
```yaml
name: annotatedCRFs
description: Reference to annotated case report forms
from_schema: https://cdisc.org/define-json
rank: 1000
alias: annotatedCRFs
owner: MetaDataVersion
domain_of:
- MetaDataVersion
range: DocumentReference
multivalued: true
inlined: true
inlined_as_list: true

```
</details>