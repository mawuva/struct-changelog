# Struct Changelog

[![CI](https://github.com/mawuva/struct-changelog/actions/workflows/ci.yml/badge.svg)](https://github.com/mawuva/struct-changelog/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/struct-changelog.svg)](https://pypi.org/project/struct-changelog/)
[![Python Version](https://img.shields.io/pypi/pyversions/struct-changelog.svg)](https://pypi.org/project/struct-changelog/)
![GitHub License](https://img.shields.io/github/license/mawuva/struct-changelog)


## What is Struct Changelog?

**Struct Changelog** is a Python library that automatically tracks and records changes made to nested data structures in real-time. It provides a comprehensive audit trail for modifications to dictionaries, lists, tuples, and custom objects, making it invaluable for debugging, data validation, and maintaining data integrity.

### What does it do?

- **🔍 Automatic Change Detection**: Captures every modification (additions, edits, deletions) in your data structures
- **📊 Detailed Audit Trail**: Records what changed, where it changed, and what the old/new values were
- **🌐 Nested Structure Support**: Works seamlessly with complex nested data (dicts, lists, objects)
- **📝 JSON Serializable**: All change records can be exported to JSON for logging or persistence
- **🔄 Multiple Usage Patterns**: Choose from simple context managers to full object-oriented approaches

### Why is it useful?

**For Debugging & Development:**
- Track exactly what changes during complex data transformations
- Identify unexpected modifications in your data pipeline
- Debug data corruption issues by seeing the sequence of changes

**For Data Validation & Integrity:**
- Ensure data modifications follow expected patterns
- Validate business rules by analyzing change patterns
- Maintain data consistency across complex operations

**For Auditing & Compliance:**
- Create detailed logs of all data modifications
- Track user actions and system changes
- Meet regulatory requirements for data change tracking

**For Testing & Quality Assurance:**
- Verify that your code modifies data as expected
- Create comprehensive test assertions about data changes
- Debug test failures by seeing exactly what changed

### Real-world Use Cases:

- **API Development**: Track changes to request/response data for debugging
- **Data Processing**: Monitor transformations in ETL pipelines
- **Configuration Management**: Track changes to application settings
- **User Interface**: Monitor state changes in complex UI components
- **Database Operations**: Track changes before committing to database
- **Machine Learning**: Monitor data preprocessing and feature engineering steps

## How it works

Struct Changelog uses Python's context manager protocol and object introspection to automatically detect changes:

1. **Context Manager**: When you use `with changelog.capture(data)`, it creates a proxy object that wraps your original data
2. **Change Detection**: Every modification (assignment, deletion, list operations) is intercepted and recorded
3. **Deep Tracking**: The system recursively tracks changes in nested structures (dicts, lists, objects)
4. **Change Recording**: Each change is recorded with:
   - **Action**: ADDED, EDITED, or REMOVED
   - **Key Path**: The location of the change (e.g., "user.profile.email")
   - **Old Value**: The original value before the change
   - **New Value**: The new value after the change
   - **Timestamp**: When the change occurred

5. **Circular Reference Protection**: Automatically handles circular references to prevent infinite loops
6. **Thread Safety**: Safe to use in multi-threaded environments

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

- **🔍 Automatic Change Detection**: Captures ADDED, EDITED, and REMOVED changes
- **🌐 Nested Structure Support**: Works with dicts, lists, tuples, and custom objects
- **📝 JSON Serializable**: All entries can be serialized to JSON
- **🔄 Multiple Usage Patterns**: Choose the approach that fits your needs
- **🧵 Thread Safe**: Safe to use in multi-threaded environments
- **📦 Zero Dependencies**: Pure Python implementation
- **🛡️ Circular Reference Protection**: Handles complex data structures safely
- **⚡ High Performance**: Minimal overhead, optimized for production use
- **🔧 Flexible API**: Multiple ways to use the library based on your needs

## Change Types

- `ADDED`: New items added to the structure
- `EDITED`: Existing items modified
- `REMOVED`: Items removed from the structure

## Examples

### Example 1: API Request/Response Tracking

```python
from struct_changelog import track_changes

# Track changes to API request data
request_data = {
    "user": {"id": 123, "name": "John"},
    "settings": {"theme": "light", "notifications": True}
}

with track_changes(request_data) as (changelog, data):
    # Simulate API processing
    data["user"]["name"] = "Jane"
    data["user"]["email"] = "jane@example.com"
    data["settings"]["theme"] = "dark"
    data["settings"]["language"] = "fr"
    data["timestamp"] = "2024-01-16T10:30:00Z"

# Log all changes for debugging
for entry in changelog.get_entries():
    print(f"API Change: {entry['action']} {entry['key_path']} = {entry['new_value']}")
```

### Example 2: Data Pipeline Monitoring

```python
from struct_changelog import ChangeTracker

# Track data transformations in ETL pipeline
tracker = ChangeTracker()
raw_data = {"users": [], "metadata": {"source": "csv"}}

with tracker.track(raw_data) as data:
    # Data cleaning
    data["users"] = [
        {"id": 1, "name": "John", "email": "john@example.com"},
        {"id": 2, "name": "Jane", "email": "jane@example.com"}
    ]
    
    # Data enrichment
    for user in data["users"]:
        user["status"] = "active"
        user["created_at"] = "2024-01-16"
    
    # Metadata updates
    data["metadata"]["processed_at"] = "2024-01-16T10:30:00Z"
    data["metadata"]["record_count"] = len(data["users"])

# Export changes for audit
print(tracker.to_json(indent=2))
```

### Example 3: Configuration Management

```python
from struct_changelog import create_changelog

# Track configuration changes
config = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"enabled": True, "ttl": 3600},
    "features": {"new_ui": False}
}

changelog = create_changelog()

with changelog.capture(config) as cfg:
    # Environment-specific changes
    cfg["database"]["host"] = "prod-db.example.com"
    cfg["database"]["port"] = 5432
    cfg["cache"]["ttl"] = 7200
    cfg["features"]["new_ui"] = True
    cfg["features"]["beta_features"] = True

# Validate changes
changes = changelog.get_entries()
assert len(changes) == 4
assert any(entry["key_path"] == "features.new_ui" for entry in changes)
```

### Example 4: Complex Object Tracking

```python
from struct_changelog import track_changes

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.preferences = {}
        self.tags = []

# Track changes to custom objects
user = User("John", 30)

with track_changes(user) as (changelog, tracked_user):
    tracked_user.name = "Jane"
    tracked_user.age = 31
    tracked_user.preferences["theme"] = "dark"
    tracked_user.preferences["language"] = "fr"
    tracked_user.tags.append("premium")
    tracked_user.tags.append("verified")

# All changes are tracked
for entry in changelog.get_entries():
    print(f"User change: {entry['action']} {entry['key_path']}")
```

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

## Why Choose Struct Changelog?

### Compared to Manual Logging
- **Automatic**: No need to manually log every change
- **Comprehensive**: Captures all changes, including nested modifications
- **Consistent**: Standardized format for all change records
- **Error-free**: Eliminates human error in change tracking

### Compared to Database Triggers
- **Language Agnostic**: Works with any Python data structure
- **No Database Required**: Works in memory, perfect for testing
- **Flexible**: Can track changes before they reach the database
- **Lightweight**: No external dependencies or setup required

### Compared to Version Control Systems
- **Granular**: Tracks individual field changes, not just file changes
- **Real-time**: Captures changes as they happen
- **In-memory**: Works with runtime data, not just files
- **Structured**: Provides structured data about changes

### Why Not Use a Global Singleton?

While a global singleton might seem convenient, it has several drawbacks:

- **Shared State**: All users share the same changelog state
- **Testing Issues**: Tests can interfere with each other
- **Thread Safety**: Requires careful synchronization
- **Coupling**: Makes code harder to maintain and test

The helper approaches provide convenience without these issues.

## License

MIT License - see [LICENCE](LICENSE) file for details.