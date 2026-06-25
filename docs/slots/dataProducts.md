

# Slot: dataProducts 


_Indexed data flows with clear ownership_





URI: [dds:slot/dataProducts](https://w3id.org/dds/slot/dataProducts)
Alias: dataProducts

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [DataProduct](../classes/DataProduct.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:dataProducts |
| native | dds:dataProducts |




## LinkML Source

<details>
```yaml
name: dataProducts
description: Indexed data flows with clear ownership
from_schema: https://w3id.org/dds
rank: 1000
alias: dataProducts
owner: Specification
domain_of:
- Specification
range: DataProduct
multivalued: true
inlined: true
inlined_as_list: true

```
</details>