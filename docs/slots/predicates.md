

# Slot: predicates 



URI: [dds:slot/predicates](https://w3id.org/dds/slot/predicates)
Alias: predicates

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LogicalPredicate](../classes/LogicalPredicate.md) | A reusable, composable, and nestable logical expression resolving to a boolean. Used for applicability conditions, validation rules, eligibility criteria, and skip logic. This is a data-model predicate — not a clinical condition (diagnosis). Implements usdm:Condition (the study-design predicate, distinct from the clinical FHIR Condition resource). |  no  |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |
| [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | A reusable, named applicability condition describing the circumstances under which a containing context applies. References one or more LogicalPredicates combined with AND. Distinct from LogicalPredicate (the expression itself): ApplicabilityCondition is the named, governed wrapper referenced from Items, ItemGroups, Parameters, and Analyses. |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:predicates |
| native | dds:predicates |




## LinkML Source

<details>
```yaml
name: predicates
alias: predicates
domain_of:
- Specification
- ApplicabilityCondition
- LogicalPredicate
range: string

```
</details>