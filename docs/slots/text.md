

# Slot: text 



URI: [dds:slot/text](https://w3id.org/dds/slot/text)
Alias: text

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Comment](../classes/Comment.md) | A descriptive element that contains explanatory text provided by a data or metadata handler |  no  |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [Query](../classes/Query.md) | A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:text |
| native | dds:text |




## LinkML Source

<details>
```yaml
name: text
alias: text
domain_of:
- Query
- Comment
- SiteOrSponsorComment
range: string

```
</details>