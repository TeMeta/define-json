# Enum: QueryType 




_Whether a Query originates inside the organization (internal) or from an external party such as a site or sponsor (external)._



URI: [dds:enum/QueryType](https://w3id.org/dds/enum/QueryType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Internal | None | Query raised within the organization. |
| External | None | Query raised by an external party (e.g. site or sponsor). |




## Slots

| Name | Description |
| ---  | --- |
| [queryType](../slots/queryType.md) | Whether the query is internal or external (e.g. site or sponsor originated). |





## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: QueryType
description: Whether a Query originates inside the organization (internal) or from
  an external party such as a site or sponsor (external).
from_schema: https://w3id.org/dds
rank: 1000
permissible_values:
  Internal:
    text: Internal
    description: Query raised within the organization.
  External:
    text: External
    description: Query raised by an external party (e.g. site or sponsor).

```
</details>