"""
Phase 2 Object-Oriented Database Models.

These classes represent the domain objects for the quiz application,
decoupled from data format and storage.
"""

from .entities import Topic, Question, Choice, Difficulty

__all__ = ["Topic", "Question", "Choice", "Difficulty"]
