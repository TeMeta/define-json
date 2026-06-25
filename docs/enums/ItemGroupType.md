# Enum: ItemGroupType 




_An enumeration that defines the roles of an item group within a specific context_



URI: [dds:enum/ItemGroupType](https://w3id.org/dds/enum/ItemGroupType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| DataCube | None | A Data Structure Definition for an Analysis Data Cube of dimensions, measures, and attributes. |
| Table | None | A simple table or data frame. |
| Object | None | An object or profile of a FHIR resource. |
| DatasetSpecialization | None | A data specialization of a concept. |
| ValueList | None | SERIALIZATION HINT for the ODM/Define-XML output generator only. Signals that this ItemGroup should render as a Define-XML ValueList element. Has no structural meaning in the canonical model hierarchy. Consider handling this as a generator-side convention rather than a canonical type in future revisions. |
| Section | None | A section of a form. |
| Form | None | A data collection form. |




## Slots

| Name | Description |
| ---  | --- |
| [type](../slots/type.md) | Type of item group |





## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: ItemGroupType
description: An enumeration that defines the roles of an item group within a specific
  context
from_schema: https://w3id.org/dds
rank: 1000
permissible_values:
  DataCube:
    text: DataCube
    description: A Data Structure Definition for an Analysis Data Cube of dimensions,
      measures, and attributes.
  Table:
    text: Table
    description: A simple table or data frame.
  Object:
    text: Object
    description: An object or profile of a FHIR resource.
  DatasetSpecialization:
    text: DatasetSpecialization
    description: A data specialization of a concept.
  ValueList:
    text: ValueList
    description: SERIALIZATION HINT for the ODM/Define-XML output generator only.
      Signals that this ItemGroup should render as a Define-XML ValueList element.
      Has no structural meaning in the canonical model hierarchy. Consider handling
      this as a generator-side convention rather than a canonical type in future revisions.
  Section:
    text: Section
    description: A section of a form.
  Form:
    text: Form
    description: A data collection form.

```
</details>