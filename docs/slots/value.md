

# Slot: value 



URI: [dds:slot/value](https://w3id.org/dds/slot/value)
Alias: value

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Translation](../classes/Translation.md) | A text representation that provides content in a specific language, used for multilingual support |  no  |
| [Parameter](../classes/Parameter.md) | A variable element that describes an input used in a formal expression |  no  |
| [Timing](../classes/Timing.md) | A temporal element that describes the timing of an event or occurrence, which can be absolute, relative, or nominal |  no  |






## Properties

* Range: [String](../types/String.md)




## Identifier and Mapping Information







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dds:value |
| native | dds:value |




## LinkML Source

<details>
```yaml
name: value
alias: value
domain_of:
- Translation
- Parameter
- Timing
range: string

```
</details>