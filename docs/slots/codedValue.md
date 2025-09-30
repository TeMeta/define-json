

# Slot: codedValue 


_The value of the CodeListItem before decoding_





URI: [odm:slot/codedValue](https://cdisc.org/odm2/slot/codedValue)
Alias: codedValue

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [CodeListItem](../classes/CodeListItem.md) | A structured member of a CodeList that extends the Coding class with addition... |  no  |







## Properties

* Range: [String](../types/String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:codedValue |
| native | odm:codedValue |




## LinkML Source

<details>
```yaml
name: codedValue
description: The value of the CodeListItem before decoding
from_schema: https://cdisc.org/define-json
rank: 1000
alias: codedValue
owner: CodeListItem
domain_of:
- CodeListItem
range: string
required: true

```
</details>