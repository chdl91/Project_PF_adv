"""
Backward-compatibility adapter: OODB -> Phase 1 flat list format.

Allows existing Phase 1 quiz.py code to work with Phase 2 OODB data
without modification. This bridges the gap between old and new architectures.
"""

from typing import List, Dict, Any, Optional
from models.database import QuizDatabase
from models.entities import Question, Topic, Choice, Difficulty


class LegacyQuizAdapter:
    """
    Converts OODB data to Phase 1 flat list format.

    Phase 1 expects: List[{
        "topic": str,
        "question": str,
        "answers": Dict[str, str],
        "correct_answer": int,
        "explanation": str,
        "difficulty": str,
        "id": str
    }]
    """

    @staticmethod
    def to_phase1_format(db: QuizDatabase, topic_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Convert OODB questions to Phase 1 flat list format.

        Args:
            db: QuizDatabase instance
            topic_id: (optional) Filter by specific topic

        Returns:
            List of question dicts in Phase 1 format
        """
        output = []

        # Get questions to convert
        if topic_id:
            questions = db.questions_by_topic(topic_id)
        else:
            questions = db.get_all_questions()

        for q in questions:
            # Build answers dict from choices
            answers_dict = {}
            for choice in sorted(q.choices, key=lambda x: x.label):
                answers_dict[choice.label] = choice.text

            # Get topic name
            topic = db.get_topic(q.topic_id)
            topic_name = topic.name if topic else "Unknown"

            # Get difficulty name
            difficulty = db.get_difficulty(q.difficulty_id)
            difficulty_name = difficulty.name if difficulty else "medium"

            # Convert correct_choice_id to answer number
            correct_num = q.get_correct_answer_number()
            correct_answer = int(correct_num) if correct_num else None

            # Build Phase 1 format
            phase1_question = {
                "topic": topic_name,
                "question": q.text,
                "answers": answers_dict,
                "correct_answer": correct_answer,
                "explanation": q.explanation,
                "difficulty": difficulty_name,
                "id": q.id
            }
            output.append(phase1_question)

        return output

    @staticmethod
    def from_phase1_format(legacy_questions: List[Dict]) -> QuizDatabase:
        """
        Convert Phase 1 flat list format back to OODB.

        This is useful for migrating Phase 1 data files to Phase 2.
        """
        db = QuizDatabase()

        # Collect unique topics and difficulties
        topics_set = set()
        difficulties_set = set()

        for q in legacy_questions:
            topics_set.add(q.get("topic", "Uncategorized"))
            difficulties_set.add(q.get("difficulty", "medium"))

        # Create difficulty objects
        for diff_name in sorted(difficulties_set):
            diff_id = f"D_{diff_name[0].upper()}"
            diff = Difficulty(
                id=diff_id,
                name=diff_name,
                weight={"easy": 1.0, "medium": 2.0,
                        "hard": 3.0}.get(diff_name, 1.5)
            )
            db.add_difficulty(diff)

        # Create topic objects and populate with questions
        for topic_name in sorted(topics_set):
            topic_id = f"T_{topic_name.replace(' ', '_')[:20]}"
            topic = Topic(id=topic_id, name=topic_name)

            # Find questions for this topic
            for q_data in legacy_questions:
                if q_data.get("topic") == topic_name:
                    q_id = q_data.get("id", f"Q_{len(topic.questions)}")
                    difficulty_name = q_data.get("difficulty", "medium")
                    difficulty_id = f"D_{difficulty_name[0].upper()}"

                    # Create choices from answers dict
                    choices = []
                    answers = q_data.get("answers", {})
                    if isinstance(answers, dict):
                        for num, text in sorted(answers.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
                            choice = Choice(
                                id=f"{q_id}_C{num}",
                                question_id=q_id,
                                label=str(num),
                                text=text
                            )
                            choices.append(choice)

                    # Determine correct choice ID
                    correct_num = q_data.get("correct_answer", 1)
                    correct_choice_id = f"{q_id}_C{correct_num}"

                    # Create question
                    question = Question(
                        id=q_id,
                        topic_id=topic_id,
                        text=q_data.get("question", ""),
                        difficulty_id=difficulty_id,
                        correct_choice_id=correct_choice_id,
                        explanation=q_data.get("explanation", ""),
                        choices=choices
                    )
                    topic.questions.append(question)

            db.add_topic(topic)

        return db


# Optional: Make phase1_format callable directly for convenience
def get_phase1_quiz_data(db: QuizDatabase, subject: str = None) -> List[Dict]:
    """
    Convenience function to get Phase 1 formatted data.

    Args:
        db: QuizDatabase instance
        subject: Topic name filter (e.g., "Digital Business")

    Returns:
        Phase 1 format question list
    """
    if subject:
        # Find topic by name
        topic_id = None
        for t in db.get_all_topics():
            if t.name == subject:
                topic_id = t.id
                break
        return LegacyQuizAdapter.to_phase1_format(db, topic_id)
    else:
        return LegacyQuizAdapter.to_phase1_format(db)
