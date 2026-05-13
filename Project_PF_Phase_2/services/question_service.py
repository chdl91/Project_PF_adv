from typing import List, Optional
from data_access.question_dao import QuestionDAO


class QuestionService:
    """Business logic for questions and answers."""

    def __init__(self, question_dao: QuestionDAO):
        self.question_dao = question_dao

    def get_questions_with_answers(self, topic_id: int, difficulty: Optional[str] = None) -> List[dict]:
        questions = self.question_dao.get_by_topic(topic_id, difficulty)
        result = []
        for q in questions:
            answers = self.question_dao.get_answers(q.question_id)
            result.append({
                "question_id": q.question_id,
                "question_text": q.question_text,
                "difficulty": q.difficulty,
                "correct_answer_id": q.correct_answer,
                "answers": [
                    {"answer_id": a.answer_id, "text": a.answer_text}
                    for a in answers
                ]
            })
        return result

    def add_question(
        self,
        topic_id: int,
        text: str,
        answers: List[str],
        correct_idx: int,
        difficulty: str = "medium"
    ) -> bool:
        if not answers or len(answers) < 2:
            print(" At least 2 answer options required.")
            return False
        if correct_idx < 0 or correct_idx >= len(answers):
            print(f" Correct answer index out of range [0-{len(answers)-1}].")
            return False
        if difficulty.lower() not in ["easy", "medium", "hard"]:
            print(" Difficulty must be easy, medium, or hard.")
            return False

        result = self.question_dao.add(topic_id, text, answers, correct_idx, difficulty)
        if result is None:
            print(" Failed to add question (topic not found).")
            return False
        print(f" Question added (ID: {result.question_id})")
        return True

    def delete_question(self, question_id: int) -> bool:
        if not self.question_dao.delete(question_id):
            print(f" Question ID {question_id} not found.")
            return False
        return True
