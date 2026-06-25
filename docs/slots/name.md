

# Slot: name 



URI: [dds:slot/name](https://w3id.org/dds/slot/name)
Alias: name

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [SiteOrSponsorComment](../classes/SiteOrSponsorComment.md) | A feedback element that contains comments from a site or sponsor, distinct from the general Comment class |  no  |
| [Measure](../classes/Measure.md) | A data cube property that describes a measurable quantity or value |  no  |
| [ComponentList](../classes/ComponentList.md) | An abstract definition that specifies a list of components within a data structure definition, including various descriptor types |  no  |
| [Analysis](../classes/Analysis.md) | Analysis extends Method to capture analysis-specific metadata including the reason for analysis, its purpose, and data traceability for the results used.<br>Expressions and parameters from Method can be generic or implementation-specific. |  no  |
| [Constraint](../classes/Constraint.md) | An ODRL constraint expressed as leftOperand operator rightOperand, e.g. purpose eq "safety-reporting", or dateTime lt "2026-01-01". |  no  |
| [SubClass](../classes/SubClass.md) | A specific SubClass within a CDISC model Class. |  no  |
| [Check](../classes/Check.md) | A reusable validation check included in the metadata package, such as a published CORE rule. Linked many-to-many by reference to the metadata and/or data elements it applies to, and optionally citing an external published rule so checks stay reusable and loosely coupled. Distinct from RangeCheck, which is an inline executable comparison; a RangeCheck may implement a Check. |  no  |
| [DocumentReference](../classes/DocumentReference.md) | A comprehensive reference element that points to an external document, combining elements from ODM and FHIR |  no  |
| [IdentifiableElement](../classes/IdentifiableElement.md) |  |  no  |
| [FormalExpression](../classes/FormalExpression.md) | A computational element that defines the execution of a data derivation within a specific context |  no  |
| [ItemGroup](../classes/ItemGroup.md) | A collection element that groups related items or subgroups within a specific context, used for tables, FHIR resource profiles, biomedical concept specializations, or form sections |  no  |
| [ConceptProperty](../classes/ConceptProperty.md) | A reified property concept that exists within the context of its containing topic concept |  no  |
| [Standard](../classes/Standard.md) | A collection element that groups related standards within a specific context, used for defining CDISC implementation guides and controlled terminologies |  no  |
| [Labelled](../classes/Labelled.md) | A mixin that provides slots for detailing meanings and multilingual descriptions |  no  |
| [Dimension](../classes/Dimension.md) | A data cube property that describes a categorical or hierarchical dimension |  no  |
| [DataService](../classes/DataService.md) | A service element that provides an API or endpoint for serving or receiving data |  no  |
| [Display](../classes/Display.md) | A rendered output of an analysis result. |  no  |
| [DataStructureDefinition](../classes/DataStructureDefinition.md) | A structural element that defines the organization of a data cube for analysis, including dimensions, attributes, and measures |  no  |
| [Query](../classes/Query.md) | A reified query (discrepancy, request for clarification, or annotation) raised against one or more metadata and/or data elements. Modelled as an intermediate relationship node so a single query can relate to many elements (many-to-many) and be referenced rather than embedded. Internal queries originate within the organization; external queries (e.g. site or sponsor) carry their source. |  no  |
| [CubeComponent](../classes/CubeComponent.md) | An abstract data field that represents a component in a data structure definition, referencing an Item for its definition |  no  |
| [Dictionary](../classes/Dictionary.md) | A dictionary that defines a set of codes and their meanings |  no  |
| [ProvisionAgreement](../classes/ProvisionAgreement.md) | An agreement element that describes the contractual relationship between a Data Provider and a Data Consumer regarding data provision |  no  |
| [Concept](../classes/Concept.md) | An abstract concept that can be referenced and specialised by data implementations. Holds ConceptProperties describing the concept's expected data shape. Multiple ItemGroups or Items can implement the same Concept, allowing standard biomedical concepts to be implemented differently across studies while remaining semantically aligned. |  no  |
| [ReturnValue](../classes/ReturnValue.md) | An output specification that defines the details of what a formal expression returns |  no  |
| [Method](../classes/Method.md) | A reusable computational procedure that describes how to derive values and can be referenced by Items.<br>Analysis and Derivation concepts can be implemented by a Method. Properties can be referenced by Parameters in its expressions. |  no  |
| [DataProduct](../classes/DataProduct.md) | A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle. The DataProduct defines the boundary of accountability between data producers and consumers. |  no  |
| [LogicalPredicate](../classes/LogicalPredicate.md) | A reusable, composable, and nestable logical expression resolving to a boolean. Used for applicability conditions, validation rules, eligibility criteria, and skip logic. This is a data-model predicate — not a clinical condition (diagnosis). Implements usdm:Condition (the study-design predicate, distinct from the clinical FHIR Condition resource). |  no  |
| [Dataflow](../classes/Dataflow.md) | An abstract representation that defines data provision for different reference periods, where a Distribution and its Dataset are instances |  no  |
| [CodeList](../classes/CodeList.md) | A value set that defines a discrete collection of permissible values for an item, corresponding to the ODM CodeList construct |  no  |
| [Relationship](../classes/Relationship.md) | A semantic link that defines connections between elements such as Items or ItemGroups, capturing relationships like "is the unit for" or "assesses seriousness of" |  no  |
| [Policy](../classes/Policy.md) | A set of usage and access rules (ODRL) governing data. For a DTA this is typically an ODRL Agreement between an assigner (provider) and assignee (consumer), composed of permissions, prohibitions and obligations. |  no  |
| [Rule](../classes/Rule.md) | An ODRL rule asserting that an action is permitted, prohibited, or required on a target asset, optionally restricted by constraints. |  no  |
| [User](../classes/User.md) | An entity that represents information about a specific user of a clinical data collection or data management system |  no  |
| [Resource](../classes/Resource.md) | An external reference that serves as the source for a Dataset, ItemGroup, or Item |  no  |
| [Specification](../classes/Specification.md) | The root specification container: a versioned, governed definition of the data model for a study or data product. Links items, item groups, methods, code lists, concepts, and study design references. Projects to Define-XML MetaDataVersion, FHIR ImplementationGuide, and OMOP CDM metadata. ODMSerializationMetadata is applied by the ODM output generator, not here. |  no  |
| [DataConsumer](../classes/DataConsumer.md) | An organization element that receives data from a Data Provider under a ProvisionAgreement; the demand-side counterpart of DataProvider. |  no  |
| [Organization](../classes/Organization.md) | An entity that represents organizational information, such as a site or sponsor |  no  |
| [GovernedElement](../classes/GovernedElement.md) |  |  no  |
| [DataAttribute](../classes/DataAttribute.md) | A data cube property that describes additional characteristics or metadata about observations |  no  |
| [DefClass](../classes/DefClass.md) | The predefined CDISC model Class that applies to an ItemGroupDef. |  no  |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |
| [Comment](../classes/Comment.md) | A descriptive element that contains explanatory text provided by a data or metadata handler |  no  |
| [DataProvider](../classes/DataProvider.md) | An organization element that provides data to a Data Consumer, which can be a sponsor, site, or any other entity that supplies data |  no  |
| [Item](../classes/Item.md) | A data element that represents a specific piece of information within a defined context, with data type, constraints, and derivation methods |  no  |
| [ApplicabilityCondition](../classes/ApplicabilityCondition.md) | A reusable, named applicability condition describing the circumstances under which a containing context applies. References one or more LogicalPredicates combined with AND. Distinct from LogicalPredicate (the expression itself): ApplicabilityCondition is the named, governed wrapper referenced from Items, ItemGroups, Parameters, and Analyses. |  no  |
| [Dataset](../classes/Dataset.md) | A collection element that groups observations sharing the same dimensionality, expressed as a set of unique dimensions within a Data Product context |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:name |
| native | dds:name |




## LinkML Source

<details>
```yaml
name: name
alias: name
domain_of:
- Labelled
- DefClass
- SubClass
- Standard
range: string

```
</details>