"""
Core domain entities for the quiz application.

Each entity is self-contained and can be serialized/deserialized independently.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Difficulty:
    """Represents difficulty level metadata."""
    id: str
    name: str  # "easy", "medium", "hard"
    weight: float = 1.0

    def __repr__(self) -> str:
        return f"Difficulty({self.name})"


@dataclass
class Choice:
    """Represents a single answer choice for a question."""
    id: str
    question_id: str
    label: str  # "1", "2", "3", "4"
    text: str

    def __repr__(self) -> str:
        return f"Choice({self.label}: {self.text[:30]}...)"


@dataclass
class Question:
    """Represents a single quiz question with its metadata."""
    id: str
    topic_id: str
    text: str
    difficulty_id: str
    correct_choice_id: str
    explanation: str
    choices: List[Choice] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def get_correct_choice(self) -> Optional[Choice]:
        """Return the correct Choice object."""
        return next(
            (c for c in self.choices if c.id == self.correct_choice_id),
            None
        )

    def get_correct_answer_number(self) -> Optional[str]:
        """Return the correct answer as '1', '2', '3', or '4'."""
        correct = self.get_correct_choice()
        return correct.label if correct else None

    def __repr__(self) -> str:
        return f"Question({self.id}: {self.text[:40]}...)"


@dataclass
class Topic:
    """Represents a topic (subject area) containing multiple questions."""
    id: str
    name: str
    description: Optional[str] = None
    questions: List[Question] = field(default_factory=list)
    metadata: Dict[str, any] = field(default_factory=dict)
    created_at: Optional[str] = None

    def question_count(self) -> int:
        """Return number of questions in this topic."""
        return len(self.questions)

    def questions_by_difficulty(self, difficulty_name: str) -> List[Question]:
        """Filter questions by difficulty level."""
        return [
            q for q in self.questions
            if q.difficulty_id and q.difficulty_id.endswith(difficulty_name)
        ]

    def __repr__(self) -> str:
        return f"Topic({self.name}, {self.question_count()} questions)"
