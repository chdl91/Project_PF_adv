import json  # read json file
import uuid  # generate unique id for each question, answer, topic and user
import os  # check if the database file exists, if not create it
from typing import List  # for type hinting
from sqlmodel import SQLModel, create_engine, Session, select  # for database operations
# import the database classes
from DB_classes import Topics, Questions, Answers, Users


def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def convert_json_to_db(json_file: str, db_file: str):
    if not os.path.exists(db_file):
        engine = create_engine(f"sqlite:///{db_file}")
        SQLModel.metadata.create_all(engine)

    data = load_json_file(json_file)
    with Session(engine) as session:
        for question in data['questions']:
            question_id = str(uuid.uuid4())
            topic_name = question['topic']
            correct_answer_id = str(uuid.uuid4())
            new_question = Questions(
                question_id=question_id,
                topic_id=get_or_create_topic(session, topic_name),
                question_text=question['question_text'],
                correct_answer=correct_answer_id,
                difficulty=question['difficulty']
            )
            session.add(new_question)
            session.commit()

            for answer in question['answers']:
                answer_id = str(uuid.uuid4())
                new_answer = Answers(
                    answer_id=answer_id,
                    question_id=question_id,
                    answer_text=answer
                )
                session.add(new_answer)
                session.commit()
