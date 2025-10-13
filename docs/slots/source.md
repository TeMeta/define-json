

# Slot: source 



URI: [odm:slot/source](https://cdisc.org/odm2/slot/source)
Alias: source

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Origin](../classes/Origin.md) | A provenance element that describes the source of data for an item |  no  |







## Properties

* Range: NONE





## Identifier and Mapping Information








## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:source |
| native | odm:source |




## LinkML Source

<details>
```yaml
name: source
alias: source
domain_of:
- Origin
- SiteOrSponsorComment
- DataProvider
- ProvisionAgreement

```
</details>