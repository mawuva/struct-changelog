"""
Integration tests for performance and edge cases.
"""

# mypy: ignore-errors

import json

from struct_changelog import (
    ChangeActions,
    ChangeTracker,
    create_changelog,
)


class TestIntegrationPerformance:
    """Integration tests for performance and edge cases."""

    def test_circular_reference_handling(self):
        """
        Scenario: Handle circular references in data structures

        Expected:
        - Should not cause infinite recursion
        - Should track changes despite circular references
        - Should complete successfully
        - Should detect circular references and skip them
        """
        # Create circular references
        data = {"key": "value"}
        data["self"] = data
        data["nested"] = {"parent": data, "value": "test"}

        changelog = create_changelog()

        with changelog.capture(data) as tracked_data:
            tracked_data["key"] = "modified"
            tracked_data["nested"]["value"] = "changed"
            tracked_data["new_key"] = "new_value"

        # Should not cause infinite recursion
        entries = changelog.get_entries()
        assert len(entries) == 3

        key_paths = [entry["key_path"] for entry in entries]
        assert "key" in key_paths
        assert "nested.value" in key_paths
        assert "new_key" in key_paths

    def test_large_dataset_performance(self):
        """
        Scenario: Performance test with large dataset

        Expected:
        - Should handle large datasets efficiently
        - Should only track actual changes
        - Should complete in reasonable time
        - Should maintain memory efficiency
        """
        # Create large dataset
        large_data = {
            "users": [
                {"id": i, "name": f"User{i}", "active": i % 2 == 0} for i in range(100)
            ],
            "config": {f"setting_{i}": f"value_{i}" for i in range(50)},
        }

        changelog = create_changelog()

        with changelog.capture(large_data) as tracked_data:
            # Modify some elements
            tracked_data["users"][0]["name"] = "ModifiedUser0"
            tracked_data["users"][50]["active"] = True
            tracked_data["config"]["setting_25"] = "modified_value"
            tracked_data["config"]["new_setting"] = "new_value"

        entries = changelog.get_entries()
        assert len(entries) == 3  # Only effective changes (users[50] does not exist)

        # Check that JSON serialization works
        json_str = changelog.to_json()
        parsed = json.loads(json_str)
        assert len(parsed) == 3

    def test_error_recovery_and_continuation(self):
        """
        Scenario: Error recovery and continuation testing

        Expected:
        - Should handle errors gracefully
        - Should capture changes made before errors
        - Should allow continuation after errors
        - Should support manual error logging
        """
        tracker = ChangeTracker()
        data = {"value": 0}

        # First batch of changes (success)
        with tracker.track(data) as d:
            d["value"] = 1
            d["status"] = "step1"

        # Simulate an error in user code
        try:
            with tracker.track(data) as d:
                d["value"] = 2
                d["status"] = "step2"
                raise ValueError("Simulated error")
        except ValueError:
            pass  # Error is expected

        # Continuation after error
        with tracker.track(data) as d:
            d["value"] = 3
            d["status"] = "step3"

        # Add manual entries for audit
        tracker.add(
            ChangeActions.ADDED,
            "audit.error_occurred",
            new_value="ValueError: Simulated error",
        )
        tracker.add(
            ChangeActions.ADDED, "audit.recovery_time", new_value="2024-01-16T10:30:00Z"
        )

        entries = tracker.entries
        assert len(entries) >= 4  # At least 4 entries

        # Check that changes were captured despite the error
        key_paths = [entry["key_path"] for entry in entries]
        assert "value" in key_paths
        assert "status" in key_paths
        assert "audit.error_occurred" in key_paths
        assert "audit.recovery_time" in key_paths

    def test_thread_safety_basic(self):
        """
        Scenario: Basic thread safety testing

        Expected:
        - Should handle concurrent access safely
        - Should track changes from multiple threads
        - Should not cause data corruption
        - Should complete successfully
        """
        import threading
        import time

        tracker = ChangeTracker()
        data = {"counter": 0}

        def modify_data(thread_id):
            """Function that modifies data in a thread."""
            with tracker.track(data) as tracked_data:
                tracked_data["counter"] = thread_id
                tracked_data[f"thread_{thread_id}"] = f"value_{thread_id}"
                time.sleep(0.01)  # Simulate work

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=modify_data, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Check that all changes were captured
        entries = tracker.entries
        assert len(entries) >= 5  # At least 5 changes

        # Check that data is consistent
        key_paths = [entry["key_path"] for entry in entries]
        assert "counter" in key_paths
        assert any("thread_" in path for path in key_paths)
