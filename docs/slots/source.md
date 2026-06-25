

# Slot: source 



URI: [dds:slot/source](https://w3id.org/dds/slot/source)
Alias: source

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [Query](../classes/Query.md) | A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source. |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [Origin](../classes/Origin.md) | A provenance element that describes the source of data for an item |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:source |
| native | dds:source |




## LinkML Source

<details>
```yaml
name: source
alias: source
domain_of:
- Query
- Origin
- SiteOrSponsorComment
- DataProvider
- ProvisionAgreement
range: string

```
</details>