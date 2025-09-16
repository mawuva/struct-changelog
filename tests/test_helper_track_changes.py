"""
Unit tests for track_changes helper function.
"""

# mypy: ignore-errors

import pytest

from struct_changelog.helpers import track_changes
from struct_changelog.types import ChangeActions


class TestTrackChanges:
    """Tests for the track_changes function."""

    def test_track_changes_context_manager(self):
        """
        Scenario: Use track_changes as context manager

        Expected:
        - Should work as context manager
        - Should return tuple (changelog, tracked_data)
        - Should track changes automatically
        - Tracked data should be the original data
        """
        data = {"key": "value"}

        with track_changes(data) as (changelog, tracked_data):
            assert tracked_data is data
            assert changelog is not None
            tracked_data["key"] = "modified"

        # Verify that changes were captured
        assert len(changelog.entries) == 1
        assert changelog.entries[0].action == ChangeActions.EDITED

    def test_track_changes_returns_tuple(self):
        """
        Scenario: Verify track_changes returns proper tuple

        Expected:
        - Should return tuple with two elements
        - First element should be changelog manager
        - Second element should be tracked data
        """
        data = {"test": "value"}

        with track_changes(data) as result:
            changelog, tracked_data = result
            assert changelog is not None
            assert tracked_data is data

    def test_track_changes_with_prefix(self):
        """
        Scenario: Use track_changes with custom prefix

        Expected:
        - Should apply prefix to key paths
        - Changes should be tracked normally
        - Key paths should include the prefix
        """
        data = {"key": "value"}

        with track_changes(data, prefix="user.") as (changelog, tracked_data):
            tracked_data["key"] = "modified"

        entries = changelog.get_entries()
        assert len(entries) == 1
        assert entries[0]["key_path"] == "user.key"

    def test_track_changes_multiple_changes(self):
        """
        Scenario: Track multiple changes in nested structure

        Expected:
        - Should track all changes made
        - Should handle nested modifications
        - Should detect additions and edits
        - All key paths should be captured
        """
        data = {"user": {"name": "John", "age": 30}}

        with track_changes(data) as (changelog, tracked_data):
            tracked_data["user"]["name"] = "Jane"
            tracked_data["user"]["age"] = 31
            tracked_data["user"]["email"] = "jane@example.com"

        entries = changelog.get_entries()
        assert len(entries) == 3

        key_paths = [entry["key_path"] for entry in entries]
        assert "user.name" in key_paths
        assert "user.age" in key_paths
        assert "user.email" in key_paths

    def test_track_changes_exception_handling(self):
        """
        Scenario: Handle exceptions within track_changes context

        Expected:
        - Should handle exceptions gracefully
        - Changes made before exception should be captured
        - Exception should be re-raised
        """
        data = {"key": "value"}

        with pytest.raises(ValueError):
            with track_changes(data) as (changelog, tracked_data):
                tracked_data["key"] = "modified"
                raise ValueError("Test exception")

        # Changes should still be captured
        assert len(changelog.entries) == 1

    def test_track_changes_new_changelog_each_time(self):
        """
        Scenario: Use track_changes multiple times

        Expected:
        - Each call should create a new changelog
        - Changelogs should be independent
        - Each should track only its own changes
        """
        data = {"key": "value"}

        with track_changes(data) as (changelog1, tracked_data1):
            tracked_data1["key"] = "modified1"

        with track_changes(data) as (changelog2, tracked_data2):
            tracked_data2["key"] = "modified2"

        assert changelog1 is not changelog2
        assert len(changelog1.entries) == 1
        assert len(changelog2.entries) == 1
