

# Slot: dataFlow 



URI: [dds:slot/dataFlow](https://w3id.org/dds/slot/dataFlow)
Alias: dataFlow

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [DataflowRelationship](../classes/DataflowRelationship.md) | A relationship element that associates a DataAttribute with a Dataflow, reported at the Dataset level |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:dataFlow |
| native | dds:dataFlow |




## LinkML Source

<details>
```yaml
name: dataFlow
alias: dataFlow
domain_of:
- DataflowRelationship
- ProvisionAgreement
range: string

```
</details>