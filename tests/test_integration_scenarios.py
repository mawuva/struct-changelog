"""
Integration tests for complex scenarios.
"""

# mypy: ignore-errors

import json

from struct_changelog import (
    ChangeActions,
    ChangeTracker,
    create_changelog,
    track_changes,
)


class TestIntegrationScenarios:
    """Integration tests for complex scenarios."""

    def test_complete_user_profile_update(self):
        """
        Scenario: Complete user profile update with multiple changes

        Expected:
        - Should track all profile modifications
        - Should handle nested structure changes
        - Should detect additions, edits, and removals
        - Should maintain state across multiple operations
        - Should support manual entry addition
        """
        # Initial data
        user_profile = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zipcode": "10001",
                "country": "USA",
            },
            "preferences": {"theme": "light", "language": "en", "notifications": True},
            "hobbies": ["reading", "gaming"],
            "metadata": {"created_at": "2024-01-01", "last_login": "2024-01-15"},
        }

        # Use ChangeTracker to maintain state
        tracker = ChangeTracker()

        # First batch of modifications
        with tracker.track(user_profile) as profile:
            profile["name"] = "Jane Smith"
            profile["email"] = "jane@example.com"
            profile["age"] = 31
            profile["address"]["city"] = "Los Angeles"
            profile["address"]["zipcode"] = "90210"
            profile["preferences"]["theme"] = "dark"
            profile["preferences"]["language"] = "fr"
            profile["hobbies"].append("cooking")
            profile["hobbies"][0] = "programming"
            profile["metadata"]["last_login"] = "2024-01-16"

        # Add manual entries for system changes
        tracker.add(
            ChangeActions.ADDED, "system.updated_at", new_value="2024-01-16T10:30:00Z"
        )
        tracker.add(
            ChangeActions.ADDED,
            "system.update_reason",
            new_value="User requested profile update",
        )

        # Second batch of modifications
        with tracker.track(user_profile) as profile:
            profile["preferences"]["notifications"] = False
            profile["address"]["country"] = "Canada"
            del profile["metadata"]["created_at"]  # Remove a field

        # Check results
        entries = tracker.entries
        assert len(entries) >= 10  # At least 10 changes

        # Check change types
        actions = [entry["action"] for entry in entries]
        assert "edited" in actions
        assert "added" in actions
        assert "removed" in actions

        # Check specific paths
        key_paths = [entry["key_path"] for entry in entries]
        assert "name" in key_paths
        assert "address.city" in key_paths
        assert "preferences.theme" in key_paths
        assert "hobbies.[0]" in key_paths
        assert "system.updated_at" in key_paths

        # Check JSON serialization
        json_str = tracker.to_json()
        parsed = json.loads(json_str)
        assert len(parsed) == len(entries)

    def test_nested_object_tracking(self):
        """
        Scenario: Track changes in complex nested objects

        Expected:
        - Should track changes in custom objects with __dict__
        - Should handle nested object modifications
        - Should track list operations on object attributes
        - Should use attribute names as key paths
        """

        class Address:
            def __init__(self, street, city, zipcode):
                self.street = street
                self.city = city
                self.zipcode = zipcode

        class User:
            def __init__(self, name, age, address):
                self.name = name
                self.age = age
                self.address = address
                self.tags = []

        # Create nested objects
        address = Address("123 Main St", "New York", "10001")
        user = User("John", 30, address)

        # Use track_changes for simplicity
        with track_changes(user) as (changelog, tracked_user):
            tracked_user.name = "Jane"
            tracked_user.age = 31
            tracked_user.address.city = "Los Angeles"
            tracked_user.address.zipcode = "90210"
            tracked_user.tags.append("premium")
            tracked_user.tags.append("verified")

        entries = changelog.get_entries()
        assert len(entries) >= 4

        # Check object paths
        key_paths = [entry["key_path"] for entry in entries]
        assert "name" in key_paths
        assert "age" in key_paths
        assert "address.city" in key_paths
        assert "address.zipcode" in key_paths
        assert "tags.[0]" in key_paths
        assert "tags.[1]" in key_paths

    def test_list_operations_comprehensive(self):
        """
        Scenario: Comprehensive list operations testing

        Expected:
        - Should track modifications to existing list elements
        - Should track additions to lists
        - Should track deletions from lists
        - Should handle nested list operations
        - Should use array notation [index] for key paths
        """
        data = {
            "numbers": [1, 2, 3, 4, 5],
            "strings": ["a", "b", "c"],
            "mixed": [1, "hello", {"key": "value"}],
            "nested_lists": [[1, 2], [3, 4], [5, 6]],
        }

        changelog = create_changelog()

        with changelog.capture(data) as tracked_data:
            # Modify existing elements
            tracked_data["numbers"][0] = 10
            tracked_data["numbers"][2] = 30

            # Add elements
            tracked_data["numbers"].append(6)
            tracked_data["numbers"].append(7)

            # Remove elements
            del tracked_data["strings"][1]

            # Modify nested lists
            tracked_data["nested_lists"][0][0] = 100
            tracked_data["nested_lists"][1].append(5)

            # Add a new list
            tracked_data["new_list"] = ["x", "y", "z"]

            # Modify an element in a mixed list
            tracked_data["mixed"][2]["key"] = "modified"

        entries = changelog.get_entries()

        # Debug output
        print(f"Number of entries: {len(entries)}")
        for i, entry in enumerate(entries, 1):
            print(
                f"  {i}. Action: {entry['action']}, Key: {entry['key_path']}, Old: {entry['old_value']}, New: {entry['new_value']}"
            )

        assert len(entries) >= 7  # 7 effective changes

        # Check operation types
        actions = [entry["action"] for entry in entries]
        assert "edited" in actions
        assert "added" in actions
        assert "removed" in actions

        # Check list paths
        key_paths = [entry["key_path"] for entry in entries]
        print(f"Key paths: {key_paths}")
        print(f"Contains .[0]: {any('.[0]' in path for path in key_paths)}")
        assert any(".[0]" in path for path in key_paths)
        assert any(".[2]" in path for path in key_paths)
        assert any(".[5]" in path for path in key_paths)
        assert any(".[6]" in path for path in key_paths)
        assert "new_list" in key_paths  # New list addition
        assert "nested_lists.[0].[0]" in key_paths
