

# Slot: resourceType 


_Type of resource (e.g.,  "ODM", "HL7-FHIR", "HL7-CDA", "HL7-v2", "OpenEHR-extract")_





URI: [dds:slot/resourceType](https://w3id.org/dds/slot/resourceType)
Alias: resourceType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:resourceType |
| native | dds:resourceType |




## LinkML Source

<details>
```yaml
name: resourceType
description: Type of resource (e.g.,  "ODM", "HL7-FHIR", "HL7-CDA", "HL7-v2", "OpenEHR-extract")
from_schema: https://w3id.org/dds
rank: 1000
alias: resourceType
owner: Resource
domain_of:
- Resource
range: string
required: false

```
</details>