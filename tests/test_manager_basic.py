"""
Unit tests for basic ChangeLogManager functionality.
"""

# mypy: ignore-errors

import json

from struct_changelog.manager import ChangeLogManager, _CaptureContext
from struct_changelog.types import ChangeActions


class TestChangeLogManagerBasic:
    """Tests for basic ChangeLogManager functionality."""

    def test_manager_initialization(self):
        """
        Scenario: Initialize a new ChangeLogManager instance

        Expected:
        - Manager should be created successfully
        - Entries list should be empty
        - Length of entries should be 0
        """
        manager = ChangeLogManager()
        assert manager.entries == []
        assert len(manager.entries) == 0

    def test_add_entry(self):
        """
        Scenario: Add a single entry to the changelog manager

        Expected:
        - Entry should be added successfully
        - Entries list should contain one entry
        - Entry attributes should match provided values
        - Old value should be None by default
        """
        manager = ChangeLogManager()

        # Test adding a simple entry
        manager.add(
            action=ChangeActions.ADDED, key_path="user.name", new_value="John Doe"
        )

        assert len(manager.entries) == 1
        entry = manager.entries[0]
        assert entry.action == ChangeActions.ADDED
        assert entry.key_path == "user.name"
        assert entry.new_value == "John Doe"
        assert entry.old_value is None

    def test_add_entry_with_old_value(self):
        """
        Scenario: Add an entry with both old and new values

        Expected:
        - Entry should be added with both old and new values
        - All attributes should match provided values
        - Action should be EDITED
        """
        manager = ChangeLogManager()

        manager.add(
            action=ChangeActions.EDITED, key_path="user.age", old_value=30, new_value=31
        )

        assert len(manager.entries) == 1
        entry = manager.entries[0]
        assert entry.action == ChangeActions.EDITED
        assert entry.old_value == 30
        assert entry.new_value == 31

    def test_add_multiple_entries(self):
        """
        Scenario: Add multiple entries to the changelog manager

        Expected:
        - All entries should be added successfully
        - Entries should be stored in order
        - Each entry should have correct action type
        """
        manager = ChangeLogManager()

        manager.add(ChangeActions.ADDED, "key1", new_value="value1")
        manager.add(ChangeActions.EDITED, "key2", old_value="old", new_value="new")
        manager.add(ChangeActions.REMOVED, "key3", old_value="removed")

        assert len(manager.entries) == 3
        assert manager.entries[0].action == ChangeActions.ADDED
        assert manager.entries[1].action == ChangeActions.EDITED
        assert manager.entries[2].action == ChangeActions.REMOVED

    def test_get_entries(self):
        """
        Scenario: Retrieve entries in generic JSON-serializable format

        Expected:
        - Should return a list of dictionaries
        - Each entry should have required keys (action, key_path, old_value, new_value)
        - Values should be properly converted to strings for actions
        - All entries should be included
        """
        manager = ChangeLogManager()

        manager.add(ChangeActions.ADDED, "test.key", new_value="test_value")
        manager.add(ChangeActions.EDITED, "another.key", old_value=1, new_value=2)

        entries = manager.get_entries()

        assert len(entries) == 2
        assert isinstance(entries, list)

        # Verify entry structure
        entry1 = entries[0]
        assert "action" in entry1
        assert "key_path" in entry1
        assert "old_value" in entry1
        assert "new_value" in entry1

        assert entry1["action"] == "added"
        assert entry1["key_path"] == "test.key"
        assert entry1["new_value"] == "test_value"
        assert entry1["old_value"] is None

    def test_to_json(self):
        """
        Scenario: Serialize changelog entries to JSON

        Expected:
        - Should return a valid JSON string
        - JSON should be parseable
        - Parsed data should match original entries
        - All entries should be included
        """
        manager = ChangeLogManager()

        manager.add(ChangeActions.ADDED, "user.name", new_value="John")
        manager.add(ChangeActions.EDITED, "user.age", old_value=30, new_value=31)

        json_str = manager.to_json()
        assert isinstance(json_str, str)

        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert len(parsed) == 2
        assert parsed[0]["action"] == "added"
        assert parsed[1]["action"] == "edited"

    def test_to_json_with_indent(self):
        """
        Scenario: Serialize to JSON with custom indentation

        Expected:
        - Should return formatted JSON string
        - Lines should be indented with specified spaces
        - JSON should still be valid
        """
        manager = ChangeLogManager()
        manager.add(ChangeActions.ADDED, "test", new_value="value")

        json_str = manager.to_json(indent=4)
        lines = json_str.split("\n")

        # With 4-space indentation, there should be indented lines
        assert any(line.startswith("    ") for line in lines)

    def test_reset(self):
        """
        Scenario: Reset the changelog manager to clear all entries

        Expected:
        - Should clear all entries from the manager
        - Entries list should be empty after reset
        - Manager should be ready for new entries
        """
        manager = ChangeLogManager()

        # Add some entries
        manager.add(ChangeActions.ADDED, "key1", new_value="value1")
        manager.add(ChangeActions.EDITED, "key2", old_value="old", new_value="new")

        assert len(manager.entries) == 2

        # Reset
        manager.reset()

        assert len(manager.entries) == 0
        assert manager.entries == []

    def test_capture_context_creation(self):
        """
        Scenario: Create a capture context for tracking changes

        Expected:
        - Should return a _CaptureContext instance
        - Context should reference the original data
        - Context should reference the changelog manager
        - Default prefix should be empty string
        """
        manager = ChangeLogManager()
        data = {"test": "value"}

        context = manager.capture(data)
        assert isinstance(context, _CaptureContext)
        assert context.original_data is data
        assert context.changelog is manager
        assert context.prefix == ""

    def test_capture_context_with_prefix(self):
        """
        Scenario: Create a capture context with a custom prefix

        Expected:
        - Context should be created with specified prefix
        - Prefix should be stored correctly
        """
        manager = ChangeLogManager()
        data = {"test": "value"}

        context = manager.capture(data, prefix="user.")
        assert context.prefix == "user."
