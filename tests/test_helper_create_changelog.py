"""
Unit tests for create_changelog helper function.
"""

# mypy: ignore-errors

from struct_changelog.helpers import create_changelog
from struct_changelog.types import ChangeActions


class TestCreateChangelog:
    """Tests for the create_changelog function."""

    def test_create_changelog_returns_manager(self):
        """
        Scenario: Call create_changelog function

        Expected:
        - Should return a ChangeLogManager instance
        - Returned object should be properly initialized
        """
        from struct_changelog.manager import ChangeLogManager

        changelog = create_changelog()
        assert isinstance(changelog, ChangeLogManager)

    def test_create_changelog_new_instance(self):
        """
        Scenario: Call create_changelog multiple times

        Expected:
        - Each call should return a new instance
        - Instances should be independent
        - Entries lists should be separate objects
        """
        changelog1 = create_changelog()
        changelog2 = create_changelog()

        assert changelog1 is not changelog2
        assert changelog1.entries is not changelog2.entries

    def test_create_changelog_empty_initialization(self):
        """
        Scenario: Verify proper initialization of created changelog

        Expected:
        - Entries list should be empty
        - Length should be 0
        - Should be ready for use
        """
        changelog = create_changelog()

        assert changelog.entries == []
        assert len(changelog.entries) == 0

    def test_create_changelog_functionality(self):
        """
        Scenario: Test that created changelog works correctly

        Expected:
        - Should support adding entries manually
        - Should support capturing changes
        - All functionality should work as expected
        """
        changelog = create_changelog()

        # Test adding entry
        changelog.add(ChangeActions.ADDED, "test.key", new_value="test_value")
        assert len(changelog.entries) == 1

        # Test capturing changes
        data = {"key": "value"}
        with changelog.capture(data) as tracked_data:
            tracked_data["key"] = "modified"

        assert len(changelog.entries) == 2
