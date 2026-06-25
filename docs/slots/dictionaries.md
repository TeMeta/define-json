

# Slot: dictionaries 


_Dictionaries defined in this version of the metadata_





URI: [dds:slot/dictionaries](https://w3id.org/dds/slot/dictionaries)
Alias: dictionaries

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [Dictionary](../classes/Dictionary.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:dictionaries |
| native | dds:dictionaries |




## LinkML Source

<details>
```yaml
name: dictionaries
description: Dictionaries defined in this version of the metadata
from_schema: https://w3id.org/dds
rank: 1000
alias: dictionaries
owner: Specification
domain_of:
- Specification
range: Dictionary
multivalued: true
inlined: true
inlined_as_list: true

```
</details>