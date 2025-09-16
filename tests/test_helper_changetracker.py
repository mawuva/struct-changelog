"""
Unit tests for ChangeTracker helper class.
"""

# mypy: ignore-errors

from struct_changelog.helpers import ChangeTracker
from struct_changelog.types import ChangeActions


class TestChangeTracker:
    """Tests for the ChangeTracker class."""

    def test_changetracker_initialization(self):
        """
        Scenario: Initialize a new ChangeTracker instance

        Expected:
        - Should create internal changelog manager
        - Entries should be empty initially
        - Should be ready for use
        """
        tracker = ChangeTracker()

        assert tracker._changelog is not None
        assert tracker.entries == []
        assert len(tracker.entries) == 0

    def test_changetracker_track_method(self):
        """
        Scenario: Use track method to capture changes

        Expected:
        - Should work as context manager
        - Should return original data
        - Should track changes automatically
        - Changes should be stored in tracker
        """
        tracker = ChangeTracker()
        data = {"key": "value"}

        with tracker.track(data) as tracked_data:
            assert tracked_data is data
            tracked_data["key"] = "modified"

        assert len(tracker.entries) == 1
        assert tracker.entries[0]["action"] == "edited"

    def test_changetracker_entries_property(self):
        """
        Scenario: Access entries through entries property

        Expected:
        - Should return list of entries
        - Should reflect all added entries
        - Should be in correct format
        """
        tracker = ChangeTracker()

        # Add entries via add method
        tracker.add(ChangeActions.ADDED, "key1", new_value="value1")
        tracker.add(ChangeActions.EDITED, "key2", old_value="old", new_value="new")

        entries = tracker.entries
        assert len(entries) == 2
        assert isinstance(entries, list)
        assert entries[0]["action"] == "added"
        assert entries[1]["action"] == "edited"

    def test_changetracker_get_entries_method(self):
        """
        Scenario: Use get_entries method to retrieve entries

        Expected:
        - Should return list of entries in generic format
        - Should include all added entries
        - Should match entries property
        """
        tracker = ChangeTracker()
        tracker.add(ChangeActions.ADDED, "test.key", new_value="test_value")

        entries = tracker.get_entries()
        assert len(entries) == 1
        assert entries[0]["key_path"] == "test.key"
        assert entries[0]["new_value"] == "test_value"

    def test_changetracker_to_json_method(self):
        """
        Scenario: Serialize tracker entries to JSON

        Expected:
        - Should return valid JSON string
        - JSON should be parseable
        - Should include all entries
        - Should match get_entries format
        """
        tracker = ChangeTracker()
        tracker.add(ChangeActions.ADDED, "user.name", new_value="John")
        tracker.add(ChangeActions.EDITED, "user.age", old_value=30, new_value=31)

        json_str = tracker.to_json()
        assert isinstance(json_str, str)

        import json

        parsed = json.loads(json_str)
        assert len(parsed) == 2
        assert parsed[0]["action"] == "added"
        assert parsed[1]["action"] == "edited"

    def test_changetracker_to_json_with_indent(self):
        """
        Scenario: Serialize to JSON with custom indentation

        Expected:
        - Should return formatted JSON string
        - Should use specified indentation
        - JSON should still be valid
        """
        tracker = ChangeTracker()
        tracker.add(ChangeActions.ADDED, "test", new_value="value")

        json_str = tracker.to_json(indent=4)
        lines = json_str.split("\n")
        assert any(line.startswith("    ") for line in lines)

    def test_changetracker_reset_method(self):
        """
        Scenario: Reset tracker to clear all entries

        Expected:
        - Should clear all entries from tracker
        - Entries should be empty after reset
        - Tracker should be ready for new entries
        """
        tracker = ChangeTracker()

        # Add some entries
        tracker.add(ChangeActions.ADDED, "key1", new_value="value1")
        tracker.add(ChangeActions.EDITED, "key2", old_value="old", new_value="new")

        assert len(tracker.entries) == 2

        # Reset
        tracker.reset()

        assert len(tracker.entries) == 0
        assert tracker.entries == []

    def test_changetracker_add_method(self):
        """
        Scenario: Add entries manually to tracker

        Expected:
        - Should add entries successfully
        - All entry types should be supported
        - Entries should be stored in order
        """
        tracker = ChangeTracker()

        tracker.add(ChangeActions.ADDED, "user.name", new_value="John Doe")
        tracker.add(ChangeActions.EDITED, "user.age", old_value=30, new_value=31)
        tracker.add(ChangeActions.REMOVED, "temp.field", old_value="temp_value")

        entries = tracker.entries
        assert len(entries) == 3
        assert entries[0]["action"] == "added"
        assert entries[1]["action"] == "edited"
        assert entries[2]["action"] == "removed"

    def test_changetracker_state_persistence(self):
        """
        Scenario: Test that ChangeTracker maintains state across operations

        Expected:
        - Should maintain state between track calls
        - Should accumulate all changes
        - Should support mixing track and manual add operations
        - All changes should be preserved
        """
        tracker = ChangeTracker()
        data = {"counter": 0}

        # First batch of changes
        with tracker.track(data) as tracked_data:
            tracked_data["counter"] = 1
            tracked_data["status"] = "active"

        # Add manual entry
        tracker.add(ChangeActions.ADDED, "log.message", new_value="Process started")

        # Second batch of changes
        with tracker.track(data) as tracked_data:
            tracked_data["counter"] = 2
            tracked_data["status"] = "completed"

        entries = tracker.entries
        assert (
            len(entries) == 5
        )  # 2 + 1 + 2 (status change from active to completed creates 2 entries)

        # Verify all entries are present
        actions = [entry["action"] for entry in entries]
        assert "edited" in actions  # counter changes
        assert "added" in actions  # status and log.message
        # Note: status change from active to completed is tracked as edited, not removed

    def test_changetracker_with_prefix(self):
        """
        Scenario: Use ChangeTracker with custom prefix

        Expected:
        - Should apply prefix to key paths
        - Should track changes normally
        - Key paths should include the prefix
        """
        tracker = ChangeTracker()
        data = {"key": "value"}

        with tracker.track(data, prefix="config.") as tracked_data:
            tracked_data["key"] = "modified"

        entries = tracker.entries
        assert len(entries) == 1
        assert entries[0]["key_path"] == "config.key"

    def test_changetracker_multiple_track_calls(self):
        """
        Scenario: Use track method multiple times on same tracker

        Expected:
        - Should accumulate changes from all track calls
        - Each track call should work independently
        - All changes should be preserved
        """
        tracker = ChangeTracker()
        data1 = {"key1": "value1"}
        data2 = {"key2": "value2"}

        with tracker.track(data1) as tracked_data1:
            tracked_data1["key1"] = "modified1"

        with tracker.track(data2) as tracked_data2:
            tracked_data2["key2"] = "modified2"

        entries = tracker.entries
        assert len(entries) == 2
        assert entries[0]["key_path"] == "key1"
        assert entries[1]["key_path"] == "key2"

    def test_changetracker_equality_with_manager(self):
        """
        Scenario: Compare ChangeTracker behavior with ChangeLogManager

        Expected:
        - Should behave identically to ChangeLogManager
        - get_entries() should return same format
        - to_json() should return same result
        - All operations should be equivalent
        """
        tracker = ChangeTracker()
        from struct_changelog import create_changelog

        manager = create_changelog()

        # Same operation on both
        tracker.add(ChangeActions.ADDED, "test", new_value="value")
        manager.add(ChangeActions.ADDED, "test", new_value="value")

        # Entries should be identical
        assert tracker.get_entries() == manager.get_entries()
        assert tracker.to_json() == manager.to_json()
