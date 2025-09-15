"""
Struct Changelog

Tracks changes in nested Python structures (dicts, lists, tuples, and objects with __dict__).
"""

from .manager import ChangeLogManager
from .types import ChangeActions, ChangeLogEntry
from .helpers import (
    create_changelog,
    track_changes,
    ChangeTracker
)

__version__ = "0.1.0"
__all__ = [
    "ChangeLogManager", 
    "ChangeActions", 
    "ChangeLogEntry", 
    "create_changelog",
    "track_changes", 
    "ChangeTracker",
    "__version__"
]
