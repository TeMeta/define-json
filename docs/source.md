

# Slot: source 



URI: [odm:source](https://cdisc.org/odm2/source)
Alias: source

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SiteOrSponsorComment](SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct fr... |  no  |
| [ProvisionAgreement](ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Da... |  no  |
| [DataProvider](DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a... |  no  |
| [CodingMapping](CodingMapping.md) | A mapping relationship that establishes connections between different coding ... |  no  |
| [Origin](Origin.md) | A provenance element that describes the source of data for an item |  no  |







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
- CodingMapping
- Origin
- SiteOrSponsorComment
- DataProvider
- ProvisionAgreement

```
</details>