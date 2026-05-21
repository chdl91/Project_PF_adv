from typing import List
from data_access.score_dao import ScoreDAO


class ScoreService:
    """Business logic for saving quiz results and retrieving the scoreboard."""

    def __init__(self, score_dao: ScoreDAO):
        self.score_dao = score_dao

    @staticmethod
    def calculate_percentage(correct: int, total: int) -> float:
        if total <= 0:
            raise ValueError("total_questions must be greater than zero")
        return (correct / total) * 100

    @staticmethod
    def calculate_grade(percentage: float) -> int:
        if percentage >= 90:
            return 6
        if percentage >= 80:
            return 5
        if percentage >= 70:
            return 4
        if percentage >= 60:
            return 3
        if percentage >= 50:
            return 2
        return 1

    def save_quiz_result(
        self, username: str, subject_name: str, score: int, total_questions: int
    ) -> bool:
        try:
            self.score_dao.save(username, subject_name, score, total_questions)
            return True
        except Exception:
            return False

    def get_top_scores(self, limit: int = 10) -> List[dict]:
        try:
            results = self.score_dao.get_top(limit)
            return [
                {
                    "username": r.user_name,
                    "subject": r.subject_name,
                    "score": r.score,
                    "total": r.total_questions,
                    "timestamp": r.timestamp
                }
                for r in results
            ]
        except Exception:
            return []
