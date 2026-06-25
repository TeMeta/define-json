

# Slot: fileType 


_Type of ODM file (e.g., Snapshot, Transactional)_





URI: [dds:slot/fileType](https://w3id.org/dds/slot/fileType)
Alias: fileType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMSerializationMetadata](../classes/ODMSerializationMetadata.md) | A mixin providing ODM/Define-XML file-level attributes required only when serializing to ODM or Define-XML format. Applied by the ODM output generator, not by the canonical model itself. These attributes (fileOID, odmVersion, defineVersion, etc.) have no meaning in FHIR, OMOP, or SDMX projections. |  no  |






## Properties

* Range: [String](../types/String.md)

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:fileType |
| native | dds:fileType |




## LinkML Source

<details>
```yaml
name: fileType
description: Type of ODM file (e.g., Snapshot, Transactional)
from_schema: https://w3id.org/dds
rank: 1000
alias: fileType
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string
required: true

```
</details>