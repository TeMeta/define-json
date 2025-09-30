# Enum: ItemGroupType 




_An enumeration that defines the roles of an item group within a specific context_



URI: [ItemGroupType](../enums/ItemGroupType.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| DataCube | None | A Data Structure Definition for an Analysis Data Cube of dimensions, measures... |
| Table | None | A simple table or data frame |
| Object | None | An object or profile of a FHIR resource |
| DataSpecialization | None | A data specialization of a concept |
| Section | None | A section of a form |
| Form | None | A data collection form |




## Slots

| Name | Description |
| ---  | --- |
| [type](../slots/type.md) | Type of item group |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: ItemGroupType
description: An enumeration that defines the roles of an item group within a specific
  context
from_schema: https://cdisc.org/define-json
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
  DataSpecialization:
    text: DataSpecialization
    description: A data specialization of a concept.
  Section:
    text: Section
    description: A section of a form.
  Form:
    text: Form
    description: A data collection form.

```
</details>
