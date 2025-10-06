

# Class: Distribution 


_A technical representation that provides a specific format or access method for a dataset_





URI: [odm:class/Distribution](https://cdisc.org/odm2/class/Distribution)



```mermaid
erDiagram
Distribution {
    string conformsTo  
    string format  
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
    AliasPredicate aliasType  
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
DataStructureDefinition {
    boolean evolvingStructure  
    string domain  
    string structure  
    boolean isReferenceData  
    ItemGroupType type  
    stringList children  
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

Distribution ||--|o DataService : "accessService"
Distribution ||--|o Dataset : "isDistributionOf"
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
DataStructureDefinition ||--}o Dimension : "dimensions"
DataStructureDefinition ||--}o Measure : "measures"
DataStructureDefinition ||--}o DataAttribute : "attributes"
DataStructureDefinition ||--|o ComponentList : "grouping"
DataStructureDefinition ||--}o Item : "items"
DataStructureDefinition ||--|o ReifiedConcept : "implementsConcept"
DataStructureDefinition ||--}o WhereClause : "applicableWhen"
DataStructureDefinition ||--}o Coding : "security"
DataStructureDefinition ||--|o Timing : "validityPeriod"
DataStructureDefinition ||--}o Coding : "coding"
DataStructureDefinition ||--}o Comment : "comments"
DataStructureDefinition ||--}o Comment : "siteOrSponsorComments"
Dataflow ||--|| DataStructureDefinition : "structure"
Dataflow ||--}o Dimension : "dimensionConstraint"
Dataflow ||--}o Coding : "coding"
Dataflow ||--}o Comment : "comments"
Dataflow ||--}o Comment : "siteOrSponsorComments"
DataService ||--|o Distribution : "isAccessServiceOf"
DataService ||--}o FormalExpression : "selection"
DataService ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"

```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [accessService](../slots/accessService.md) | 0..1 <br/> [DataService](../classes/DataService.md) | Service that provides access to this distribution | direct |
| [conformsTo](../slots/conformsTo.md) | 0..1 <br/> [String](../types/String.md)&nbsp;or&nbsp;<br />[String](../types/String.md)&nbsp;or&nbsp;<br />[DataStructureDefinition](../classes/DataStructureDefinition.md) | The standard or specification the distribution conforms to | direct |
| [isDistributionOf](../slots/isDistributionOf.md) | 0..1 <br/> [Dataset](../classes/Dataset.md) | Dataset this distribution represents | direct |
| [format](../slots/format.md) | 0..1 <br/> [String](../types/String.md) | File format or serialization used in the distribution | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Dataset](../classes/Dataset.md) | [distribution](../slots/distribution.md) | range | [Distribution](../classes/Distribution.md) |
| [DataService](../classes/DataService.md) | [isAccessServiceOf](../slots/isAccessServiceOf.md) | range | [Distribution](../classes/Distribution.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:Distribution |
| native | odm:Distribution |
| exact | dprod:Distribution, dcat:Distribution |
| narrow | sdmx:JsonDataset, sdmx:CsvDataset, sdmx:StructureSpecificDataset |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Distribution
description: A technical representation that provides a specific format or access
  method for a dataset
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:Distribution
- dcat:Distribution
narrow_mappings:
- sdmx:JsonDataset
- sdmx:CsvDataset
- sdmx:StructureSpecificDataset
attributes:
  accessService:
    name: accessService
    description: Service that provides access to this distribution
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - Distribution
    range: DataService
  conformsTo:
    name: conformsTo
    description: The standard or specification the distribution conforms to
    from_schema: https://cdisc.org/define-json
    domain_of:
    - Dataset
    - Distribution
    any_of:
    - range: string
    - range: DataStructureDefinition
  isDistributionOf:
    name: isDistributionOf
    description: Dataset this distribution represents
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - Distribution
    range: Dataset
  format:
    name: format
    description: File format or serialization used in the distribution
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - Distribution

```
</details>

### Induced

<details>
```yaml
name: Distribution
description: A technical representation that provides a specific format or access
  method for a dataset
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:Distribution
- dcat:Distribution
narrow_mappings:
- sdmx:JsonDataset
- sdmx:CsvDataset
- sdmx:StructureSpecificDataset
attributes:
  accessService:
    name: accessService
    description: Service that provides access to this distribution
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: accessService
    owner: Distribution
    domain_of:
    - Distribution
    range: DataService
  conformsTo:
    name: conformsTo
    description: The standard or specification the distribution conforms to
    from_schema: https://cdisc.org/define-json
    alias: conformsTo
    owner: Distribution
    domain_of:
    - Dataset
    - Distribution
    any_of:
    - range: string
    - range: DataStructureDefinition
  isDistributionOf:
    name: isDistributionOf
    description: Dataset this distribution represents
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: isDistributionOf
    owner: Distribution
    domain_of:
    - Distribution
    range: Dataset
  format:
    name: format
    description: File format or serialization used in the distribution
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: format
    owner: Distribution
    domain_of:
    - Distribution

```
</details>