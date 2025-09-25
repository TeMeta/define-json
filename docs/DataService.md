

# Class: DataService 


_A service element that provides an API or endpoint for serving or receiving data_





URI: [odm:DataService](https://cdisc.org/odm2/DataService)



```mermaid
erDiagram
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
Coding {
    string code  
    string decode  
    string codeSystem  
    string codeSystemVersion  
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
Resource {
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
ReturnValue {
    DataType dataType  
    stringList valueList  
    string OID  
    string uuid  
    string name  
    string description  
    string label  
    stringList aliases  
}
Parameter {
    DataType dataType  
    string value  
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

DataService ||--|o Distribution : "isAccessServiceOf"
DataService ||--}o FormalExpression : "selection"
DataService ||--}o Coding : "coding"
FormalExpression ||--}o Parameter : "parameters"
FormalExpression ||--|o ReturnValue : "returnValue"
FormalExpression ||--}o Resource : "externalCodeLibs"
FormalExpression ||--}o Coding : "coding"
Resource ||--}o FormalExpression : "selection"
Resource ||--}o Coding : "coding"
ReturnValue ||--}o Coding : "coding"
Parameter ||--}o CodeList : "codeList"
Parameter ||--}o Item : "items"
Parameter ||--}o ConceptProperty : "conceptProperty"
Parameter ||--}o Coding : "coding"
Distribution ||--|o DataService : "accessService"
Distribution ||--|o Dataset : "isDistributionOf"
Dataset ||--|o Dataflow : "describedBy"
Dataset ||--|o DataStructureDefinition : "structuredBy"
Dataset ||--}o Distribution : "distribution"
Dataset ||--}o Coding : "security"
Dataset ||--|o Timing : "validityPeriod"
Dataset ||--}o Coding : "coding"

```




## Inheritance
* [IdentifiableElement](IdentifiableElement.md) [ [Identifiable](Identifiable.md) [Labelled](Labelled.md)]
    * [Resource](Resource.md) [ [Versioned](Versioned.md)]
        * **DataService**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [isAccessServiceOf](isAccessServiceOf.md) | 0..1 <br/> [Distribution](Distribution.md) | Distribution(s) for which this service provides access | direct |
| [protocol](protocol.md) | 0..1 <br/> [String](String.md) | Protocol used by the service (e | direct |
| [securitySchemaType](securitySchemaType.md) | 0..1 <br/> [String](String.md) | Security or authentication method used (e | direct |
| [resourceType](resourceType.md) | 0..1 <br/> [String](String.md) | Type of resource (e | [Resource](Resource.md) |
| [attribute](attribute.md) | 0..1 <br/> [String](String.md) | Field provided by the Name attribute where the data or information can be obt... | [Resource](Resource.md) |
| [selection](selection.md) | * <br/> [FormalExpression](FormalExpression.md) | Machine-executable instructions for selecting data from the resource | [Resource](Resource.md) |
| [version](version.md) | 0..1 <br/> [String](String.md) | The version of the external resources | [Versioned](Versioned.md) |
| [href](href.md) | 0..1 <br/> [String](String.md) | Machine-readable instructions to obtain the resource e | [Versioned](Versioned.md) |
| [OID](OID.md) | 1 <br/> [String](String.md) | Local identifier within this study/context | [Identifiable](Identifiable.md) |
| [uuid](uuid.md) | 0..1 <br/> [String](String.md) | Universal unique identifier | [Identifiable](Identifiable.md) |
| [name](name.md) | 0..1 <br/> [String](String.md) | Short name or identifier, used for field names | [Labelled](Labelled.md) |
| [description](description.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Detailed description, shown in tooltips | [Labelled](Labelled.md) |
| [coding](coding.md) | * <br/> [Coding](Coding.md) | Semantic tags for this element | [Labelled](Labelled.md) |
| [label](label.md) | 0..1 <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Human-readable label, shown in UIs | [Labelled](Labelled.md) |
| [aliases](aliases.md) | * <br/> [String](String.md)&nbsp;or&nbsp;<br />[String](String.md)&nbsp;or&nbsp;<br />[TranslatedText](TranslatedText.md) | Alternative name or identifier | [Labelled](Labelled.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [DataProduct](DataProduct.md) | [inputPort](inputPort.md) | range | [DataService](DataService.md) |
| [DataProduct](DataProduct.md) | [outputPort](outputPort.md) | range | [DataService](DataService.md) |
| [Distribution](Distribution.md) | [accessService](accessService.md) | range | [DataService](DataService.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://cdisc.org/define-json




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | odm:DataService |
| native | odm:DataService |
| exact | dprod:DataService, dcat:DataService |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DataService
description: A service element that provides an API or endpoint for serving or receiving
  data
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:DataService
- dcat:DataService
is_a: Resource
attributes:
  isAccessServiceOf:
    name: isAccessServiceOf
    description: Distribution(s) for which this service provides access
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataService
    range: Distribution
  protocol:
    name: protocol
    description: Protocol used by the service (e.g., HTTPS, FTP)
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataService
  securitySchemaType:
    name: securitySchemaType
    description: Security or authentication method used (e.g., OAuth2)
    from_schema: https://cdisc.org/define-json
    rank: 1000
    domain_of:
    - DataService

```
</details>

### Induced

<details>
```yaml
name: DataService
description: A service element that provides an API or endpoint for serving or receiving
  data
from_schema: https://cdisc.org/define-json
exact_mappings:
- dprod:DataService
- dcat:DataService
is_a: Resource
attributes:
  isAccessServiceOf:
    name: isAccessServiceOf
    description: Distribution(s) for which this service provides access
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: isAccessServiceOf
    owner: DataService
    domain_of:
    - DataService
    range: Distribution
  protocol:
    name: protocol
    description: Protocol used by the service (e.g., HTTPS, FTP)
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: protocol
    owner: DataService
    domain_of:
    - DataService
  securitySchemaType:
    name: securitySchemaType
    description: Security or authentication method used (e.g., OAuth2)
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: securitySchemaType
    owner: DataService
    domain_of:
    - DataService
  resourceType:
    name: resourceType
    description: Type of resource (e.g.,  "ODM", "HL7-FHIR", "HL7-CDA", "HL7-v2",
      "OpenEHR-extract")
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: resourceType
    owner: DataService
    domain_of:
    - Resource
    range: string
    required: false
  attribute:
    name: attribute
    description: Field provided by the Name attribute where the data or information
      can be obtained. Examples are "valueQuantity.value" or "valueQuantity.unit".
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: attribute
    owner: DataService
    domain_of:
    - Resource
    - MeasureRelationship
    - DataflowRelationship
    - GroupRelationship
    - DimensionRelationship
    - ObservationRelationship
    range: string
  selection:
    name: selection
    description: Machine-executable instructions for selecting data from the resource.
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: selection
    owner: DataService
    domain_of:
    - Resource
    range: FormalExpression
    multivalued: true
    inlined: true
    inlined_as_list: true
  version:
    name: version
    description: The version of the external resources
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: version
    owner: DataService
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
    owner: DataService
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
    owner: DataService
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
    owner: DataService
    domain_of:
    - Identifiable
    range: string
  name:
    name: name
    description: Short name or identifier, used for field names
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: name
    owner: DataService
    domain_of:
    - Labelled
    range: string
  description:
    name: description
    description: Detailed description, shown in tooltips
    from_schema: https://cdisc.org/define-json
    rank: 1000
    alias: description
    owner: DataService
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
    owner: DataService
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
    owner: DataService
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
    owner: DataService
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

```
</details>