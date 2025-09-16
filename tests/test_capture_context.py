"""
Unit tests for _CaptureContext functionality.
"""

# mypy: ignore-errors

import pytest

from struct_changelog.manager import ChangeLogManager
from struct_changelog.types import ChangeActions


class TestCaptureContext:
    """Tests for the _CaptureContext class."""

    def test_context_enter_exit(self):
        """
        Scenario: Use capture context to track changes in data

        Expected:
        - Context should return the original data
        - Changes should be tracked automatically
        - Both edited and added changes should be detected
        - All changes should be recorded in the changelog
        """
        manager = ChangeLogManager()
        data = {"key": "value"}

        with manager.capture(data) as tracked_data:
            assert tracked_data is data
            tracked_data["key"] = "modified"
            tracked_data["new_key"] = "new_value"

        # Verify that changes were captured
        assert len(manager.entries) == 2

        # Verify change types
        actions = [entry.action for entry in manager.entries]
        assert ChangeActions.EDITED in actions
        assert ChangeActions.ADDED in actions

    def test_context_exception_handling(self):
        """
        Scenario: Handle exceptions within capture context

        Expected:
        - Context should handle exceptions gracefully
        - Changes made before exception should still be captured
        - Exception should be re-raised after capturing changes
        """
        manager = ChangeLogManager()
        data = {"key": "value"}

        with pytest.raises(ValueError):
            with manager.capture(data) as tracked_data:
                tracked_data["key"] = "modified"
                raise ValueError("Test exception")

        # Changes should still be captured
        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == "key"

    def test_context_circular_reference(self):
        """
        Scenario: Handle circular references in data structures

        Expected:
        - Should not cause infinite recursion
        - Should track changes despite circular references
        - Should complete successfully
        """
        manager = ChangeLogManager()

        # Create circular reference
        data = {"key": "value"}
        data["self"] = data

        with manager.capture(data) as tracked_data:
            tracked_data["key"] = "modified"

        # Should not cause infinite recursion
        assert len(manager.entries) == 1
        assert manager.entries[0].key_path == "key"

    def test_context_with_prefix(self):
        """
        Scenario: Use capture context with custom prefix

        Expected:
        - Key paths should be prefixed with specified prefix
        - Changes should be tracked normally
        - Prefix should be applied to all key paths
        """
        manager = ChangeLogManager()
        data = {"key": "value"}

        with manager.capture(data, prefix="user.") as tracked_data:
            tracked_data["key"] = "modified"

        entries = manager.get_entries()
        assert len(entries) == 1
        assert entries[0]["key_path"] == "user.key"

    def test_context_type_change(self):
        """
        Scenario: Track changes when data type changes

        Expected:
        - Should detect type changes as edited actions
        - Should capture both old and new values
        - Should handle different data types correctly
        """
        manager = ChangeLogManager()
        data = {"key": "string"}

        with manager.capture(data) as tracked_data:
            tracked_data["key"] = 42  # Change from string to int

        entries = manager.get_entries()
        assert len(entries) == 1
        assert entries[0]["action"] == "edited"
        assert entries[0]["old_value"] == "string"
        assert entries[0]["new_value"] == 42
