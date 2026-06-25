

# Slot: analyses 


_Analyses defined in this version of the metadata._





URI: [dds:slot/analyses](https://w3id.org/dds/slot/analyses)
Alias: analyses

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [Analysis](../classes/Analysis.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:analyses |
| native | dds:analyses |




## LinkML Source

<details>
```yaml
name: analyses
description: Analyses defined in this version of the metadata.
from_schema: https://w3id.org/dds
rank: 1000
alias: analyses
owner: Specification
domain_of:
- Specification
range: Analysis
multivalued: true
inlined: true
inlined_as_list: true

```
</details>