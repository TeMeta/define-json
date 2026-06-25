

# Slot: appliesTo 


_The metadata and/or data element(s) this check applies to, referenced by OID. Multivalued and non-inlined for many-to-many, loosely coupled linkage._





URI: [dds:slot/appliesTo](https://w3id.org/dds/slot/appliesTo)
Alias: appliesTo

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Check](../classes/Check.md) | A reusable validation check included in the metadata package, such as a published CORE rule. Linked many-to-many by reference to the metadata and/or data elements it applies to, and optionally citing an external published rule so checks stay reusable and loosely coupled. Distinct from RangeCheck, which is an inline executable comparison; a RangeCheck may implement a Check. |  no  |






## Properties

* Range: [IdentifiableElement](../classes/IdentifiableElement.md)

* Multivalued: True




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:appliesTo |
| native | dds:appliesTo |




## LinkML Source

<details>
```yaml
name: appliesTo
description: The metadata and/or data element(s) this check applies to, referenced
  by OID. Multivalued and non-inlined for many-to-many, loosely coupled linkage.
from_schema: https://w3id.org/dds
rank: 1000
alias: appliesTo
owner: Check
domain_of:
- Check
range: IdentifiableElement
multivalued: true
inlined: false

```
</details>