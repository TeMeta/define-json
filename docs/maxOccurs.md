

# Slot: maxOccurs 


_Maximum number of occurrences of this property in the context. Leave empty for unbounded. Set to 0 to disable property_





URI: [odm:maxOccurs](https://cdisc.org/odm2/maxOccurs)
Alias: maxOccurs

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ConceptProperty](ConceptProperty.md) | A reified property concept that exists within the context of its containing t... |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:maxOccurs |
| native | odm:maxOccurs |




## LinkML Source

<details>
```yaml
name: maxOccurs
description: Maximum number of occurrences of this property in the context. Leave
  empty for unbounded. Set to 0 to disable property
from_schema: https://cdisc.org/define-json
rank: 1000
alias: maxOccurs
owner: ConceptProperty
domain_of:
- ConceptProperty
range: integer

```
</details>