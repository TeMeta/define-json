

# Slot: fileOID 


_Unique identifier for the ODM file_





URI: [dds:slot/fileOID](https://w3id.org/dds/slot/fileOID)
Alias: fileOID

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
| self | dds:fileOID |
| native | dds:fileOID |




## LinkML Source

<details>
```yaml
name: fileOID
description: Unique identifier for the ODM file
from_schema: https://w3id.org/dds
rank: 1000
alias: fileOID
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string
required: true

```
</details>