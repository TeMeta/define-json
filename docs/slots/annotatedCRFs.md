

# Slot: annotatedCRFs 


_Reference to annotated case report forms_





URI: [dds:slot/annotatedCRFs](https://w3id.org/dds/slot/annotatedCRFs)
Alias: annotatedCRFs

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [DocumentReference](../classes/DocumentReference.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:annotatedCRFs |
| native | dds:annotatedCRFs |




## LinkML Source

<details>
```yaml
name: annotatedCRFs
description: Reference to annotated case report forms
from_schema: https://w3id.org/dds
rank: 1000
alias: annotatedCRFs
owner: Specification
domain_of:
- Specification
range: DocumentReference
multivalued: true
inlined: true
inlined_as_list: true

```
</details>