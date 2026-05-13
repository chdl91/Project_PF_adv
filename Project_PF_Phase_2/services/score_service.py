from typing import List
from data_access.score_dao import ScoreDAO


class ScoreService:
    """Business logic for saving quiz results and retrieving the scoreboard."""

    def __init__(self, score_dao: ScoreDAO):
        self.score_dao = score_dao

    def save_quiz_result(
        self, username: str, subject_name: str, score: int, total_questions: int
    ) -> bool:
        try:
            percentage = (score / total_questions * 100) if total_questions > 0 else 0

            if percentage >= 90:
                grade = 6
            elif percentage >= 80:
                grade = 5
            elif percentage >= 70:
                grade = 4
            elif percentage >= 60:
                grade = 3
            elif percentage >= 50:
                grade = 2
            else:
                grade = 1

            self.score_dao.save(username, subject_name, score, total_questions)
            print(
                f" Result saved for {username} ({subject_name}): "
                f"{score}/{total_questions} ({percentage:.1f}%) - Grade: {grade}"
            )
            return True
        except Exception as e:
            print(f"Error saving quiz result: {e}")
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
        except Exception as e:
            print(f"Error retrieving top scores: {e}")
            return []
