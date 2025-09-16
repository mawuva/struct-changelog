"""
Struct Changelog

Tracks changes in nested Python structures (dicts, lists, tuples, and objects with __dict__).
"""

from .helpers import ChangeTracker, create_changelog, track_changes
from .manager import ChangeLogManager
from .types import ChangeActions, ChangeLogEntry

__version__ = "0.2.0"
__all__ = [
    "ChangeLogManager",
    "ChangeActions",
    "ChangeLogEntry",
    "create_changelog",
    "track_changes",
    "ChangeTracker",
    "__version__",
]
