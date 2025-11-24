# Standalone Dataset Deconstructor

A fully self-contained dataset analysis tool for deconstructing clinical datasets with **zero external dependencies** beyond pandas.

## Features

✅ **Self-Contained**: No dependencies on shared_utils or other project libraries  
✅ **CDISC-Aware**: Built-in CDISC variable type classification  
✅ **Structure Detection**: Automatically detects vertical vs horizontal datasets  
✅ **Topic Identification**: Finds observation topics and dimensions  
✅ **Specialisation Building**: Creates Define-JSON-like structures  

## What's Included

- **DatasetDeconstructor** (~200 lines) - Main analysis engine
- **TopicDetector** (~450 lines) - Structure and topic detection
- **CDISCVariableClassifier** (~250 lines) - Minimal CDISC classifier
- **SpecialisationBuilder** (~300 lines) - Define-JSON structure builder
- **Supporting models** (~100 lines) - Data structures

**Total:** ~1,300 lines of self-contained Python

## Installation

Simply copy the `standalone/` directory to your project:

```bash
cp -r dataset_deconstructor/standalone/ your_project/dataset_deconstructor/
```

Or use it in place:

```python
import sys
sys.path.insert(0, 'path/to/dataset_deconstructor/standalone')
from dataset_deconstructor import DatasetDeconstructor
```

## Quick Start

### Basic Usage

```python
import pandas as pd
from dataset_deconstructor import DatasetDeconstructor

# Load your dataset
df = pd.read_csv("VS.csv")

# Deconstruct it
deconstructor = DatasetDeconstructor()
breakdown = deconstructor.deconstruct_dataset(df, "VS")

# Inspect results
print(f"Structure: {breakdown.structure.structure_type}")
print(f"Key Dimensions: {breakdown.structure.key_dimensions}")
print(f"Topics: {[t.topic_name for t in breakdown.structure.topics]}")
print(f"Measure Columns: {breakdown.structure.measure_columns}")
```

### Convenience Function

```python
from dataset_deconstructor import deconstruct_dataset

# Quick analysis
result = deconstruct_dataset(df, "VS")
print(result)
# {
#   "structure_type": "vertical",
#   "key_dimensions": ["STUDYID", "USUBJID", "VISITNUM"],
#   "topics": ["SYSBP", "DIABP", "PULSE", "TEMP"],
#   "measure_columns": ["VSORRES", "VSORRESU"]
# }
```

### Full Specialisation Building

```python
from dataset_deconstructor import DatasetDeconstructor, DeconstructionConfig

# Enable full specialisation building
config = DeconstructionConfig(enable_specialisation_building=True)
deconstructor = DatasetDeconstructor(config)

# Get complete Define-JSON-like structure
specialisation = deconstructor.deconstruct_and_build(df, "VS")

print(f"Reified Concepts: {len(specialisation['ReifiedConcepts'])}")
print(f"Item Groups: {len(specialisation['ItemGroups'])}")
print(f"Items: {len(specialisation['Items'])}")
```

## What It Detects

### Structure Types

- **Vertical**: Findings domains (VS, LB, EG) with topic dimension columns (TESTCD, PARAMCD)
- **Horizontal**: Event/demographics domains (DM, AE, CM) with one observation per row

### Column Roles

- **IDENTIFIER**: STUDYID, USUBJID, --SEQ
- **TIMING**: VISITNUM, --DTC, --DY
- **TOPIC**: --TESTCD, --PARAMCD, --DECOD (what is being measured)
- **RESULT**: --ORRES, --STRESN, AVAL (measurement values)
- **ATTRIBUTE**: Everything else (units, methods, categories)

### Examples

#### Vertical Structure (VS - Vital Signs)

```
STUDYID  USUBJID   VISITNUM  VSTESTCD  VSORRES  VSORRESU
STUDY01  SUBJ001   1         SYSBP     120      mmHg
STUDY01  SUBJ001   1         DIABP     80       mmHg
STUDY01  SUBJ001   1         PULSE     72       beats/min
```

Detected:
- Structure: **vertical**
- Topic Dimension: **VSTESTCD**
- Topics: **SYSBP, DIABP, PULSE**
- Key Dimensions: **STUDYID, USUBJID, VISITNUM**
- Measures: **VSORRES**
- Attributes: **VSORRESU**

#### Horizontal Structure (DM - Demographics)

```
STUDYID  USUBJID   AGE  SEX  RACE
STUDY01  SUBJ001   45   M    WHITE
STUDY01  SUBJ002   52   F    BLACK
```

Detected:
- Structure: **horizontal**
- Topics: **AGE, SEX, RACE** (each column is a topic)
- Key Dimensions: **STUDYID, USUBJID**

## Comparison with Full Version

| Feature | Standalone | Full (with shared_utils) |
|---------|-----------|--------------------------|
| Structure Detection | ✅ Full | ✅ Full |
| Topic Detection | ✅ Full | ✅ Full |
| CDISC Classification | ✅ Minimal (5 types) | ✅ Complete (8 types) |
| Pattern Registry | ❌ Inline patterns | ✅ External registry |
| Concept Registry | ❌ Not available | ✅ Full integration |
| Define-JSON I/O | ❌ Not included | ✅ Full handlers |
| Dependencies | 📦 pandas only | 📦 shared_utils + more |

## Testing

Create a simple test:

```python
import pandas as pd
from dataset_deconstructor import DatasetDeconstructor

# Create test data
data = {
    'STUDYID': ['STUDY01'] * 6,
    'USUBJID': ['SUBJ001'] * 3 + ['SUBJ002'] * 3,
    'VISITNUM': [1, 1, 1, 1, 1, 1],
    'VSTESTCD': ['SYSBP', 'DIABP', 'PULSE'] * 2,
    'VSORRES': [120, 80, 72, 118, 78, 70],
    'VSORRESU': ['mmHg'] * 4 + ['beats/min'] * 2
}
df = pd.DataFrame(data)

# Test deconstruction
deconstructor = DatasetDeconstructor()
breakdown = deconstructor.deconstruct_dataset(df, "VS")

# Verify
assert breakdown.structure.structure_type.value == "vertical"
assert breakdown.structure.topic_dimension == "VSTESTCD"
assert len(breakdown.structure.topics) == 3
print("✅ All tests passed!")
```

## Extending

### Add Custom Patterns

```python
from dataset_deconstructor import TopicDetector

detector = TopicDetector()

# Add custom topic patterns
detector.topic_dimension_patterns['custom'] = ['mytest', 'myparam']

# Add custom CDISC patterns
import re
detector.cdisc_topic_patterns['custom_suffix'] = re.compile(r'(\w{2})MYTEST$')
```

### Custom Variable Classification

```python
from dataset_deconstructor import CDISCVariableClassifier

classifier = CDISCVariableClassifier()

# Add custom patterns
classifier.topic_patterns['custom'] = ['myvar', 'customcd']
classifier._compile_patterns()  # Recompile after adding
```

## Architecture

```
standalone/
├── dataset_deconstructor.py    # Main deconstructor class
├── topic_detector.py            # Structure & topic detection
├── variable_classifier.py       # CDISC variable classification
├── specialisation_builder.py    # Define-JSON structure building
├── models.py                    # Data models
├── column_analyzer.py           # Column analysis
├── __init__.py                  # Package exports
└── README.md                    # This file
```

## Limitations

1. **No Concept Registry**: Cannot look up concepts from CDISC Library or NCI Thesaurus
2. **No JSON I/O**: Doesn't include Define-JSON/Dataset-JSON read/write
3. **Simplified Patterns**: Uses inline patterns instead of external registry
4. **Basic Classification**: Only 5 variable types vs 8 in full version

For full functionality, use the integrated version with `shared_utils`.

## When to Use Standalone

✅ **Use standalone when:**
- You need zero dependencies beyond pandas
- Working in restricted/air-gapped environments
- Building a simple prototype
- Don't need concept registry integration
- Want to understand the core algorithm

❌ **Use full version when:**
- You need complete CDISC Library integration
- Want concept registry lookup and enhancement
- Need Define-JSON/Dataset-JSON I/O
- Building production regulatory submissions
- Want the full pattern registry

## License

Same as parent project.

## Support

This is a self-contained extraction. For updates, regenerate from the main project.

