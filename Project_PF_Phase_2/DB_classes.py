from typing import Optional
from sqlmodel import SQLModel, Field


class Topics(SQLModel, table=True):
    topic_id: str = Field(default=None, primary_key=True)
    topic_name: str = Field(..., max_length=30)


class Questions(SQLModel, table=True):
    question_id: str = Field(default=None, primary_key=True)
    topic_id: str = Field(..., foreign_key="topics.topic_id")
    question_text: str = Field(..., max_length=255)
    correct_answer: str = Field(..., foreign_key="answers.answer_id")
    difficulty: str = Field(..., max_length=10)


class Answers(SQLModel, table=True):
    answer_id: str = Field(default=None, primary_key=True)
    question_id: str = Field(..., foreign_key="questions.question_id")
    answer_text: str = Field(..., max_length=255)


class Users(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    user_name: str = Field(..., max_length=3)
    user_score: int = Field(default=0)
    user_timestamp: Optional[str] = Field(default=None)
