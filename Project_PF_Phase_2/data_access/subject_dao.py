from typing import List, Optional
from sqlmodel import select
from domain.models import Subject, Topic, Question, Answer


class SubjectDAO:
    """Database access for subjects and topics."""

    def __init__(self, database):
        self.database = database

    def get_all(self) -> List[Subject]:
        with self.database.get_session() as session:
            return session.exec(select(Subject)).all()

    def get_by_name(self, name: str) -> Optional[Subject]:
        with self.database.get_session() as session:
            return session.exec(
                select(Subject).where(Subject.subject_name == name)
            ).first()

    def get_topics(self, subject_id: int) -> List[Topic]:
        with self.database.get_session() as session:
            return session.exec(
                select(Topic).where(Topic.subject_id == subject_id)
            ).all()

    def add_subject(self, name: str) -> Optional[Subject]:
        with self.database.get_session() as session:
            if session.exec(select(Subject).where(Subject.subject_name == name)).first():
                return None
            subject = Subject(subject_name=name)
            session.add(subject)
            session.commit()
            session.refresh(subject)
            return subject

    def add_topic(self, name: str, subject_id: int) -> Optional[Topic]:
        with self.database.get_session() as session:
            existing = session.exec(
                select(Topic).where(
                    (Topic.topic_name == name) & (Topic.subject_id == subject_id)
                )
            ).first()
            if existing:
                return None
            topic = Topic(topic_name=name, subject_id=subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)
            return topic

    def delete_topic(self, topic_id: int) -> bool:
        with self.database.get_session() as session:
            topic = session.get(Topic, topic_id)
            if not topic:
                return False
            questions = session.exec(
                select(Question).where(Question.topic_id == topic_id)
            ).all()
            for q in questions:
                for a in session.exec(select(Answer).where(Answer.question_id == q.question_id)).all():
                    session.delete(a)
                session.delete(q)
            session.delete(topic)
            session.commit()
            return True

    def delete_subject(self, subject_id: int) -> bool:
        with self.database.get_session() as session:
            subject = session.get(Subject, subject_id)
            if not subject:
                return False
            topics = session.exec(
                select(Topic).where(Topic.subject_id == subject_id)
            ).all()
            for topic in topics:
                for q in session.exec(select(Question).where(Question.topic_id == topic.topic_id)).all():
                    for a in session.exec(select(Answer).where(Answer.question_id == q.question_id)).all():
                        session.delete(a)
                    session.delete(q)
                session.delete(topic)
            session.delete(subject)
            session.commit()
            return True
