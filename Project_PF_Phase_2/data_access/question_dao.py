from typing import List, Optional
from sqlmodel import select
from domain.models import Question, Answer, Topic


class QuestionDAO:
    """Database access for questions and answers."""

    def __init__(self, database):
        self.database = database

    def get_by_topic(self, topic_id: int, difficulty: Optional[str] = None) -> List[Question]:
        with self.database.get_session() as session:
            if difficulty:
                stmt = select(Question).where(
                    (Question.topic_id == topic_id) &
                    (Question.difficulty == difficulty.lower())
                )
            else:
                stmt = select(Question).where(Question.topic_id == topic_id)
            return session.exec(stmt).all()

    def get_answers(self, question_id: int) -> List[Answer]:
        with self.database.get_session() as session:
            return session.exec(
                select(Answer).where(Answer.question_id == question_id)
            ).all()

    def add(
        self,
        topic_id: int,
        text: str,
        answers: List[str],
        correct_idx: int,
        difficulty: str
    ) -> Optional[Question]:
        with self.database.get_session() as session:
            if not session.get(Topic, topic_id):
                return None

            question = Question(
                topic_id=topic_id,
                question_text=text,
                difficulty=difficulty.lower()
            )
            session.add(question)
            session.flush()

            correct_answer_obj = None
            for idx, answer_text in enumerate(answers):
                answer = Answer(question_id=question.question_id, answer_text=answer_text)
                session.add(answer)
                session.flush()
                if idx == correct_idx:
                    correct_answer_obj = answer

            if correct_answer_obj is None:
                session.rollback()
                return None

            question.correct_answer = correct_answer_obj.answer_id
            session.commit()
            session.refresh(question)
            return question

    def delete(self, question_id: int) -> bool:
        with self.database.get_session() as session:
            question = session.get(Question, question_id)
            if not question:
                return False
            for answer in session.exec(select(Answer).where(Answer.question_id == question_id)).all():
                session.delete(answer)
            session.delete(question)
            session.commit()
            return True
