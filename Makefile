# Define-JSON Testing and Validation Makefile (Poetry-native)

.PHONY: help install test validate lint clean format check-syntax generate-docs notebook quick dev linkml-lint generate-json-schema generate-pydantic docs-serve docs-build

help:
	@echo "Define-JSON Testing and Validation (Poetry)"
	@echo "============================================"
	@echo ""
	@echo "Available targets:"
	@echo "  install              - Install all dependencies via Poetry"
	@echo "  test                 - Run all tests (unit, CLI, schema)"
	@echo "  validate             - Validate YAML schema structure"
	@echo "  lint                 - Lint YAML file for style issues"
	@echo "  linkml-lint          - Run LinkML schema linter"
	@echo "  format               - Format YAML file (manual step)"
	@echo "  check-syntax         - Check YAML syntax"
	@echo "  generate-json-schema - Generate JSON Schema from LinkML"
	@echo "  generate-pydantic    - Generate Pydantic models from LinkML"
	@echo "  clean                - Clean up generated files"
	@echo "  notebook             - Start Jupyter notebook server"
	@echo "  quick                - Quick CLI validation"
	@echo "  dev                  - Quick validation for development"
	@echo "  docs-serve           - Serve documentation with MkDocs"
	@echo "  docs-build           - Build static documentation site"

install:
	@echo "Installing dependencies with Poetry..."
	poetry install
	@echo "Dependencies installed successfully"

check-syntax:
	@echo "Checking YAML syntax..."
	poetry run python -c "import yaml; yaml.safe_load(open('define-json.yaml'))"
	@echo "✓ YAML syntax is valid"

validate:
	@echo "Validating LinkML schema structure..."
	poetry run python -c "from linkml_runtime import SchemaView; sv = SchemaView('define-json.yaml'); print('✓ Schema loaded successfully')"
	@echo "✓ LinkML schema validation passed"

lint:
	@echo "Linting YAML file..."
	poetry run yamllint define-json.yaml || echo "⚠ YAML linting issues found (yamllint)"

linkml-lint:
	@echo "Running LinkML schema linter..."
	poetry run linkml-lint define-json.yaml || echo "⚠ LinkML linting issues found (non-blocking)"
	@echo "✓ LinkML linting complete"

format:
	@echo "Formatting YAML file..."
	@echo "(No automatic YAML formatter configured. Use yamlfmt or similar if desired.)"
	@echo "YAML formatting complete"

generate-json-schema:
	@echo "Generating JSON Schema from LinkML..."
	poetry run linkml generate json-schema define-json.yaml > generated/json-schema.json
	@echo "✓ JSON Schema generated: generated/json-schema.json"

generate-pydantic:
	@echo "Generating Pydantic models from LinkML..."
	poetry run linkml generate pydantic --meta AUTO define-json.yaml > generated/pydantic_models.py
	@echo "✓ Pydantic models generated: generated/pydantic_models.py"

test: check-syntax validate linkml-lint
	@echo "Running unit tests..."
	poetry run python -m unittest tests.test_schema
	@echo "Running CLI validation..."
	poetry run python validate_schema.py
	@echo "✓ All tests passed"

notebook:
	@echo "Starting Jupyter notebook server..."
	poetry run jupyter notebook

docs-serve:
	@echo "Serving documentation with MkDocs..."
	poetry run mkdocs serve

docs-build:
	@echo "Building static documentation site with MkDocs..."
	poetry run mkdocs build

clean:
	@echo "Cleaning up generated files..."
	rm -rf docs/
	rm -rf generated/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	@echo "✓ Cleanup complete"

dev: check-syntax validate linkml-lint
	@echo "✓ Development validation complete"

quick: install
	@echo "Running quick CLI validation..."
	poetry run python validate_schema.py
	@echo "✓ Quick validation complete"

