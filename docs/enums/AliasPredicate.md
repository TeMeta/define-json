# Enum: AliasPredicate 




_An enumeration that defines permissible values for the relationship between an element and its alias_



URI: [odm:enum/AliasPredicate](https://cdisc.org/odm2/enum/AliasPredicate)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| EXACT_SYNONYM | skos:exactMatch | Codes have identical meaning e.g. "diabetes mellitus" and "DM" |
| RELATED_SYNONYM | skos:relatedMatch | Codes are related but not equivalent e.g. "diabetes" and "mellitus" |
| BROAD_SYNONYM | skos:broaderMatch | Target is broader than source e.g. "diabetes" is broader than "type 2 diabetes" |
| NARROW_SYNONYM | skos:narrowerMatch | Target is narrower than source e.g. "type 2 diabetes" is narrower than "diabetes" |




## Slots

| Name | Description |
| ---  | --- |
| [aliasType](../slots/aliasType.md) | How this coding is related in the context of its parent element |





## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: AliasPredicate
description: An enumeration that defines permissible values for the relationship between
  an element and its alias
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  EXACT_SYNONYM:
    text: EXACT_SYNONYM
    description: Codes have identical meaning e.g. "diabetes mellitus" and "DM"
    meaning: skos:exactMatch
  RELATED_SYNONYM:
    text: RELATED_SYNONYM
    description: Codes are related but not equivalent e.g. "diabetes" and "mellitus"
    meaning: skos:relatedMatch
  BROAD_SYNONYM:
    text: BROAD_SYNONYM
    description: Target is broader than source e.g. "diabetes" is broader than "type
      2 diabetes"
    meaning: skos:broaderMatch
  NARROW_SYNONYM:
    text: NARROW_SYNONYM
    description: Target is narrower than source e.g. "type 2 diabetes" is narrower
      than "diabetes"
    meaning: skos:narrowerMatch

```
</details>