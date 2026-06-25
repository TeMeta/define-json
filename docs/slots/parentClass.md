

# Slot: parentClass 


_Name of the parent Class or SubClass following CDISC Controlled Terminology._





URI: [odm:slot/parentClass](https://cdisc.org/odm2/slot/parentClass)
Alias: parentClass

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SubClass](../classes/SubClass.md) | A specific SubClass within a CDISC model Class. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:parentClass |
| native | odm:parentClass |




## LinkML Source

<details>
```yaml
name: parentClass
description: Name of the parent Class or SubClass following CDISC Controlled Terminology.
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: parentClass
owner: SubClass
domain_of:
- SubClass
range: string
required: false

```
</details>