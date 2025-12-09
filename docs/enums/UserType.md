# Enum: UserType 




_An enumeration that defines the types of users in a clinical data collection or management system_



URI: [odm:enum/UserType](https://cdisc.org/odm2/enum/UserType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Sponsor | None |  |
| Investigator | None |  |
| Lab | None |  |
| Other | None |  |
| Subject | None |  |
| Monitor | None |  |
| Data analyst | None |  |
| Care provider | None |  |
| Assessor | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [userType](../slots/userType.md) | User's role in the study. |





## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/define-json






## LinkML Source

<details>
```yaml
name: UserType
description: An enumeration that defines the types of users in a clinical data collection
  or management system
from_schema: https://cdisc.org/define-json
rank: 1000
permissible_values:
  Sponsor:
    text: Sponsor
  Investigator:
    text: Investigator
  Lab:
    text: Lab
  Other:
    text: Other
  Subject:
    text: Subject
  Monitor:
    text: Monitor
  Data analyst:
    text: Data analyst
  Care provider:
    text: Care provider
  Assessor:
    text: Assessor

```
</details>