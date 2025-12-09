# Define-JSON Testing, Validation and Conversion Makefile

.PHONY: help install test validate lint clean check-syntax linkml-lint generate-json-schema generate-pydantic docs docs-serve docs-build docs-deploy demo roundtrip convert test-roundtrip format setup test-xml-roundtrip-360i test-xml-roundtrip-LZZT test-xml-roundtrip-v21-adam test-xml-roundtrip-v21-sdtm test-xml-roundtrips reverse-engineer reverse-engineer-lb reverse-engineer-vs

help:
	@echo "Define-JSON Testing, Validation and Conversion"
	@echo "=============================================="
	@echo ""
	@echo "Main targets:"
	@echo "  demo                       - Run complete XML<->JSON conversion demo"
	@echo "  roundtrip                  - Test XML->JSON->XML roundtrip conversion"
	@echo "  convert                    - Convert sample XML to JSON"
	@echo ""
	@echo "Reverse Engineering:"
	@echo "  reverse-engineer           - Reverse engineer Define-JSON from Dataset-JSON"
	@echo "  reverse-engineer-lb        - Run reverse engineering on LB sample"
	@echo "  reverse-engineer-vs        - Run reverse engineering on VS sample"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  install                    - Install all dependencies via Poetry"
	@echo "  test                       - Run all tests (unit, CLI, schema, roundtrip)"
	@echo "  validate                   - Validate YAML schema structure"
	@echo "  lint                       - Lint YAML file for style issues"
	@echo "  linkml-lint                - Run LinkML schema linter"
	@echo "  check-syntax               - Check YAML syntax"
	@echo ""
	@echo "Roundtrip Tests:"
	@echo "  test-xml-roundtrips        - Run all XML roundtrip tests"
	@echo "  test-xml-roundtrip-360i    - Test define-360i.xml roundtrip"
	@echo "  test-xml-roundtrip-LZZT    - Test define_LZZT_ADaM.xml roundtrip"
	@echo "  test-xml-roundtrip-v21-adam - Test defineV21-ADaM.xml roundtrip"
	@echo "  test-xml-roundtrip-v21-sdtm - Test defineV21-SDTM.xml roundtrip"
	@echo ""
	@echo "Documentation:"
	@echo "  docs                       - Generate LinkML documentation"
	@echo "  docs-serve                 - Serve documentation with MkDocs"
	@echo "  docs-build                 - Build static documentation site"
	@echo "  docs-deploy                - Deploy docs to GitHub Pages"
	@echo ""
	@echo "Generators:"
	@echo "  generate-json-schema       - Generate JSON Schema from LinkML"
	@echo "  generate-pydantic          - Generate Pydantic models from LinkML"
	@echo "  clean                      - Clean up generated files"

install:
	@echo "Installing dependencies with Poetry..."
	poetry install
	@echo "Dependencies installed successfully"

check-syntax:
	@echo "Checking YAML syntax..."
	poetry run python -c "import yaml; yaml.safe_load(open('define.yaml'))"
	@echo "YAML syntax is valid"

validate:
	@echo "Validating LinkML schema structure..."
	poetry run python -c "from linkml_runtime import SchemaView; sv = SchemaView('define.yaml'); print('Schema loaded successfully')"
	@echo "LinkML schema validation passed"

lint:
	@echo "Linting YAML file..."
	poetry run yamllint define.yaml || echo "YAML linting issues found (yamllint)"

linkml-lint:
	@echo "Running LinkML schema linter..."
	poetry run linkml-lint define.yaml || echo "LinkML linting issues found (non-blocking)"
	@echo "LinkML linting complete"

generate-json-schema:
	@echo "Generating JSON Schema from LinkML..."
	poetry run linkml generate json-schema define.yaml > generated/define-json-schema.json
	@echo "JSON Schema generated: generated/define-json-schema.json"

generate-pydantic:
	@echo "Generating Pydantic models from LinkML..."
	poetry run linkml generate pydantic --meta auto define.yaml > generated/define.py
	@echo "Pydantic models generated: generated/define.py"
# Main functionality targets
demo:
	@echo "Running complete XML<->JSON conversion demo..."
	poetry run python demo.py

roundtrip:
	@echo "Testing XML→JSON→XML roundtrip conversion..."
	poetry run python -m src.define_json test-roundtrip data/define-360i.xml

convert:
	@echo "Converting sample XML to JSON..."
	poetry run python -m src.define_json xml2json data/define-360i.xml data/define-360i.json

# Testing targets
test: check-syntax validate linkml-lint
	@echo "Running unit tests..."
	poetry run python -m unittest discover tests/ -v
roundtrip; from pathlib import Path; result = validate_true_roundtrip(Path('data/define-360i.xml'), Path('data/define-360i-recreated.xml')); print('Roundtrip test passed' if result.get('passed') else 'Roundtrip test failed')"

test-xml-roundtrip-LZZT:
	@echo "Testing XML→JSON→XML roundtrip conversion for define_LZZT_ADaM..."
	poetry run python -m src.define_json xml2json data/define_LZZT_ADaM.xml data/define_LZZT_ADaM.json --preserve-original
	poetry run python -m src.define_json json2xml data/define_LZZT_ADaM.json data/define_LZZT_ADaM_roundtrip.xml --strict-mode
	poetry run python -m scripts.compare_xml_roundtrip data/define_LZZT_ADaM.xml data/define_LZZT_ADaM_roundtrip.xml --validate-only --ignore-order-numbers

test-xml-roundtrip-360i:
	@echo "Testing XML→JSON→XML roundtrip conversion for define-360i..."
	poetry run python -m src.define_json xml2json data/define-360i.xml data/define-360i.json --preserve-original
	poetry run python -m src.define_json json2xml data/define-360i.json data/define-360i_roundtrip.xml --strict-mode
	poetry run python -m scripts.compare_xml_roundtrip data/define-360i.xml data/define-360i_roundtrip.xml --validate-only --ignore-order-numbers

test-xml-roundtrip-v21-adam:
	@echo "Testing XML→JSON→XML roundtrip conversion for defineV21-ADaM..."
	poetry run python -m src.define_json xml2json data/defineV21-ADaM.xml data/defineV21-ADaM.json --preserve-original
	poetry run python -m src.define_json json2xml data/defineV21-ADaM.json data/defineV21-ADaM_roundtrip.xml --strict-mode
	poetry run python -m scripts.compare_xml_roundtrip data/defineV21-ADaM.xml data/defineV21-ADaM_roundtrip.xml --validate-only --ignore-order-numbers

test-xml-roundtrip-v21-sdtm:
	@echo "Testing XML→JSON→XML roundtrip conversion for defineV21-SDTM..."
	poetry run python -m src.define_json xml2json data/defineV21-SDTM.xml data/defineV21-SDTM.json --preserve-original
	poetry run python -m src.define_json json2xml data/defineV21-SDTM.json data/defineV21-SDTM_roundtrip.xml --strict-mode
	poetry run python -m scripts.compare_xml_roundtrip data/defineV21-SDTM.xml data/defineV21-SDTM_roundtrip.xml --validate-only --ignore-order-numbers

test-xml-roundtrips: test-xml-roundtrip-360i test-xml-roundtrip-LZZT test-xml-roundtrip-v21-adam test-xml-roundtrip-v21-sdtm
	@echo "All XML roundtrip tests completed"

# Documentation generation (suppress gen-doc warnings)
docs:
	@echo "Generating LinkML documentation..."
	mkdir -p docs/js docs/classes docs/enums docs/slots docs/types docs/schemas;
	cp versioning_architecture.md docs/Versioning.md;
	cp README.md docs/About.md;
	cp src/js/* docs/js/;
	cp CONVERSION_README.md docs/CONVERSION_README.md;
	cp QUICK_REFERENCE.md docs/QUICK_REFERENCE.md;
	poetry run gen-doc define.yaml --directory docs/ --subfolder-type-separation --hierarchical-class-view --diagram-type er_diagram \
	--sort-by rank --include-top-level-diagram --truncate-descriptions false

docs-serve:
	@echo "Serving documentation with MkDocs..."
	poetry run mkdocs serve

docs-build:
	@echo "Building static documentation site with MkDocs..."
	poetry run mkdocs build

docs-deploy:
	@echo "Deploying documentation to GitHub Pages..."
	poetry run mkdocs gh-deploy

clean:
	@echo "Cleaning up generated files..."
	rm -rf docs/*
	rm -rf generated/*
	rm -rf __pycache__/ src/**/__pycache__/
	rm -rf .pytest_cache/
	rm -f data/test*.json data/test*.xml data/converted*.json data/makefile-roundtrip.*
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	@echo "Cleanup complete"

# Development helpers
format:
	@echo "Formatting Python code..."
	poetry run black src/ tests/ *.py --line-length 100
	@echo "Code formatting complete"

setup: install
	@echo "Setting up development environment..."
	@mkdir -p data generated
	@echo "Development environment ready"

# Reverse Engineering targets
reverse-engineer:
	@echo "Reverse engineering Define-JSON from Dataset-JSON..."
	@echo "Usage: make reverse-engineer-lb or make reverse-engineer-vs"
	@echo "Or run directly: python scripts/reverse_engineer_define.py <dataset-json-file>"

reverse-engineer-lb:
	@echo "Reverse engineering LB (Laboratory) dataset..."
	python scripts/reverse_engineer_define.py \
		examples/sample_dataset_lb.json \
		--output-dir test_outputs/reverse_lb \
		--domain LB
	@echo ""
	@echo "✅ Reverse engineering complete!"
	@echo "📁 Outputs in: test_outputs/reverse_lb/"
	@echo "   - define_metadata.json"
	@echo "   - data_cube_config_suggestion.yaml"
	@echo "   - reverse_engineering_report.md"

reverse-engineer-vs:
	@echo "Reverse engineering VS (Vital Signs) dataset..."
	python scripts/reverse_engineer_define.py \
		examples/sample_dataset_vs.json \
		--output-dir test_outputs/reverse_vs \
		--domain VS
	@echo ""
	@echo "✅ Reverse engineering complete!"
	@echo "📁 Outputs in: test_outputs/reverse_vs/"
	@echo "   - define_metadata.json"
	@echo "   - data_cube_config_suggestion.yaml"
	@echo "   - reverse_engineering_report.md"
# Generate all together, stop if any fail
generate-all: validate clean docs docs-build docs-deploy generate-json-schema generate-pydantic
	@echo "All generators complete"
