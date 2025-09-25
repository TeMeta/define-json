

# Slot: publishedBy 


_Associates the Data Provider that reports/publishes the data._





URI: [odm:publishedBy](https://cdisc.org/odm2/publishedBy)
Alias: publishedBy

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) | A collection element that groups observations sharing the same dimensionality... |  no  |







## Properties

* Range: NONE&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:publishedBy |
| native | odm:publishedBy |




## LinkML Source

<details>
```yaml
name: publishedBy
description: Associates the Data Provider that reports/publishes the data.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: publishedBy
owner: Dataset
domain_of:
- Dataset
any_of:
- range: Organization
- range: string

```
</details>