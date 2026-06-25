

# Slot: inputDataflows 


_Dataflows that supply input data for this analysis. Replaces Dataflow.analysisMethod (which had the dependency backwards — a data contract should not know which analyses consume it)._





URI: [dds:slot/inputDataflows](https://w3id.org/dds/slot/inputDataflows)
Alias: inputDataflows

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |






## Properties

* Range: [Dataflow](../classes/Dataflow.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:inputDataflows |
| native | dds:inputDataflows |




## LinkML Source

<details>
```yaml
name: inputDataflows
description: Dataflows that supply input data for this analysis. Replaces Dataflow.analysisMethod
  (which had the dependency backwards — a data contract should not know which analyses
  consume it).
from_schema: https://w3id.org/dds
rank: 1000
alias: inputDataflows
owner: Analysis
domain_of:
- Analysis
range: Dataflow
multivalued: true
inlined: false

```
</details>