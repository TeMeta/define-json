"""
Main entry point for define_json package.

Enables running the package as a module: python -m define_json
"""

from .utils.cli import main

if __name__ == '__main__':
    import sys
    sys.exit(main())
