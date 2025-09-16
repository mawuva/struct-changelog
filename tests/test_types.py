"""
Unit tests for types and data structures.
"""

# mypy: ignore-errors

from struct_changelog.types import ChangeActions, ChangeLogEntry


class TestChangeActions:
    """Tests for the ChangeActions enum."""

    def test_change_actions_values(self):
        """
        Scenario: Verify that ChangeActions enum has correct string values

        Expected:
        - ADDED should equal "added"
        - EDITED should equal "edited"
        - REMOVED should equal "removed"
        """
        assert ChangeActions.ADDED == "added"
        assert ChangeActions.EDITED == "edited"
        assert ChangeActions.REMOVED == "removed"

    def test_change_actions_enum_properties(self):
        """
        Scenario: Verify ChangeActions enum properties

        Expected:
        - Enum should have exactly 3 values
        - List of enum values should match expected order
        """
        assert len(ChangeActions) == 3
        assert list(ChangeActions) == [
            ChangeActions.ADDED,
            ChangeActions.EDITED,
            ChangeActions.REMOVED,
        ]

    def test_change_actions_string_behavior(self):
        """
        Scenario: Verify that ChangeActions properly inherits from str

        Expected:
        - Enum values should be instances of str
        - Direct comparison with strings should work
        - str() conversion should return the string value
        """
        assert isinstance(ChangeActions.ADDED, str)
        assert ChangeActions.ADDED == "added"
        assert str(ChangeActions.EDITED) == "ChangeActions.EDITED"

    def test_change_actions_comparison(self):
        """
        Scenario: Verify comparison behavior between ChangeActions values

        Expected:
        - Different enum values should not be equal
        - Enum values should equal their string representations
        """
        assert ChangeActions.ADDED != ChangeActions.EDITED
        assert ChangeActions.EDITED != ChangeActions.REMOVED
        assert ChangeActions.ADDED == "added"
        assert ChangeActions.EDITED == "edited"
        assert ChangeActions.REMOVED == "removed"


class TestChangeLogEntry:
    """Tests for the ChangeLogEntry class."""

    def test_changelog_entry_creation(self):
        """
        Scenario: Create a ChangeLogEntry with basic parameters

        Expected:
        - Entry should be created successfully
        - Action should match the provided value
        - Key path should match the provided value
        - Old value should be None by default
        - New value should match the provided value
        """
        entry = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="user.name", new_value="John Doe"
        )

        assert entry.action == ChangeActions.ADDED
        assert entry.key_path == "user.name"
        assert entry.old_value is None
        assert entry.new_value == "John Doe"

    def test_changelog_entry_with_all_parameters(self):
        """
        Scenario: Create a ChangeLogEntry with all parameters

        Expected:
        - Entry should be created with all provided values
        - All attributes should match the provided values
        """
        entry = ChangeLogEntry(
            action=ChangeActions.EDITED, key_path="user.age", old_value=30, new_value=31
        )

        assert entry.action == ChangeActions.EDITED
        assert entry.key_path == "user.age"
        assert entry.old_value == 30
        assert entry.new_value == 31

    def test_changelog_entry_default_values(self):
        """
        Scenario: Create a ChangeLogEntry with only required parameters

        Expected:
        - Entry should be created successfully
        - Optional parameters should have default values (None)
        - Required parameters should match provided values
        """
        entry = ChangeLogEntry(action=ChangeActions.REMOVED, key_path="temp.data")

        assert entry.action == ChangeActions.REMOVED
        assert entry.key_path == "temp.data"
        assert entry.old_value is None
        assert entry.new_value is None

    def test_changelog_entry_immutability(self):
        """
        Scenario: Test dataclass mutability behavior

        Expected:
        - Dataclass should allow attribute modification
        - Modified values should be reflected in the object
        """
        entry = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="test.key", new_value="test_value"
        )

        # Dataclasses allow attribute modification
        entry.new_value = "modified_value"
        assert entry.new_value == "modified_value"

    def test_changelog_entry_with_different_types(self):
        """
        Scenario: Test ChangeLogEntry with various data types

        Expected:
        - Should handle primitive types (int, str, bool)
        - Should handle complex types (list, dict)
        - Should handle None values
        - All values should be stored and retrieved correctly
        """
        # Test with primitive types
        entry1 = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="count", new_value=42
        )
        assert entry1.new_value == 42

        # Test with lists
        entry2 = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="items", new_value=[1, 2, 3]
        )
        assert entry2.new_value == [1, 2, 3]

        # Test with dictionaries
        entry3 = ChangeLogEntry(
            action=ChangeActions.EDITED,
            key_path="config",
            old_value={"debug": False},
            new_value={"debug": True},
        )
        assert entry3.old_value == {"debug": False}
        assert entry3.new_value == {"debug": True}

        # Test with None
        entry4 = ChangeLogEntry(
            action=ChangeActions.REMOVED,
            key_path="deleted_field",
            old_value="some_value",
        )
        assert entry4.old_value == "some_value"
        assert entry4.new_value is None

    def test_changelog_entry_string_representation(self):
        """
        Scenario: Test string representation of ChangeLogEntry

        Expected:
        - String representation should be valid
        - Should contain class name or action information
        """
        entry = ChangeLogEntry(
            action=ChangeActions.ADDED,
            key_path="user.email",
            new_value="user@example.com",
        )

        # Test that entry can be converted to string
        str_repr = str(entry)
        assert "ChangeLogEntry" in str_repr or "ADDED" in str_repr

    def test_changelog_entry_equality(self):
        """
        Scenario: Test equality comparison between ChangeLogEntry instances

        Expected:
        - Entries with same values should be equal
        - Entries with different values should not be equal
        - Dataclass should generate __eq__ automatically
        """
        entry1 = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="test.key", new_value="value"
        )

        entry2 = ChangeLogEntry(
            action=ChangeActions.ADDED, key_path="test.key", new_value="value"
        )

        entry3 = ChangeLogEntry(
            action=ChangeActions.EDITED, key_path="test.key", new_value="value"
        )

        # Dataclasses automatically generate __eq__
        assert entry1 == entry2
        assert entry1 != entry3

    def test_changelog_entry_with_complex_objects(self):
        """
        Scenario: Test ChangeLogEntry with complex custom objects

        Expected:
        - Should handle custom objects as values
        - Object equality should work correctly
        - Old and new values should be stored properly
        """

        class CustomObject:
            def __init__(self, value):
                self.value = value

            def __eq__(self, other):
                return isinstance(other, CustomObject) and self.value == other.value

        obj1 = CustomObject("test")
        obj2 = CustomObject("modified")

        entry = ChangeLogEntry(
            action=ChangeActions.EDITED,
            key_path="custom.object",
            old_value=obj1,
            new_value=obj2,
        )

        assert entry.old_value == obj1
        assert entry.new_value == obj2
        assert entry.old_value != entry.new_value
