"""
Helper functions and utilities for easier ChangeLogManager usage.
"""

from contextlib import contextmanager
from typing import Any, Generator, Tuple

from .manager import ChangeLogManager
from .types import ChangeActions


def create_changelog() -> ChangeLogManager:
    """
    Create a new ChangeLogManager instance.

    This is a simple factory function that provides a more explicit way
    to create changelog instances.

    Returns:
        ChangeLogManager: A new changelog manager instance.

    Example:
        >>> changelog = create_changelog()
        >>> data = {"a": 1}
        >>> with changelog.capture(data) as d:
        ...     d["a"] = 2
        >>> print(changelog.get_entries())
    """
    return ChangeLogManager()


@contextmanager
def track_changes(
    data: Any, prefix: str = ""
) -> Generator[Tuple[ChangeLogManager, Any], None, None]:
    """
    Context manager that automatically creates and manages a ChangeLogManager.

    This helper eliminates the need to manually create a ChangeLogManager
    and provides a clean, concise API for tracking changes.

    Args:
        data (Any): The data structure to track changes in.
        prefix (str, optional): Prefix to prepend to key paths. Defaults to "".

    Yields:
        Tuple[ChangeLogManager, Any]: A tuple containing the changelog manager
            and the tracked data.

    Example:
        >>> data = {"user": {"name": "John", "age": 30}}
        >>> with track_changes(data) as (changelog, tracked_data):
        ...     tracked_data["user"]["name"] = "Jane"
        ...     tracked_data["user"]["age"] = 31
        >>> print(changelog.get_entries())
    """
    changelog = ChangeLogManager()
    with changelog.capture(data, prefix) as tracked_data:
        yield changelog, tracked_data


class ChangeTracker:
    """
    A wrapper class that provides a more object-oriented approach to change tracking.

    This class encapsulates a ChangeLogManager and provides convenient methods
    for tracking changes. It's useful when you need to track changes across
    multiple operations or when you want to maintain state between operations.

    Example:
        >>> tracker = ChangeTracker()
        >>> data = {"count": 0}
        >>> with tracker.track(data) as d:
        ...     d["count"] = 5
        >>> print(tracker.entries)
        >>> tracker.reset()  # Clear all entries
    """

    def __init__(self) -> None:
        """Initialize a new ChangeTracker with an empty changelog."""
        self._changelog = ChangeLogManager()

    def track(self, data: Any, prefix: str = "") -> Any:
        """
        Create a context manager to track changes in the given data.

        Args:
            data (Any): The data structure to track changes in.
            prefix (str, optional): Prefix to prepend to key paths. Defaults to "".

        Returns:
            Any: A context manager that yields the tracked data.

        Example:
            >>> tracker = ChangeTracker()
            >>> data = {"value": 1}
            >>> with tracker.track(data) as d:
            ...     d["value"] = 2
        """
        return self._changelog.capture(data, prefix)

    @property
    def entries(self) -> list:
        """
        Get all changelog entries in a generic, JSON-serializable format.

        Returns:
            list: List of dictionaries representing changelog entries.
        """
        return self._changelog.get_entries()

    def get_entries(self) -> list:
        """
        Get all changelog entries in a generic, JSON-serializable format.

        Returns:
            list: List of dictionaries representing changelog entries.
        """
        return self._changelog.get_entries()

    def to_json(self, indent: int = 2) -> str:
        """
        Return changelog entries as a JSON string.

        Args:
            indent (int, optional): Number of spaces for indentation. Defaults to 2.

        Returns:
            str: JSON string representing the changelog.
        """
        return self._changelog.to_json(indent)

    def reset(self) -> None:
        """Clear all stored entries in the changelog."""
        self._changelog.reset()

    def add(
        self,
        action: ChangeActions,
        key_path: str,
        old_value: Any = None,
        new_value: Any = None,
    ) -> None:
        """
        Add a new entry to the changelog manually.

        Args:
            action (ChangeActions): The type of change (from ChangeActions enum).
            key_path (str): Path/key of the changed item.
            old_value (Any, optional): Original value before change.
            new_value (Any, optional): New value after change.
        """
        self._changelog.add(action, key_path, old_value, new_value)
