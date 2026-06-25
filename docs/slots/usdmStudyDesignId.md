

# Slot: usdmStudyDesignId 


_OID or URI reference to the USDM StudyDesign that this specification implements. When present, arms, epochs, and scheduled visit slots are resolved from the referenced USDM instance. The USDM study design is the authoritative source for EPOCH, VISITNUM, ARM, and timing anchors; DDS does not redeclare them._





URI: [dds:slot/usdmStudyDesignId](https://w3id.org/dds/slot/usdmStudyDesignId)
Alias: usdmStudyDesignId

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:usdmStudyDesignId |
| native | dds:usdmStudyDesignId |




## LinkML Source

<details>
```yaml
name: usdmStudyDesignId
description: OID or URI reference to the USDM StudyDesign that this specification
  implements. When present, arms, epochs, and scheduled visit slots are resolved from
  the referenced USDM instance. The USDM study design is the authoritative source
  for EPOCH, VISITNUM, ARM, and timing anchors; DDS does not redeclare them.
from_schema: https://w3id.org/dds
rank: 1000
alias: usdmStudyDesignId
owner: Specification
domain_of:
- Specification
range: string
required: false

```
</details>