

# Slot: analysisPurpose 


_The purpose or role of this analysis in the study._





URI: [odm:slot/analysisPurpose](https://cdisc.org/odm2/slot/analysisPurpose)
Alias: analysisPurpose

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
| self | odm:analysisPurpose |
| native | odm:analysisPurpose |




## LinkML Source

<details>
```yaml
name: analysisPurpose
description: The purpose or role of this analysis in the study.
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: analysisPurpose
owner: Analysis
domain_of:
- Analysis
range: string

```
</details>