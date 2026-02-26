

# Slot: outputDataflow 


_Description of the output interface before concrete Datasets exist. Dataflows referenced here represent the supply side of a ProvisionAgreement._





URI: [odm:slot/outputDataflow](https://cdisc.org/odm2/slot/outputDataflow)
Alias: outputDataflow

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |






## Properties

* Range: [Dataflow](../classes/Dataflow.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:outputDataflow |
| native | odm:outputDataflow |
| close | dcat:distribution |




## LinkML Source

<details>
```yaml
name: outputDataflow
description: Description of the output interface before concrete Datasets exist. Dataflows
  referenced here represent the supply side of a ProvisionAgreement.
from_schema: https://cdisc.org/define-json
close_mappings:
- dcat:distribution
rank: 1000
alias: outputDataflow
owner: DataProduct
domain_of:
- DataProduct
range: Dataflow
multivalued: true
inlined: true
inlined_as_list: true

```
</details>