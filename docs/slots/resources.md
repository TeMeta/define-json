

# Slot: resources 


_References to resources and documents that describe this version of the metadata._





URI: [dds:slot/resources](https://w3id.org/dds/slot/resources)
Alias: resources

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[DocumentReference](../classes/DocumentReference.md)&nbsp;or&nbsp;<br />[Resource](../classes/Resource.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:resources |
| native | dds:resources |




## LinkML Source

<details>
```yaml
name: resources
description: References to resources and documents that describe this version of the
  metadata.
from_schema: https://w3id.org/dds
rank: 1000
alias: resources
owner: Specification
domain_of:
- Specification
range: string
multivalued: true
inlined: true
inlined_as_list: true
any_of:
- range: DocumentReference
- range: Resource

```
</details>