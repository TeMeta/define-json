

# Slot: analysisReason 


_The reason this analysis was performed.  _





URI: [odm:slot/analysisReason](https://cdisc.org/odm2/slot/analysisReason)
Alias: analysisReason

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:analysisReason |
| native | odm:analysisReason |




## LinkML Source

<details>
```yaml
name: analysisReason
description: 'The reason this analysis was performed.  '
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: analysisReason
owner: Analysis
domain_of:
- Analysis
range: string

```
</details>