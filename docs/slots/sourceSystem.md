

# Slot: sourceSystem 


_Source system that generated the data_





URI: [dds:slot/sourceSystem](https://w3id.org/dds/slot/sourceSystem)
Alias: sourceSystem

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
| self | dds:sourceSystem |
| native | dds:sourceSystem |




## LinkML Source

<details>
```yaml
name: sourceSystem
description: Source system that generated the data
from_schema: https://w3id.org/dds
rank: 1000
alias: sourceSystem
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string

```
</details>