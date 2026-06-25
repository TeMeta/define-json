# Enum: OriginSource 




_An enumeration that defines the sources of data origin. Values sourced from NCI Thesaurus subset C170450._



URI: [dds:enum/OriginSource](https://w3id.org/dds/enum/OriginSource)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Investigator | ncit:C25936 |  |
| Sponsor | ncit:C70793 |  |
| Subject | ncit:C41189 |  |
| Vendor | ncit:C68608 |  |




## Slots

| Name | Description |
| ---  | --- |
| [sourceType](../slots/sourceType.md) | who made the comment, such as Investigator, Sponsor. |





## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: OriginSource
description: An enumeration that defines the sources of data origin. Values sourced
  from NCI Thesaurus subset C170450.
from_schema: https://w3id.org/dds
rank: 1000
permissible_values:
  Investigator:
    text: Investigator
    meaning: ncit:C25936
  Sponsor:
    text: Sponsor
    meaning: ncit:C70793
  Subject:
    text: Subject
    meaning: ncit:C41189
  Vendor:
    text: Vendor
    meaning: ncit:C68608

```
</details>