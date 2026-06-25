

# Slot: asOfDateTime 


_Date and time when the data snapshot was taken_





URI: [dds:slot/asOfDateTime](https://w3id.org/dds/slot/asOfDateTime)
Alias: asOfDateTime

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMSerializationMetadata](../classes/ODMSerializationMetadata.md) | A mixin providing ODM/Define-XML file-level attributes required only when serializing to ODM or Define-XML format. Applied by the ODM output generator, not by the canonical model itself. These attributes (fileOID, odmVersion, defineVersion, etc.) have no meaning in FHIR, OMOP, or SDMX projections. |  no  |






## Properties

* Range: [Datetime](../types/Datetime.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:asOfDateTime |
| native | dds:asOfDateTime |




## LinkML Source

<details>
```yaml
name: asOfDateTime
description: Date and time when the data snapshot was taken
from_schema: https://w3id.org/dds
rank: 1000
alias: asOfDateTime
owner: ODMSerializationMetadata
domain_of:
- ODMSerializationMetadata
range: datetime

```
</details>