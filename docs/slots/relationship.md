

# Slot: relationship 


_Relationship to the referencing entity_





URI: [odm:slot/relationship](https://cdisc.org/odm2/slot/relationship)
Alias: relationship

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combin... |  no  |







## Properties

* Range: [String](../types/String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:relationship |
| native | odm:relationship |




## LinkML Source

<details>
```yaml
name: relationship
description: Relationship to the referencing entity
from_schema: https://cdisc.org/define-json
rank: 1000
alias: relationship
owner: DocumentReference
domain_of:
- DocumentReference
range: string
required: false

```
</details>