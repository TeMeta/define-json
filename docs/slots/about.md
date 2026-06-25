

# Slot: about 


_The metadata and/or data element(s) this query concerns, referenced by OID. Multivalued and non-inlined to support many-to-many linkage across both metadata (e.g. Item, ItemGroup) and data (e.g. Dataset) elements._





URI: [dds:slot/about](https://w3id.org/dds/slot/about)
Alias: about

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Query](../classes/Query.md) | A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source. |  no  |






## Properties

* Range: [IdentifiableElement](../classes/IdentifiableElement.md)

* Multivalued: True

* Required: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:about |
| native | dds:about |




## LinkML Source

<details>
```yaml
name: about
description: The metadata and/or data element(s) this query concerns, referenced by
  OID. Multivalued and non-inlined to support many-to-many linkage across both metadata
  (e.g. Item, ItemGroup) and data (e.g. Dataset) elements.
from_schema: https://w3id.org/dds
rank: 1000
alias: about
owner: Query
domain_of:
- Query
range: IdentifiableElement
required: true
multivalued: true
inlined: false

```
</details>