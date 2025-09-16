"""
Pytest configuration and shared fixtures.
"""

# mypy: ignore-errors

import pytest

from struct_changelog import ChangeLogManager, ChangeTracker


@pytest.fixture
def empty_changelog():
    """
    Fixture for an empty ChangeLogManager.

    Returns:
        ChangeLogManager: Empty changelog manager ready for use
    """
    return ChangeLogManager()


@pytest.fixture
def empty_tracker():
    """
    Fixture for an empty ChangeTracker.

    Returns:
        ChangeTracker: Empty tracker ready for use
    """
    return ChangeTracker()


@pytest.fixture
def sample_data():
    """
    Fixture for sample test data.

    Returns:
        dict: Sample data structure with nested dicts and lists
    """
    return {
        "user": {"name": "John Doe", "age": 30, "email": "john@example.com"},
        "settings": {"theme": "light", "language": "en"},
        "items": [1, 2, 3, 4, 5],
    }


@pytest.fixture
def complex_data():
    """
    Fixture for complex test data.

    Returns:
        dict: Complex data structure with multiple nesting levels
    """
    return {
        "users": [
            {"id": 1, "name": "Alice", "active": True},
            {"id": 2, "name": "Bob", "active": False},
            {"id": 3, "name": "Charlie", "active": True},
        ],
        "config": {
            "database": {"host": "localhost", "port": 5432, "name": "testdb"},
            "cache": {"enabled": True, "ttl": 3600},
        },
        "metadata": {
            "version": "1.0.0",
            "created_at": "2024-01-01T00:00:00Z",
            "tags": ["production", "stable"],
        },
    }


@pytest.fixture
def populated_changelog(sample_data):
    """
    Fixture for a ChangeLogManager with pre-populated entries.

    Returns:
        ChangeLogManager: Changelog manager with sample entries
    """
    changelog = ChangeLogManager()

    # Add some entries
    changelog.add("added", "user.name", new_value="John Doe")
    changelog.add("edited", "user.age", old_value=29, new_value=30)
    changelog.add("added", "settings.theme", new_value="light")

    return changelog


@pytest.fixture
def populated_tracker(sample_data):
    """
    Fixture for a ChangeTracker with pre-populated entries.

    Returns:
        ChangeTracker: Tracker with sample entries
    """
    tracker = ChangeTracker()

    # Add some entries
    tracker.add("added", "user.name", new_value="John Doe")
    tracker.add("edited", "user.age", old_value=29, new_value=30)
    tracker.add("added", "settings.theme", new_value="light")

    return tracker


class MockData:
    """Utility class for creating test data."""

    @staticmethod
    def create_nested_dict(depth=3, width=2):
        """
        Create a nested dictionary with specified depth and width.

        Args:
            depth (int): Nesting depth
            width (int): Number of keys at each level

        Returns:
            dict: Nested dictionary structure
        """
        if depth == 0:
            return f"value_{depth}"

        result = {}
        for i in range(width):
            result[f"key_{i}"] = MockData.create_nested_dict(depth - 1, width)

        return result

    @staticmethod
    def create_large_list(size=1000):
        """
        Create a large list of data items.

        Args:
            size (int): Number of items to create

        Returns:
            list: List of dictionaries with test data
        """
        return [
            {"id": i, "value": f"item_{i}", "active": i % 2 == 0} for i in range(size)
        ]

    @staticmethod
    def create_circular_reference():
        """
        Create data with circular references.

        Returns:
            dict: Dictionary with circular references
        """
        data = {"key": "value"}
        data["self"] = data
        data["nested"] = {"parent": data, "value": "test"}
        return data


@pytest.fixture
def mock_data():
    """
    Fixture for test data utilities.

    Returns:
        MockData: Utility class for creating test data
    """
    return MockData()


# Pytest markers configuration
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")


# Command line options configuration
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--run-performance",
        action="store_true",
        default=False,
        help="run performance tests",
    )


# Test filtering based on options
def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if not config.getoption("--run-performance"):
        skip_perf = pytest.mark.skip(reason="need --run-performance option to run")
        for item in items:
            if "performance" in item.keywords:
                item.add_marker(skip_perf)
