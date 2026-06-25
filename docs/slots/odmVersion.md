

# Slot: odmVersion 


_Version of the ODM standard used_





URI: [dds:slot/odmVersion](https://w3id.org/dds/slot/odmVersion)
Alias: odmVersion

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
| self | dds:odmVersion |
| native | dds:odmVersion |




## LinkML Source

<details>
```yaml
name: odmVersion
description: Version of the ODM standard used
from_schema: https://w3id.org/dds
rank: 1000
alias: odmVersion
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: string
required: true

```
</details>