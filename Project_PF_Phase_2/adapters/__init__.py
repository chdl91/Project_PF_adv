"""
Adapter modules for data transformation and compatibility.

- legacy.py: Backward-compatibility with Phase 1 flat list format
- (future) rest_api.py: REST API serializers for web GUI
- (future) cache.py: Caching layer for performance optimization
"""

from .legacy import LegacyQuizAdapter, get_phase1_quiz_data

__all__ = ["LegacyQuizAdapter", "get_phase1_quiz_data"]
