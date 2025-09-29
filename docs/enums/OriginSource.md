# Enum: OriginSource 




_An enumeration that defines the sources of data origin_



URI: [OriginSource](../enums/OriginSource.md)

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
| [source](../slots/source.md) | The source of the data, such as Investigator, Sponsor, Subject, or Vendor |
| [sourceType](../slots/sourceType.md) | who made the comment, such as Investigator, Sponsor |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: OriginSource
description: An enumeration that defines the sources of data origin
from_schema: https://cdisc.org/define-json
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
