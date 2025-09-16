"""
Core ChangeLogManager for tracking changes in nested Python structures.
Fully generic and JSON-serializable.
"""

import copy
import json
from typing import Any, Dict, List, Set

from .types import ChangeActions, ChangeLogEntry


class ChangeLogManager:
    """
    Tracks changes in nested Python structures (dicts, lists, tuples, and objects with __dict__).

    Usage example:
        changelog = ChangeLogManager()
        data = {"a": 1, "b": {"c": 2}}

        with changelog.capture(data) as d:
            d["a"] = 10
            d["b"]["c"] = 20

        print(changelog.get_entries())
    """

    def __init__(self) -> None:
        """Initialize an empty changelog."""
        self.entries: List[ChangeLogEntry] = []

    def add(
        self,
        action: ChangeActions,
        key_path: str,
        old_value: Any = None,
        new_value: Any = None,
    ) -> None:
        """
        Add a new entry to the changelog.

        Args:
            action (ChangeActions): The type of change.
            key_path (str): Path/key of the changed item.
            old_value (Any, optional): Original value before change.
            new_value (Any, optional): New value after change.
        """
        self.entries.append(ChangeLogEntry(action, key_path, old_value, new_value))

    def capture(self, data: Any, prefix: str = "") -> Any:
        """
        Create a context manager to capture changes in `data`.

        Args:
            data (Any): The data structure to track.
            prefix (str, optional): Prefix to prepend to key paths. Defaults to "".

        Returns:
            _CaptureContext: Context manager that captures changes on exit.
        """
        return _CaptureContext(data, self, prefix)

    def get_entries(self) -> List[Dict[str, Any]]:
        """
        Return changelog entries in a generic, JSON-serializable format.

        Returns:
            List[Dict[str, Any]]: Each entry is a dict with keys: action, key_path, old_value, new_value.
        """
        return [
            {
                "action": entry.action.value,
                "key_path": entry.key_path,
                "old_value": entry.old_value,
                "new_value": entry.new_value,
            }
            for entry in self.entries
        ]

    def to_json(self, indent: int = 2) -> str:
        """
        Return changelog entries in a JSON-serializable format.

        Args:
            indent (int, optional): Number of spaces for indentation. Defaults to 2.

        Returns:
            str: JSON string representing the changelog.
        """
        return json.dumps(self.get_entries(), indent=indent)

    def reset(self) -> None:
        """Clear all stored entries in the changelog."""
        self.entries.clear()


class _CaptureContext:
    """
    Internal context manager used by ChangeLogManager to capture changes.

    Usage:
        with _CaptureContext(data, changelog) as d:
            # modify d
    """

    def __init__(
        self, data: Any, changelog: ChangeLogManager, prefix: str = ""
    ) -> None:
        """
        Initialize the capture context.

        Args:
            data (Any): The data structure to track.
            changelog (ChangeLogManager): The changelog to record changes into.
            prefix (str, optional): Prefix for key paths.
        """
        self.original_data = data
        self.changelog = changelog
        self.prefix = prefix
        self.before = None

    def __enter__(self) -> Any:
        """
        Enter the context: store a deep copy of the data for comparison.

        Returns:
            Any: The original data (to be modified within the context).
        """
        self.before = copy.deepcopy(self.original_data)
        return self.original_data

    def __exit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:  # mypy: ignore-errors
        """
        Exit the context: compute differences and populate the changelog.

        Args:
            exc_type: Exception type if raised inside the context.
            exc_val: Exception value.
            exc_tb: Traceback.
        """
        self._diff(self.prefix, self.before, self.original_data, set())

    def _diff(self, path: str, before: Any, after: Any, visited: Set[int]) -> None:
        """
        Recursively compute differences between before and after data.

        Args:
            path (str): Current key path prefix.
            before (Any): Original value.
            after (Any): Modified value.
            visited (Set[int]): Set of object ids already visited (to prevent circular references).
        """
        # Prevent infinite recursion for circular references
        # Only check for circular references when we're about to recurse into containers
        if isinstance(before, (dict, list, tuple)) and isinstance(
            after, (dict, list, tuple)
        ):
            if id(before) in visited or id(after) in visited:
                return
            visited.add(id(before))
            visited.add(id(after))

        # If types differ, record as edited
        if not isinstance(after, type(before)):
            self.changelog.add(
                ChangeActions.EDITED,
                path.rstrip("."),
                old_value=before,
                new_value=after,
            )
            return

        # Handle dicts
        if isinstance(before, dict):
            before_keys = set(before.keys())
            after_keys = set(after.keys())
            for key in after_keys - before_keys:
                self.changelog.add(
                    ChangeActions.ADDED, f"{path}{key}", new_value=after[key]
                )
            for key in before_keys - after_keys:
                self.changelog.add(
                    ChangeActions.REMOVED, f"{path}{key}", old_value=before[key]
                )
            for key in before_keys & after_keys:
                self._diff(f"{path}{key}.", before[key], after[key], visited)

        # Handle lists and tuples
        elif isinstance(before, (list, tuple)):
            common_len = min(len(before), len(after))
            for i in range(common_len):
                self._diff(f"{path}[{i}].", before[i], after[i], visited)
            for i in range(common_len, len(after)):
                self.changelog.add(
                    ChangeActions.ADDED, f"{path}[{i}]", new_value=after[i]
                )
            for i in range(common_len, len(before)):
                self.changelog.add(
                    ChangeActions.REMOVED, f"{path}[{i}]", old_value=before[i]
                )

        # Handle objects with __dict__
        elif hasattr(before, "__dict__") and hasattr(after, "__dict__"):
            self._diff(path, before.__dict__, after.__dict__, visited)

        # Handle simple values
        else:
            if before != after:
                self.changelog.add(
                    ChangeActions.EDITED,
                    path.rstrip("."),
                    old_value=before,
                    new_value=after,
                )
