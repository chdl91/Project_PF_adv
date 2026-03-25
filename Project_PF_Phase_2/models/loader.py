"""
Data loaders and serializers for OODB JSON format.

Handles parsing OODB-structured JSON files into domains objects
and vice versa.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path

from models.entities import Topic, Question, Choice, Difficulty
from models.database import QuizDatabase


class OODBLoader:
    """Loads OODB-formatted JSON into QuizDatabase."""

    def __init__(self, data_dir: Path = Path("./data")):
        self.data_dir = Path(data_dir)

    def load_file(self, filename: str) -> dict:
        """Load and parse a JSON file."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_database_from_file(self, filename: str) -> QuizDatabase:
        """Load a complete OODB JSON structure into QuizDatabase."""
        data = self.load_file(filename)
        return self.load_database_from_dict(data)

    def load_database_from_dict(self, data: dict) -> QuizDatabase:
        """
        Load OODB structure from dictionary.

        Expected schema:
        {
          "schema_version": "2.0",
          "objects": {
            "difficulties": [...],
            "topics": [...],
            "questions": [...],
            "choices": [...]
          }
        }
        """
        db = QuizDatabase()

        # Load difficulties
        for diff_data in data.get("objects", {}).get("difficulties", []):
            diff = Difficulty(
                id=diff_data["id"],
                name=diff_data["name"],
                weight=diff_data.get("weight", 1.0)
            )
            db.add_difficulty(diff)

        # Load choices (build lookup)
        choices_by_question: Dict[str, List[Choice]] = {}
        for choice_data in data.get("objects", {}).get("choices", []):
            choice = Choice(
                id=choice_data["id"],
                question_id=choice_data["question_id"],
                label=choice_data["label"],
                text=choice_data["text"]
            )
            db.add_difficulty(choice) if False else None  # placeholder
            q_id = choice.question_id
            if q_id not in choices_by_question:
                choices_by_question[q_id] = []
            choices_by_question[q_id].append(choice)

        # Load questions with their choices
        questions_by_topic: Dict[str, List[Question]] = {}
        for q_data in data.get("objects", {}).get("questions", []):
            question = Question(
                id=q_data["id"],
                topic_id=q_data["topic_id"],
                text=q_data["text"],
                difficulty_id=q_data["difficulty_id"],
                correct_choice_id=q_data["correct_choice_id"],
                explanation=q_data["explanation"],
                choices=choices_by_question.get(q_data["id"], []),
                tags=q_data.get("tags", []),
                created_at=q_data.get("created_at"),
                updated_at=q_data.get("updated_at")
            )
            db.questions[question.id] = question

            topic_id = question.topic_id
            if topic_id not in questions_by_topic:
                questions_by_topic[topic_id] = []
            questions_by_topic[topic_id].append(question)

        # Load topics with their questions
        for topic_data in data.get("objects", {}).get("topics", []):
            topic = Topic(
                id=topic_data["id"],
                name=topic_data["name"],
                description=topic_data.get("description"),
                questions=questions_by_topic.get(topic_data["id"], []),
                metadata=topic_data.get("metadata", {}),
                created_at=topic_data.get("created_at")
            )
            db.add_topic(topic)

        return db

    def save_database_to_file(self, db: QuizDatabase, filename: str) -> None:
        """Save QuizDatabase back to OODB JSON format."""
        data = self.database_to_dict(db)
        filepath = self.data_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def database_to_dict(self, db: QuizDatabase) -> dict:
        """Convert QuizDatabase to OODB dictionary format."""
        return {
            "schema_version": "2.0",
            "objects": {
                "difficulties": [
                    {
                        "id": d.id,
                        "name": d.name,
                        "weight": d.weight
                    }
                    for d in db.difficulties.values()
                ],
                "topics": [
                    {
                        "id": t.id,
                        "name": t.name,
                        "description": t.description,
                        "metadata": t.metadata,
                        "created_at": t.created_at
                    }
                    for t in db.topics.values()
                ],
                "questions": [
                    {
                        "id": q.id,
                        "topic_id": q.topic_id,
                        "text": q.text,
                        "difficulty_id": q.difficulty_id,
                        "correct_choice_id": q.correct_choice_id,
                        "explanation": q.explanation,
                        "tags": q.tags,
                        "created_at": q.created_at,
                        "updated_at": q.updated_at
                    }
                    for q in db.questions.values()
                ],
                "choices": [
                    {
                        "id": c.id,
                        "question_id": c.question_id,
                        "label": c.label,
                        "text": c.text
                    }
                    for c in db.choices.values()
                ]
            }
        }
