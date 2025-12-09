

# Slot: valueList 


_A list of possible return values._





URI: [odm:slot/valueList](https://cdisc.org/odm2/slot/valueList)
Alias: valueList

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ReturnValue](../classes/ReturnValue.md) | An output specification that defines the details of what a formal expression returns |  no  |






## Properties

* Range: [String](../types/String.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:valueList |
| native | odm:valueList |




## LinkML Source

<details>
```yaml
name: valueList
description: A list of possible return values.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: valueList
owner: ReturnValue
domain_of:
- ReturnValue
range: string
multivalued: true

```
</details>