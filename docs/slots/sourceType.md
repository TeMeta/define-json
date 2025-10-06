

# Slot: sourceType 


_who made the comment, such as Investigator, Sponsor._





URI: [odm:slot/sourceType](https://cdisc.org/odm2/slot/sourceType)
Alias: sourceType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |







## Properties

* Range: [OriginSource](../enums/OriginSource.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:sourceType |
| native | odm:sourceType |




## LinkML Source

<details>
```yaml
name: sourceType
description: who made the comment, such as Investigator, Sponsor.
from_schema: https://cdisc.org/define-json
rank: 1000
alias: sourceType
owner: SiteOrSponsorComment
domain_of:
- SiteOrSponsorComment
range: OriginSource

```
</details>