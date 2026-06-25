

# Slot: sourceSystemVersion 


_Version of the source system_





URI: [dds:slot/sourceSystemVersion](https://w3id.org/dds/slot/sourceSystemVersion)
Alias: sourceSystemVersion

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
| self | dds:sourceSystemVersion |
| native | dds:sourceSystemVersion |




## LinkML Source

<details>
```yaml
name: sourceSystemVersion
description: Version of the source system
from_schema: https://w3id.org/dds
rank: 1000
alias: sourceSystemVersion
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string

```
</details>