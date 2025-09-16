"""
Unit tests for data structure tracking functionality.
"""

# mypy: ignore-errors

from struct_changelog.manager import ChangeLogManager


class TestDataStructures:
    """Tests for tracking changes in various data structures."""

    def test_context_with_nested_dict(self):
        """
        Scenario: Track changes in nested dictionary structures

        Expected:
        - Should track changes at any nesting level
        - Key paths should reflect the nested structure
        - All modifications should be captured
        - New keys should be detected as additions
        """
        manager = ChangeLogManager()
        data = {"user": {"name": "John", "age": 30}}

        with manager.capture(data) as tracked_data:
            tracked_data["user"]["name"] = "Jane"
            tracked_data["user"]["age"] = 31
            tracked_data["user"]["email"] = "jane@example.com"

        entries = manager.get_entries()
        assert len(entries) == 3

        # Verify key paths
        key_paths = [entry["key_path"] for entry in entries]
        assert "user.name" in key_paths
        assert "user.age" in key_paths
        assert "user.email" in key_paths

    def test_context_with_list(self):
        """
        Scenario: Track changes in list structures

        Expected:
        - Should track modifications to existing list elements
        - Should track additions to the list
        - Key paths should use array notation [index]
        - All list operations should be captured
        """
        manager = ChangeLogManager()
        data = {"items": [1, 2, 3]}

        with manager.capture(data) as tracked_data:
            tracked_data["items"][0] = 10
            tracked_data["items"].append(4)
            tracked_data["items"].append(5)

        entries = manager.get_entries()
        assert len(entries) >= 3  # At least 3 changes

        # Verify key paths for lists
        key_paths = [entry["key_path"] for entry in entries]
        assert any("[0]" in path for path in key_paths)
        assert any("[3]" in path for path in key_paths)
        assert any("[4]" in path for path in key_paths)

    def test_context_with_custom_object(self):
        """
        Scenario: Track changes in custom objects with __dict__

        Expected:
        - Should track changes to object attributes
        - Should use attribute names as key paths
        - Should capture old and new values correctly
        """

        class TestObject:
            def __init__(self, value):
                self.value = value

        manager = ChangeLogManager()
        obj = TestObject("initial")

        with manager.capture(obj) as tracked_obj:
            tracked_obj.value = "modified"

        entries = manager.get_entries()
        assert len(entries) == 1
        assert entries[0]["key_path"] == "value"
        assert entries[0]["old_value"] == "initial"
        assert entries[0]["new_value"] == "modified"

    def test_context_dict_key_removal(self):
        """
        Scenario: Track removal of dictionary keys

        Expected:
        - Should detect key removal as removed action
        - Should capture the old value of removed key
        - Should use the key name as key path
        """
        manager = ChangeLogManager()
        data = {"key1": "value1", "key2": "value2"}

        with manager.capture(data) as tracked_data:
            del tracked_data["key1"]

        entries = manager.get_entries()
        assert len(entries) == 1
        assert entries[0]["action"] == "removed"
        assert entries[0]["key_path"] == "key1"
        assert entries[0]["old_value"] == "value1"

    def test_context_list_item_removal(self):
        """
        Scenario: Track removal of list items

        Expected:
        - Should detect item removal as removed action
        - Should capture the old value of removed item
        - Should use array notation [index] in key path
        """
        manager = ChangeLogManager()
        data = {"items": [1, 2, 3, 4]}

        with manager.capture(data) as tracked_data:
            del tracked_data["items"][1]  # Remove item at index 1

        entries = manager.get_entries()
        assert len(entries) == 3  # Modification + reindexing + removal
        assert any(entry["action"] == "removed" for entry in entries)
        assert any(".[1]" in entry["key_path"] for entry in entries)
        # Check that there is an entry with old_value == 2
        assert any(entry["old_value"] == 2 for entry in entries)
