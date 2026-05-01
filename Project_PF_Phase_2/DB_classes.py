from typing import Optional
from sqlmodel import SQLModel, Field


class Subject(SQLModel, table=True):
    subject_id: int = Field(default=None, primary_key=True)
    subject_name: str = Field(..., max_length=30)


class Topic(SQLModel, table=True):
    topic_id: int = Field(default=None, primary_key=True)
    topic_name: str = Field(..., max_length=30)
    subject_id: int = Field(..., foreign_key="subject.subject_id")


class Question(SQLModel, table=True):
    question_id: int = Field(default=None, primary_key=True)
    topic_id: int = Field(..., foreign_key="topic.topic_id")
    question_text: str = Field(..., max_length=255)
    correct_answer: Optional[int] = Field(
        default=None, foreign_key="answer.answer_id")
    difficulty: str = Field(..., max_length=10)


class Answer(SQLModel, table=True):
    answer_id: int = Field(default=None, primary_key=True)
    question_id: int = Field(..., foreign_key="question.question_id")
    answer_text: str = Field(..., max_length=255)


class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    user_name: str = Field(..., max_length=30)
    user_score: int = Field(default=0)
    user_timestamp: Optional[str] = Field(default=None)
    admin_status: bool = Field(default=False)
