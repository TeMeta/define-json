# Enum: TimingLandmark 




_Well-known protocol reference points that a Timing can be expressed relative to. Corresponds to USDM TimingRelativeToLandmark. For visit-specific anchors not covered by this enum, use a USDM ScheduledActivityInstance OID reference in Timing.relativeTo as a free string._



URI: [dds:enum/TimingLandmark](https://w3id.org/dds/enum/TimingLandmark)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| INFORMED_CONSENT | None | Date of informed consent |
| SCREENING | None | Start of screening period |
| RANDOMIZATION | usdm:Randomization | Date of randomisation |
| FIRST_DOSE | usdm:FirstDose | Date of first study drug administration |
| LAST_DOSE | usdm:LastDose | Date of last study drug administration |
| CYCLE_START | usdm:CycleStart | Start of the current treatment cycle |
| END_OF_TREATMENT | usdm:EndOfTreatment | Date treatment was completed or discontinued |
| PROCEDURE_DATE | None | Date of a specified procedure |
| DIAGNOSIS_DATE | None | Date of the index diagnosis |








## Identifier and Mapping Information






### Schema Source


* from schema: https://w3id.org/dds






## LinkML Source

<details>
```yaml
name: TimingLandmark
description: Well-known protocol reference points that a Timing can be expressed relative
  to. Corresponds to USDM TimingRelativeToLandmark. For visit-specific anchors not
  covered by this enum, use a USDM ScheduledActivityInstance OID reference in Timing.relativeTo
  as a free string.
from_schema: https://w3id.org/dds
exact_mappings:
- usdm:TimingRelativeToLandmark
rank: 1000
permissible_values:
  INFORMED_CONSENT:
    text: INFORMED_CONSENT
    description: Date of informed consent
  SCREENING:
    text: SCREENING
    description: Start of screening period
  RANDOMIZATION:
    text: RANDOMIZATION
    description: Date of randomisation
    meaning: usdm:Randomization
  FIRST_DOSE:
    text: FIRST_DOSE
    description: Date of first study drug administration
    meaning: usdm:FirstDose
  LAST_DOSE:
    text: LAST_DOSE
    description: Date of last study drug administration
    meaning: usdm:LastDose
  CYCLE_START:
    text: CYCLE_START
    description: Start of the current treatment cycle
    meaning: usdm:CycleStart
  END_OF_TREATMENT:
    text: END_OF_TREATMENT
    description: Date treatment was completed or discontinued
    meaning: usdm:EndOfTreatment
  PROCEDURE_DATE:
    text: PROCEDURE_DATE
    description: Date of a specified procedure
  DIAGNOSIS_DATE:
    text: DIAGNOSIS_DATE
    description: Date of the index diagnosis

```
</details>