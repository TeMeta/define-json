

# Slot: context 



URI: [dds:slot/context](https://w3id.org/dds/slot/context)
Alias: context

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ODMSerializationMetadata](../classes/ODMSerializationMetadata.md) | A mixin providing ODM/Define-XML file-level attributes required only when serializing to ODM or Define-XML format. Applied by the ODM output generator, not by the canonical model itself. These attributes (fileOID, odmVersion, defineVersion, etc.) have no meaning in FHIR, OMOP, or SDMX projections. |  no  |
| [FormalExpression](../classes/FormalExpression.md) | A computational element that defines the execution of a data derivation within a specific context |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:context |
| native | dds:context |




## LinkML Source

<details>
```yaml
name: context
alias: context
domain_of:
- ODMSerializationMetadata
- FormalExpression
range: string

```
</details>