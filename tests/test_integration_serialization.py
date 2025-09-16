"""
Integration tests for serialization and approach comparisons.
"""

# mypy: ignore-errors

import json

from struct_changelog import (
    ChangeLogManager,
    ChangeTracker,
    create_changelog,
    track_changes,
)


class TestIntegrationSerialization:
    """Integration tests for serialization and approach comparisons."""

    def test_multiple_approaches_comparison(self):
        """
        Scenario: Compare different helper approaches

        Expected:
        - All approaches should work correctly
        - Results should be equivalent
        - Each approach should have its own changelog
        - All should support the same operations
        """
        data = {"counter": 0, "status": "idle"}

        # Approach 1: Classic ChangeLogManager
        manager = ChangeLogManager()
        with manager.capture(data) as d1:
            d1["counter"] = 1
            d1["status"] = "active"

        # Approach 2: Factory function
        factory_changelog = create_changelog()
        with factory_changelog.capture(data) as d2:
            d2["counter"] = 2
            d2["status"] = "processing"

        # Approach 3: Global context manager
        with track_changes(data) as (track_changelog, d3):
            d3["counter"] = 3
            d3["status"] = "completed"

        # Approach 4: ChangeTracker
        tracker = ChangeTracker()
        with tracker.track(data) as d4:
            d4["counter"] = 4
            d4["status"] = "final"

        # All should have captured changes
        assert len(manager.entries) > 0
        assert len(factory_changelog.entries) > 0
        assert len(track_changelog.entries) > 0
        assert len(tracker.entries) > 0

        # Entries should be in the same format
        manager_entries = manager.get_entries()
        factory_entries = factory_changelog.get_entries()
        track_entries = track_changelog.get_entries()
        tracker_entries = tracker.get_entries()

        # Check entry structure
        for entries in [
            manager_entries,
            factory_entries,
            track_entries,
            tracker_entries,
        ]:
            assert isinstance(entries, list)
            if entries:  # If there are entries
                entry = entries[0]
                assert "action" in entry
                assert "key_path" in entry
                assert "old_value" in entry
                assert "new_value" in entry

    def test_json_serialization_complex_objects(self):
        """
        Scenario: JSON serialization with complex objects

        Expected:
        - Should serialize all data types to JSON
        - Should handle complex nested structures
        - Should preserve data integrity
        - Should be parseable back to original format
        """
        data = {
            "simple": "value",
            "number": 42,
            "boolean": True,
            "null_value": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "mixed": [1, "string", {"key": "value"}, None],
        }

        changelog = create_changelog()

        with changelog.capture(data) as tracked_data:
            tracked_data["simple"] = "modified"
            tracked_data["number"] = 43
            tracked_data["boolean"] = False
            tracked_data["null_value"] = "not_null"
            tracked_data["list"].append(4)
            tracked_data["dict"]["nested"] = "modified"
            tracked_data["mixed"][1] = "modified_string"

        # Test JSON serialization
        json_str = changelog.to_json()
        parsed = json.loads(json_str)

        # Debug output
        print(f"Number of entries: {len(parsed)}")
        for i, entry in enumerate(parsed, 1):
            print(
                f"  {i}. Action: {entry['action']}, Key: {entry['key_path']}, Old: {entry['old_value']}, New: {entry['new_value']}"
            )

        assert isinstance(parsed, list)
        assert len(parsed) == 7  # 7 effective changes

        # Check that all types are serializable
        for entry in parsed:
            assert isinstance(entry, dict)
            assert "action" in entry
            assert "key_path" in entry
            # old_value and new_value can be any JSON-serializable type
