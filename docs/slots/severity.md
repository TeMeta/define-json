

# Slot: severity 


_Whether a failure is an error ("Hard") or a warning ("Soft")._





URI: [dds:slot/severity](https://w3id.org/dds/slot/severity)
Alias: severity

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Check](../classes/Check.md) | A reusable validation check included in the metadata package, such as a published CORE rule. Linked many-to-many by reference to the metadata and/or data elements it applies to, and optionally citing an external published rule so checks stay reusable and loosely coupled. Distinct from RangeCheck, which is an inline executable comparison; a RangeCheck may implement a Check. |  no  |






## Properties

* Range: [SoftHard](../enums/SoftHard.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:severity |
| native | dds:severity |




## LinkML Source

<details>
```yaml
name: severity
description: Whether a failure is an error ("Hard") or a warning ("Soft").
from_schema: https://w3id.org/dds
rank: 1000
alias: severity
owner: Check
domain_of:
- Check
range: SoftHard

```
</details>