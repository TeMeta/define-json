# 🚀 Define-JSON Quick Reference

## Installation

This project uses **Poetry** for Python dependency and environment management.

To install poetry:
```bash
# Recommended official installer (works on Linux, macOS, and WSL)
curl -sSL https://install.python-poetry.org | python3 -

# On Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -3 -
```

After installation, restart your shell or run

```bash
export PATH="$HOME/.local/bin:$PATH"    # Linux/macOS/WSL
# or add it permanently to ~/.bashrc, ~/.zshrc, etc.
```

verify it worked (`poetry --version`) then clone this repo and install everything

```bash
git clone https://github.com/TeMeta/define-json.git
cd define-json
make setup
```


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

## Updating the model, refreshing schemas

1. make your updates and run `make generate-all` to update everything
2. new schemas are created in `/generated` folder for review
3. to avoid accidental overwrites, copy schemas manually once approved to `src/define_json/schema`
4. update the conversion tooling to handle any breaking changes
