

# Slot: creationDateTime 


_Date and time when the ODM file was created_





URI: [dds:slot/creationDateTime](https://w3id.org/dds/slot/creationDateTime)
Alias: creationDateTime

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMSerializationMetadata](../classes/ODMSerializationMetadata.md) | A mixin providing ODM/Define-XML file-level attributes required only when serializing to ODM or Define-XML format. Applied by the ODM output generator, not by the canonical model itself. These attributes (fileOID, odmVersion, defineVersion, etc.) have no meaning in FHIR, OMOP, or SDMX projections. |  no  |






## Properties

* Range: [Datetime](../types/Datetime.md)

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:creationDateTime |
| native | dds:creationDateTime |




## LinkML Source

<details>
```yaml
name: creationDateTime
description: Date and time when the ODM file was created
from_schema: https://w3id.org/dds
rank: 1000
alias: creationDateTime
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: datetime
required: true

```
</details>