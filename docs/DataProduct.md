

# Class: DataProduct 


_A governed collection that represents a purpose-driven assembly of datasets and services with an owning team and lifecycle_





URI: [odm:DataProduct](https://cdisc.org/odm2/DataProduct)



```mermaid
erDiagram
DataProduct {
    string dataProductOwner  
    string domain  
    DataProductLifecycleStatus lifecycleStatus  
    stringList hasPolicy  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
    boolean mandatory  
    string purpose  
    datetime lastUpdated  
    string owner  
    string wasDerivedFrom  
}
Comment {
    string text  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
}
DocumentReference {
    string title  
    integerList pages  
    string relationship  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Dataset {
    string publishedBy  
    stringList keys  
    string datasetType  
    string conformsTo  
    stringList hasPolicy  
    string informationSensitivityClassification  
    string version  
    string href  
    stringList profile  
    string authenticator  
    string action  
    string reportingBegin  
    string reportingEnd  
    string dataExtractionDate  
    string validFrom  
    string validTo  
    string publicationYear  
    string publicationPeriod  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Timing {
    TimingType type  
    boolean isNominal  
    string value  
    datetime windowLower  
    datetime windowUpper  
    boolean recalled  
    string frequency  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Distribution {
    string conformsTo  
    string format  
}
DataStructureDefinition {
    boolean evolvingStructure  
    string domain  
    string structure  
    boolean isReferenceData  
    ItemGroupType type  
    stringList profile  
    string authenticator  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
    boolean mandatory  
    string purpose  
    datetime lastUpdated  
    string owner  
    string wasDerivedFrom  
    string version  
    string href  
}
Dataflow {
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
    boolean mandatory  
    string purpose  
    datetime lastUpdated  
    string owner  
    string wasDerivedFrom  
}
DataService {
    string protocol  
    string securitySchemaType  
    string resourceType  
    string attribute  
    string version  
    string href  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
FormalExpression {
    string context  
    string expression  
    string returnType  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}

DataProduct ||--}o DataService : "inputPort"
DataProduct ||--}o DataService : "outputPort"
DataProduct ||--}o Dataset : "inputDataset"
DataProduct ||--}o Dataset : "outputDataset"
DataProduct ||--}o Coding : "coding"
DataProduct ||--}o Comment : "comment"
Comment ||--}o DocumentReference : "documents"
Comment ||--}o Coding : "coding"
DocumentReference ||--}o Coding : "coding"
Dataset ||--|o Dataflow : "describedBy"
Dataset ||--|o DataStructureDefinition : "structuredBy"
Dataset ||--}o Distribution : "distribution"
Dataset ||--}o Coding : "security"
Dataset ||--|o Timing : "validityPeriod"
Dataset ||--}o Coding : "coding"
Timing ||--|o NominalOccurrence : "relativeTo"
Timing ||--|o NominalOccurrence : "relativeFrom"
Timing ||--|o Method : "imputation"
Timing ||--}o Coding : "coding"
Distribution ||--|o DataService : "accessService"
Distribution ||--|o Dataset : "isDistributionOf"
DataStructureDefinition ||--}o Dimension : "dimensions"
DataStructureDefinition ||--}o Measure : "measures"
DataStructureDefinition ||--}o DataAttribute : "attributes"
DataStructureDefinition ||--|o ComponentList : "grouping"
DataStructureDefinition ||--}o Item : "items"
DataStructureDefinition ||--}o ItemGroup : "children"
DataStructureDefinition ||--|o ReifiedConcept : "implementsConcept"
DataStructureDefinition ||--|o WhereClause : "whereClause"
DataStructureDefinition ||--}o Coding : "security"
DataStructureDefinition ||--|o Timing : "validityPeriod"
DataStructureDefinition ||--}o Coding : "coding"
DataStructureDefinition ||--}o Comment : "comment"
Dataflow ||--|| DataStructureDefinition : "structure"
Dataflow ||--}o Dimension : "dimensionConstraint"
Dataflow ||--}o Coding : "coding"
Dataflow ||--}o Comment : "comment"
DataService ||--|o Distribution : "isAccessServiceOf"
DataService ||--}o FormalExpression : "selection"
DataService ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"

```




## Inheritance
* [GovernedElement](GovernedElement.md) [ [Identifiable](Identifiable.md) [Labelled](Labelled.md) [Governed](Governed.md)]
    * **DataProduct** [ [Versioned](Versioned.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [dataProductOwner](dataProductOwner.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[User](User.md)&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md) | The person or team accountable for this data product | direct |
| [domain](domain.md) | 0..1 <br/> [String](String.md) | The functional domain or business area this product serves | direct |
| [lifecycleStatus](lifecycleStatus.md) | 0..1 <br/> [DataProductLifecycleStatus](DataProductLifecycleStatus.md) | Current lifecycle status of the data product | direct |
| [inputPort](inputPort.md) | * <br/> [DataService](DataService.md) | Services that provide input into this data product | direct |
| [outputPort](outputPort.md) | * <br/> [DataService](DataService.md) | Services that expose output from this data product | direct |
| [inputDataset](inputDataset.md) | * <br/> [Dataset](Dataset.md) | Source datasets used by the data product | direct |
| [outputDataset](outputDataset.md) | * <br/> [Dataset](Dataset.md) | Output datasets produced by the data product | direct |
| [hasPolicy](hasPolicy.md) | * <br/> [String](String.md) | Policies governing the use and access of the data product | direct |
| [version](version.md) | 0..1 <br/> [String](String.md) | The version of the external resources | [Versioned](Versioned.md) |
| [href](href.md) | 0..1 <br/> [String](String.md) | Machine-readable instructions to obtain the resource e | [Versioned](Versioned.md) |
| [OID](OID.md) | 1 <br/> [String](String.md) | Local identifier within this study/context | [Identifiable](Identifiable.md) |
| [uuid](uuid.md) | 0..1 <br/> [String](String.md) | Universal unique identifier | [Identifiable](Identifiable.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | Short name or identifier, used for field names | [Labelled](Labelled.md) |
| [description](description.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](Labelled.md) |
| [coding](coding.md) | * <br/> [Coding](Coding.md) | Semantic tags for this element | [Labelled](Labelled.md) |
| [label](label.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](Labelled.md) |
| [aliases](aliases.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Alternative name or identifier | [Labelled](Labelled.md) |
| [mandatory](mandatory.md) | 0..1 <br/> [Boolean](Boolean.md) | Is this element required? | [Governed](Governed.md) |
| [comment](comment.md) | * <br/> [Comment](Comment.md) | Comment on the element, such as a rationale for its inclusion or exclusion | [Governed](Governed.md) |
| [purpose](purpose.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Purpose or rationale for this data element | [Governed](Governed.md) |
| [lastUpdated](lastUpdated.md) | 0..1 <br/> [Datetime](Datetime.md) | When the resource was last updated | [Governed](Governed.md) |
| [owner](owner.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[User](User.md)&nbsp;or&nbsp;<br />[Organization](Organization.md)&nbsp;or&nbsp;<br />[String](String.md) | Party responsible for this element | [Governed](Governed.md) |
| [wasDerivedFrom](wasDerivedFrom.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[Item](Item.md)&nbsp;or&nbsp;<br />[ItemGroup](ItemGroup.md)&nbsp;or&nbsp;<br />[MetaDataVersion](MetaDataVersion.md)&nbsp;or&nbsp;<br />[CodeList](CodeList.md)&nbsp;or&nbsp;<br />[ReifiedConcept](ReifiedConcept.md)&nbsp;or&nbsp;<br />[ConceptProperty](ConceptProperty.md)&nbsp;or&nbsp;<br />[Condition](Condition.md)&nbsp;or&nbsp;<br />[Method](Method.md)&nbsp;or&nbsp;<br />[NominalOccurrence](NominalOccurrence.md)&nbsp;or&nbsp;<br />[Dataflow](Dataflow.md)&nbsp;or&nbsp;<br />[CubeComponent](CubeComponent.md)&nbsp;or&nbsp;<br />[DataProduct](DataProduct.md)&nbsp;or&nbsp;<br />[ProvisionAgreement](ProvisionAgreement.md) | Reference to another item that this item implements or extends, e | [Governed](Governed.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GovernedElement](GovernedElement.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Governed](Governed.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [MetaDataVersion](MetaDataVersion.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Item](Item.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [ItemGroup](ItemGroup.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [CodeList](CodeList.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [ReifiedConcept](ReifiedConcept.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [ConceptProperty](ConceptProperty.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Condition](Condition.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Method](Method.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [NominalOccurrence](NominalOccurrence.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [DataStructureDefinition](DataStructureDefinition.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Dataflow](Dataflow.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [CubeComponent](CubeComponent.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Measure](Measure.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [Dimension](Dimension.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [DataAttribute](DataAttribute.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [DataProduct](DataProduct.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |
| [ProvisionAgreement](ProvisionAgreement.md) | [wasDerivedFrom](wasDerivedFrom.md) | any_of[range] | [DataProduct](DataProduct.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:DataProduct |
| native | odm:DataProduct |
| exact | dprod:DataProduct, dcat:DataService |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataProduct
description: A governed collection that represents a purpose-driven assembly of datasets
  and services with an owning team and lifecycle
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:DataProduct
- dcat:DataService
is_a: GovernedElement
mixins:
- Versioned
attributes:
  dataProductOwner:
    name: dataProductOwner
    description: The person or team accountable for this data product
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - prov:wasAttributedTo
    rank: 1000
    domain_of:
    - DataProduct
    any_of:
    - range: User
    - range: Organization
    - range: string
  domain:
    name: domain
    description: The functional domain or business area this product serves
    from_schema: https://cdisc.org/define-json
    domain_of:
    - ItemGroup
    - DataProduct
  lifecycleStatus:
    name: lifecycleStatus
    description: Current lifecycle status of the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataProduct
    range: DataProductLifecycleStatus
  inputPort:
    name: inputPort
    description: Services that provide input into this data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataProduct
    range: DataService
    multivalued: true
    inlined: true
    inlined_as_list: true
  outputPort:
    name: outputPort
    description: Services that expose output from this data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataProduct
    range: DataService
    multivalued: true
    inlined: true
    inlined_as_list: true
  inputDataset:
    name: inputDataset
    description: Source datasets used by the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataProduct
    range: Dataset
    multivalued: true
    inlined: true
    inlined_as_list: true
  outputDataset:
    name: outputDataset
    description: Output datasets produced by the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataProduct
    range: Dataset
    multivalued: true
    inlined: true
    inlined_as_list: true
  hasPolicy:
    name: hasPolicy
    description: Policies governing the use and access of the data product
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Dataset
    - DataProduct
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: DataProduct
description: A governed collection that represents a purpose-driven assembly of datasets
  and services with an owning team and lifecycle
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:DataProduct
- dcat:DataService
is_a: GovernedElement
mixins:
- Versioned
attributes:
  dataProductOwner:
    name: dataProductOwner
    description: The person or team accountable for this data product
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - prov:wasAttributedTo
    rank: 1000
    alias: dataProductOwner
    owner: DataProduct
    domain_of:
    - DataProduct
    any_of:
    - range: User
    - range: Organization
    - range: string
  domain:
    name: domain
    description: The functional domain or business area this product serves
    from_schema: https://cdisc.org/define-json
    alias: domain
    owner: DataProduct
    domain_of:
    - ItemGroup
    - DataProduct
  lifecycleStatus:
    name: lifecycleStatus
    description: Current lifecycle status of the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: lifecycleStatus
    owner: DataProduct
    domain_of:
    - DataProduct
    range: DataProductLifecycleStatus
  inputPort:
    name: inputPort
    description: Services that provide input into this data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: inputPort
    owner: DataProduct
    domain_of:
    - DataProduct
    range: DataService
    multivalued: true
    inlined: true
    inlined_as_list: true
  outputPort:
    name: outputPort
    description: Services that expose output from this data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: outputPort
    owner: DataProduct
    domain_of:
    - DataProduct
    range: DataService
    multivalued: true
    inlined: true
    inlined_as_list: true
  inputDataset:
    name: inputDataset
    description: Source datasets used by the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: inputDataset
    owner: DataProduct
    domain_of:
    - DataProduct
    range: Dataset
    multivalued: true
    inlined: true
    inlined_as_list: true
  outputDataset:
    name: outputDataset
    description: Output datasets produced by the data product
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: outputDataset
    owner: DataProduct
    domain_of:
    - DataProduct
    range: Dataset
    multivalued: true
    inlined: true
    inlined_as_list: true
  hasPolicy:
    name: hasPolicy
    description: Policies governing the use and access of the data product
    from_schema: https://cdisc.org/define-json
    alias: hasPolicy
    owner: DataProduct
    domain_of:
    - Dataset
    - DataProduct
    multivalued: true
    inlined: true
    inlined_as_list: true
  version:
    name: version
    description: The version of the external resources
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: version
    owner: DataProduct
    domain_of:
    - Versioned
    range: string
  href:
    name: href
    description: Machine-readable instructions to obtain the resource e.g. FHIR path,
      URL
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: href
    owner: DataProduct
    domain_of:
    - Versioned
    range: string
    required: false
  OID:
    name: OID
    description: Local identifier within this study/context. Use CDISC OID format
      for regulatory submissions, or simple strings for internal use.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    identifier: true
    alias: OID
    owner: DataProduct
    domain_of:
    - Identifiable
    range: string
    required: true
    pattern: ^[A-Za-z][A-Za-z0-9._-]*$
  uuid:
    name: uuid
    description: Universal unique identifier
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: uuid
    owner: DataProduct
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: DataProduct
    domain_of:
    - Labelled
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: description
    owner: DataProduct
    domain_of:
    - Labelled
    - CodeListItem
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  coding:
    name: coding
    description: Semantic tags for this element
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: coding
    owner: DataProduct
    domain_of:
    - Labelled
    - CodeListItem
    - SourceItem
    range: Coding
    multivalued: true
    inlined: true
    inlined_as_list: true
  label:
    name: label
    description: Human-readable label, shown in UIs
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - skos:prefLabel
    rank: 1000
    alias: label
    owner: DataProduct
    domain_of:
    - Labelled
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  aliases:
    name: aliases
    description: Alternative name or identifier
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - skos:altLabel
    rank: 1000
    alias: aliases
    owner: DataProduct
    domain_of:
    - Labelled
    - CodeListItem
    range: string
    multivalued: true
    inlined: true
    inlined_as_list: true
    any_of:
    - range: string
    - range: TranslatedText
  mandatory:
    name: mandatory
    description: Is this element required?
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: mandatory
    owner: DataProduct
    domain_of:
    - Governed
    range: boolean
  comment:
    name: comment
    description: Comment on the element, such as a rationale for its inclusion or
      exclusion
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: comment
    owner: DataProduct
    domain_of:
    - Governed
    range: Comment
    multivalued: true
  purpose:
    name: purpose
    description: Purpose or rationale for this data element
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: purpose
    owner: DataProduct
    domain_of:
    - Governed
    range: string
    any_of:
    - range: string
    - range: TranslatedText
  lastUpdated:
    name: lastUpdated
    description: When the resource was last updated
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: lastUpdated
    owner: DataProduct
    domain_of:
    - Governed
    range: datetime
  owner:
    name: owner
    description: Party responsible for this element
    from_schema: https://cdisc.org/define-json
    narrow_mappings:
    - prov:wasAttributedTo
    - prov:wasAssociatedBy
    rank: 1000
    alias: owner
    owner: DataProduct
    domain_of:
    - Governed
    range: string
    any_of:
    - range: User
    - range: Organization
    - range: string
  wasDerivedFrom:
    name: wasDerivedFrom
    description: Reference to another item that this item implements or extends, e.g.
      a template Item definition.
    from_schema: https://cdisc.org/define-json
    exact_mappings:
    - prov:wasDerivedFrom
    rank: 1000
    alias: wasDerivedFrom
    owner: DataProduct
    domain_of:
    - Governed
    range: string
    any_of:
    - range: Item
    - range: ItemGroup
    - range: MetaDataVersion
    - range: CodeList
    - range: ReifiedConcept
    - range: ConceptProperty
    - range: Condition
    - range: Method
    - range: NominalOccurrence
    - range: Dataflow
    - range: CubeComponent
    - range: DataProduct
    - range: ProvisionAgreement

```
</details>