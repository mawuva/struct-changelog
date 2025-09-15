# Struct Changelog

[![CI](https://github.com/mawuva/struct-changelog/actions/workflows/ci.yml/badge.svg)](https://github.com/mawuva/struct-changelog/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/struct-changelog.svg)](https://pypi.org/project/struct-changelog/)
[![Python Version](https://img.shields.io/pypi/pyversions/struct-changelog.svg)](https://pypi.org/project/struct-changelog/)
[![License](https://img.shields.io/pypi/l/struct-changelog.svg)](https://pypi.org/project/struct-changelog/)

Tracks changes in nested Python structures (dicts, lists, tuples, and objects with __dict__).

## Installation

```bash
pip install struct-changelog
```

## Quick Start

### Basic Usage

```python
from struct_changelog import ChangeLogManager

# Create a changelog manager
changelog = ChangeLogManager()

# Your data
data = {"user": {"name": "John", "age": 30}}

# Track changes
with changelog.capture(data) as d:
    d["user"]["name"] = "Jane"
    d["user"]["age"] = 31
    d["user"]["email"] = "jane@example.com"

# View changes
for entry in changelog.get_entries():
    print(f"{entry['action']}: {entry['key_path']} = {entry['new_value']}")
```

### Helper Approaches

To avoid manually creating `ChangeLogManager` instances, you can use these helper approaches:

#### 1. Context Manager Global (Recommended for simple use)

```python
from struct_changelog import track_changes

data = {"config": {"debug": False}}

# Most concise approach
with track_changes(data) as (changelog, tracked_data):
    tracked_data["config"]["debug"] = True
    tracked_data["config"]["version"] = "2.0"

print(changelog.get_entries())
```

#### 2. Factory Function

```python
from struct_changelog import create_changelog

# More explicit than the original approach
changelog = create_changelog()
data = {"settings": {"theme": "light"}}

with changelog.capture(data) as d:
    d["settings"]["theme"] = "dark"
```

#### 3. ChangeTracker Class (For stateful tracking)

```python
from struct_changelog import ChangeTracker

# Object-oriented approach - useful for maintaining state
tracker = ChangeTracker()

data = {"session": {"user_id": 123}}

# Track changes
with tracker.track(data) as d:
    d["session"]["user_id"] = 456
    d["session"]["active"] = True

# Access entries
print(tracker.entries)

# Add manual entries
tracker.add(ChangeActions.ADDED, "session.notes", new_value="User logged in")

# Reset when needed
tracker.reset()
```

## Features

- **Automatic Change Detection**: Captures ADDED, EDITED, and REMOVED changes
- **Nested Structure Support**: Works with dicts, lists, tuples, and custom objects
- **JSON Serializable**: All entries can be serialized to JSON
- **Multiple Usage Patterns**: Choose the approach that fits your needs
- **Thread Safe**: Safe to use in multi-threaded environments
- **Zero Dependencies**: Pure Python implementation

## Change Types

- `ADDED`: New items added to the structure
- `EDITED`: Existing items modified
- `REMOVED`: Items removed from the structure

## Examples

See the `examples/` directory for comprehensive usage examples:

- `basic_usage.py` - Basic dictionary tracking
- `nested_structures.py` - Complex nested structures
- `lists_arrays.py` - List and array modifications
- `objects.py` - Custom object tracking
- `manual_tracking.py` - Manual entry addition
- `helper_approaches.py` - All helper approaches compared

## API Reference

### ChangeLogManager

The core class for tracking changes.

```python
changelog = ChangeLogManager()
with changelog.capture(data) as tracked_data:
    # Modify tracked_data
    pass
```

### Helper Functions

- `create_changelog()` - Factory function for creating managers
- `track_changes(data)` - Context manager that creates and manages a changelog
- `ChangeTracker` - Wrapper class for object-oriented usage

## Why Not Use a Global Singleton?

While a global singleton might seem convenient, it has several drawbacks:

- **Shared State**: All users share the same changelog state
- **Testing Issues**: Tests can interfere with each other
- **Thread Safety**: Requires careful synchronization
- **Coupling**: Makes code harder to maintain and test

The helper approaches provide convenience without these issues.

## License

MIT License - see LICENSE file for details.