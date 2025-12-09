# Enum: PublishingSet 




_An enumeration that defines permissible values for publishing sets_



URI: [odm:enum/PublishingSet](https://cdisc.org/odm2/enum/PublishingSet)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| ADaM | None | Analysis Data Model |
| CDASH | None | Clinical Data Acquisition Standards Harmonization |
| DEFINE-XML | None | Define-XML Standard |
| SDTM | None | Study Data Tabulation Model |
| SEND | None | Standard for Exchange of Non-clinical Data |




## Slots

| Name | Description |
| ---  | --- |
| [publishingSet](../slots/publishingSet.md) | Publishing Set of a Controlled Terminology |





## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: PublishingSet
description: An enumeration that defines permissible values for publishing sets
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  ADaM:
    text: ADaM
    description: Analysis Data Model
  CDASH:
    text: CDASH
    description: Clinical Data Acquisition Standards Harmonization
  DEFINE-XML:
    text: DEFINE-XML
    description: Define-XML Standard
  SDTM:
    text: SDTM
    description: Study Data Tabulation Model
  SEND:
    text: SEND
    description: Standard for Exchange of Non-clinical Data

```
</details>