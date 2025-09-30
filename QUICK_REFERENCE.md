# 🚀 Define-JSON Quick Reference

## 🔄 Convert from Any Directory

### JSON → XML
```bash
PYTHONPATH=/Users/jeremyteoh/Projects/define-json python -c "
from src.define_json.converters.json_to_xml import DefineJSONToXMLConverter
from pathlib import Path
DefineJSONToXMLConverter().convert_file(Path('input.json'), Path('output.xml'))
print('✅ Done!')
"
```

### XML → JSON  
```bash
PYTHONPATH=/Users/jeremyteoh/Projects/define-json python -c "
from src.define_json.converters.xml_to_json import DefineXMLToJSONConverter
from pathlib import Path
DefineXMLToJSONConverter().convert_file(Path('input.xml'), Path('output.json'))
print('✅ Done!')
"
```

### Alternative (sys.path)
```bash
python -c "
import sys
sys.path.append('/Users/jeremyteoh/Projects/define-json')
from src.define_json.converters.json_to_xml import DefineJSONToXMLConverter
from pathlib import Path
DefineJSONToXMLConverter().convert_file(Path('input.json'), Path('output.xml'))
"
```

## 📚 Full Documentation
- **Complete Guide**: [CONVERSION_README.md](CONVERSION_README.md)
- **Project Overview**: [README.md](README.md)
- **Schema Documentation**: [docs/](docs/)

## 🧪 Testing
```bash
# From project directory
make test-roundtrip
make convert
make roundtrip
```
