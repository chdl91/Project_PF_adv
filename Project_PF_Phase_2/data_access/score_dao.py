import datetime
import zoneinfo
from typing import List
from sqlmodel import select, col
from domain.models import QuizResult


class ScoreDAO:
    """Database access for quiz results and the scoreboard."""

    def __init__(self, database):
        self.database = database

    def save(self, user_name: str, subject_name: str, score: int, total_questions: int) -> QuizResult:

        tz = zoneinfo.ZoneInfo("Europe/Zurich")
        
        timestamp = datetime.datetime.now(tz).isoformat()

        with self.database.get_session() as session:
            result = QuizResult(
                user_name=user_name[:30],
                subject_name=subject_name[:100],
                score=score,
                total_questions=total_questions,
                timestamp=timestamp
            )
            session.add(result)
            session.commit()
            session.refresh(result)
            return result

    def get_top(self, limit: int = 10) -> List[QuizResult]:
        with self.database.get_session() as session:
            return session.exec(
                select(QuizResult).order_by(col(QuizResult.score).desc()).limit(limit)
            ).all()
