

# Slot: inputData 


_Datasets or slices/subsets of datasets asked for by this analysis. If a Item is referenced by a Parameter e.g. Analysis Variable, make sure to include its parent ItemGroup here._





URI: [dds:slot/inputData](https://w3id.org/dds/slot/inputData)
Alias: inputData

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |






## Properties

* Range: [String](../types/String.md)&nbsp;or&nbsp;<br />[ItemGroup](../classes/ItemGroup.md)&nbsp;or&nbsp;<br />[Dataset](../classes/Dataset.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:inputData |
| native | dds:inputData |




## LinkML Source

<details>
```yaml
name: inputData
description: Datasets or slices/subsets of datasets asked for by this analysis. If
  a Item is referenced by a Parameter e.g. Analysis Variable, make sure to include
  its parent ItemGroup here.
from_schema: https://w3id.org/dds
rank: 1000
alias: inputData
owner: Analysis
domain_of:
- Analysis
range: string
multivalued: true
inlined: false
any_of:
- range: ItemGroup
- range: Dataset

```
</details>