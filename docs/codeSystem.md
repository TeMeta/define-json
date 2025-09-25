

# Slot: codeSystem 


_The code system identifier_





URI: [odm:codeSystem](https://cdisc.org/odm2/codeSystem)
Alias: codeSystem

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Coding](Coding.md) | A semantic reference that provides standardized codes and their meanings from... |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:codeSystem |
| native | odm:codeSystem |




## LinkML Source

<details>
```yaml
name: codeSystem
description: The code system identifier
from_schema: https://cdisc.org/define-json
rank: 1000
alias: codeSystem
owner: Coding
domain_of:
- Coding
range: string
required: true

```
</details>