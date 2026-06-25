

# Slot: provider 


_The Data Provider that is part of this agreement. Inlined so a standalone DTA is a self-contained snapshot._





URI: [odm:slot/provider](https://cdisc.org/odm2/slot/provider)
Alias: provider

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |






## Properties

* Range: [DataProvider](../classes/DataProvider.md)




## Identifier and Mapping Information






### Schema Source


* from schema: https://cdisc.org/data-definition-spec




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:provider |
| native | odm:provider |




## LinkML Source

<details>
```yaml
name: provider
description: The Data Provider that is part of this agreement. Inlined so a standalone
  DTA is a self-contained snapshot.
from_schema: https://cdisc.org/data-definition-spec
rank: 1000
alias: provider
owner: ProvisionAgreement
domain_of:
- ProvisionAgreement
range: DataProvider
inlined: true

```
</details>