"""
In-memory OODB implementation for Phase 2.

Loads OODB-structured JSON and provides OOP access patterns.
Can be extended to support file persistence, SQL queries, or remote APIs.
"""

from typing import List, Optional, Dict
from .entities import Topic, Question, Choice, Difficulty


class QuizDatabase:
    """
    In-memory OODB for quiz data.

    Provides:
    - Topic and Question lookup
    - Filtering by difficulty, topic, tags
    - Object navigation (Question -> Topic, Question -> Choices, etc)
    """

    def __init__(self):
        self.difficulties: Dict[str, Difficulty] = {}
        self.topics: Dict[str, Topic] = {}
        self.questions: Dict[str, Question] = {}
        self.choices: Dict[str, Choice] = {}

    def add_difficulty(self, diff: Difficulty) -> None:
        """Add a difficulty level."""
        self.difficulties[diff.id] = diff

    def add_topic(self, topic: Topic) -> None:
        """Add a topic (with its questions)."""
        self.topics[topic.id] = topic
        for q in topic.questions:
            self.questions[q.id] = q
            for c in q.choices:
                self.choices[c.id] = c

    def get_topic(self, topic_id: str) -> Optional[Topic]:
        """Fetch a topic by ID."""
        return self.topics.get(topic_id)

    def get_question(self, question_id: str) -> Optional[Question]:
        """Fetch a question by ID."""
        return self.questions.get(question_id)

    def get_choice(self, choice_id: str) -> Optional[Choice]:
        """Fetch a choice by ID."""
        return self.choices.get(choice_id)

    def get_all_topics(self) -> List[Topic]:
        """Return all topics."""
        return list(self.topics.values())

    def get_all_questions(self) -> List[Question]:
        """Return all questions across all topics."""
        return list(self.questions.values())

    def questions_by_topic(self, topic_id: str) -> List[Question]:
        """Return questions for a specific topic."""
        topic = self.get_topic(topic_id)
        return topic.questions if topic else []

    def questions_by_difficulty(self, difficulty_id: str) -> List[Question]:
        """Return questions with a specific difficulty."""
        return [q for q in self.questions.values() if q.difficulty_id == difficulty_id]

    def questions_by_tags(self, tags: List[str]) -> List[Question]:
        """Return questions that have any of the given tags."""
        return [
            q for q in self.questions.values()
            if any(tag in q.tags for tag in tags)
        ]

    def get_difficulty(self, diff_id: str) -> Optional[Difficulty]:
        """Fetch a difficulty level by ID."""
        return self.difficulties.get(diff_id)

    def summary(self) -> Dict:
        """Return a summary of the database contents."""
        return {
            "topics_count": len(self.topics),
            "questions_count": len(self.questions),
            "choices_count": len(self.choices),
            "difficulties": list(self.difficulties.keys()),
            "topics": [
                {
                    "id": t.id,
                    "name": t.name,
                    "question_count": len(t.questions)
                }
                for t in self.topics.values()
            ]
        }
