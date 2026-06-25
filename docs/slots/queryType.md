

# Slot: queryType 


_Whether the query is internal or external (e.g. site or sponsor originated)._





URI: [dds:slot/queryType](https://w3id.org/dds/slot/queryType)
Alias: queryType

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Query](../classes/Query.md) | A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source. |  no  |






## Properties

* Range: [QueryType](../enums/QueryType.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:queryType |
| native | dds:queryType |




## LinkML Source

<details>
```yaml
name: queryType
description: Whether the query is internal or external (e.g. site or sponsor originated).
from_schema: https://w3id.org/dds
rank: 1000
alias: queryType
owner: Query
domain_of:
- Query
range: QueryType

```
</details>