

# Slot: resourceType 


_Type of resource (e.g.,  "ODM", "HL7-FHIR", "HL7-CDA", "HL7-v2", "OpenEHR-extract")_





URI: [odm:resourceType](https://cdisc.org/odm2/resourceType)
Alias: resourceType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Resource](Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or ... |  no  |
| [DataService](DataService.md) | A service element that provides an API or endpoint for serving or receiving d... |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:resourceType |
| native | odm:resourceType |




## LinkML Source

<details>
```yaml
name: resourceType
description: Type of resource (e.g.,  "ODM", "HL7-FHIR", "HL7-CDA", "HL7-v2", "OpenEHR-extract")
from_schema: https://cdisc.org/define-json
rank: 1000
alias: resourceType
owner: Resource
domain_of:
- Resource
range: string
required: false

```
</details>