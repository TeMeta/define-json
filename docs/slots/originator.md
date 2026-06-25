

# Slot: originator 


_Organization or system that created the ODM file_





URI: [dds:slot/originator](https://w3id.org/dds/slot/originator)
Alias: originator

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMSerializationMetadata](../classes/ODMSerializationMetadata.md) | A mixin providing ODM/Define-XML file-level attributes required only when serializing to ODM or Define-XML format. Applied by the ODM output generator, not by the canonical model itself. These attributes (fileOID, odmVersion, defineVersion, etc.) have no meaning in FHIR, OMOP, or SDMX projections. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:originator |
| native | dds:originator |




## LinkML Source

<details>
```yaml
name: originator
description: Organization or system that created the ODM file
from_schema: https://w3id.org/dds
rank: 1000
alias: originator
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string

```
</details>