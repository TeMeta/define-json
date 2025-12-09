

# Slot: leafID 


_Leaf identifier for document reference in Define-XML_





URI: [odm:slot/leafID](https://cdisc.org/odm2/slot/leafID)
Alias: leafID

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:leafID |
| native | odm:leafID |




## LinkML Source

<details>
```yaml
name: leafID
description: Leaf identifier for document reference in Define-XML
from_schema: https://cdisc.org/define-json
rank: 1000
alias: leafID
owner: DocumentReference
domain_of:
- DocumentReference
range: string

```
</details>