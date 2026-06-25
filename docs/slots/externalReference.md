

# Slot: externalReference 


_URI or CURIE of the published rule this check is sourced from (e.g. a CORE rule identifier), enabling reuse across metadata packages._





URI: [dds:slot/externalReference](https://w3id.org/dds/slot/externalReference)
Alias: externalReference

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Check](../classes/Check.md) | A reusable validation check included in the metadata package, such as a published CORE rule. Linked many-to-many by reference to the metadata and/or data elements it applies to, and optionally citing an external published rule so checks stay reusable and loosely coupled. Distinct from RangeCheck, which is an inline executable comparison; a RangeCheck may implement a Check. |  no  |






## Properties

* Range: [Uriorcurie](../types/Uriorcurie.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:externalReference |
| native | dds:externalReference |




## LinkML Source

<details>
```yaml
name: externalReference
description: URI or CURIE of the published rule this check is sourced from (e.g. a
  CORE rule identifier), enabling reuse across metadata packages.
from_schema: https://w3id.org/dds
rank: 1000
alias: externalReference
owner: Check
domain_of:
- Check
range: uriorcurie

```
</details>