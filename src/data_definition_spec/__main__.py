"""
Main entry point for data_definition_spec package.

Enables running the package as a module: python -m data_definition_spec
"""

from .utils.cli import main

if __name__ == '__main__':
    import sys
    sys.exit(main())
