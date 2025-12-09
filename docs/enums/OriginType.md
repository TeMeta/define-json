# Enum: OriginType 




_An enumeration that defines the types of origins for data items._



URI: [odm:enum/OriginType](https://cdisc.org/odm2/enum/OriginType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Assigned | ncit:C170547 | A value that is derived through designation, such as values from a look up table or a label on a CRF. |
| Collected | ncit:C170548 | A value that is actually observed and recorded by a person or obtained by an instrument. |
| Derived | ncit:C170549 | A value that is calculated by an algorithm or reproducible rule, and which is dependent upon other data values. |
| Not Available | ncit:C126101 | A value that is not discoverable or accessible. |
| Other | None | Different than the one(s) previously specified or mentioned. (NCI) |
| Predecessor | ncit:C170550 | A value that is copied from another variable. |
| Protocol | ncit:C170551 | A value that is included as part of the study protocol. |








## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: OriginType
description: An enumeration that defines the types of origins for data items.
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  Assigned:
    text: Assigned
    description: A value that is derived through designation, such as values from
      a look up table or a label on a CRF.
    meaning: ncit:C170547
  Collected:
    text: Collected
    description: A value that is actually observed and recorded by a person or obtained
      by an instrument.
    meaning: ncit:C170548
  Derived:
    text: Derived
    description: A value that is calculated by an algorithm or reproducible rule,
      and which is dependent upon other data values.
    meaning: ncit:C170549
  Not Available:
    text: Not Available
    description: A value that is not discoverable or accessible.
    meaning: ncit:C126101
  Other:
    text: Other
    description: Different than the one(s) previously specified or mentioned. (NCI)
  Predecessor:
    text: Predecessor
    description: A value that is copied from another variable.
    meaning: ncit:C170550
  Protocol:
    text: Protocol
    description: A value that is included as part of the study protocol.
    meaning: ncit:C170551

```
</details>