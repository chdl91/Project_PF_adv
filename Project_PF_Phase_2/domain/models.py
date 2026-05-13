# this module makes so timestamp and correct answer optional because we might want to create a question without an answer first, and then add the answer later, and we might want to create a user without a timestamp first, and then add the timestamp later. This allows for more flexibility in the creation of questions and users, as we can add the missing information at a later time without having to worry about violating any constraints.
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
<<<<<<< HEAD:Project_PF_Phase_2/DB_classes.py
    # is optional because we might want to create a question without an answer first, and then add the answer later
    correct_answer: Optional[int] = Field(
        default=None, foreign_key="answer.answer_id")
=======
    correct_answer: Optional[int] = Field(default=None, foreign_key="answer.answer_id")
>>>>>>> ef4a70f (Major restructuring of code, and all that follows. Also restructured the files):Project_PF_Phase_2/domain/models.py
    difficulty: str = Field(..., max_length=10)


class Answer(SQLModel, table=True):
    answer_id: int = Field(default=None, primary_key=True)
    question_id: int = Field(..., foreign_key="question.question_id")
    answer_text: str = Field(..., max_length=255)


class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    user_name: str = Field(..., max_length=30)
<<<<<<< HEAD:Project_PF_Phase_2/DB_classes.py
    user_score: int = Field(default=0)
    # is optional because we might want to create a user without a timestamp first, and then add the timestamp later
    user_timestamp: Optional[str] = Field(default=None)
=======
>>>>>>> ef4a70f (Major restructuring of code, and all that follows. Also restructured the files):Project_PF_Phase_2/domain/models.py
    admin_status: bool = Field(default=False)


class QuizResult(SQLModel, table=True):
    result_id: int = Field(default=None, primary_key=True)
    user_name: str = Field(..., max_length=30)
    subject_name: str = Field(..., max_length=100)
    score: int = Field(default=0)
    total_questions: int = Field(default=0)
    timestamp: Optional[str] = Field(default=None)
