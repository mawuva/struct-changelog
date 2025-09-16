## v0.2.0 (2025-09-16)

### Feat

- Add examples for ChangeLogManager usage - Introduced multiple example scripts demonstrating various use cases of ChangeLogManager, including basic usage, nested structures, lists and arrays, manual tracking, and custom objects. - Created a README.md file to provide an overview of the examples and instructions for execution. - Removed 'examples/' from .gitignore to allow tracking of example files.
- Implement ChangeLogManager and helper utilities for change tracking - Added ChangeLogManager for tracking changes in nested data structures - Introduced helper functions and a ChangeTracker class for easier usage - Defined ChangeActions enum and ChangeLogEntry dataclass for structured change records

### Refactor

- Clean up imports and enhance type hints in changelog module - Streamlined import statements in __init__.py for better readability. - Improved type hints in helpers.py and manager.py for better clarity and type checking. - Removed unnecessary blank lines to enhance code cleanliness.
