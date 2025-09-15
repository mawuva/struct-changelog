"""
Types and data structures for the changelog.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ChangeActions(str, Enum):
    """
    Enum representing the type of change recorded in the changelog.

    Values:
        ADDED: An item was added.
        EDITED: An item was modified.
        REMOVED: An item was removed.
    """

    ADDED = "added"
    EDITED = "edited"
    REMOVED = "removed"


@dataclass
class ChangeLogEntry:
    """
    Represents a single change entry in the changelog.

    Attributes:
        action (ChangeActions): The type of change (ADDED, EDITED, REMOVED).
        key_path (str): The path/key of the changed item, supports nested keys and indices.
        old_value (Any, optional): The original value before the change. Defaults to None.
        new_value (Any, optional): The new value after the change. Defaults to None.
    """

    action: ChangeActions
    key_path: str
    old_value: Any = None
    new_value: Any = None
