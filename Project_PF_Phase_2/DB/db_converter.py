from DB_classes import Subject, Topic, Question, Answer, User
import json  # read json file
import os  # check if the database file exists, if not create it
import sys  # for path manipulation
from typing import List  # for type hinting
from sqlmodel import SQLModel, create_engine, Session, select  # for database operations

# Add parent directory to path so we can import from parent folder FIRST (before importing DB_classes)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# import the database models (after path is set)


def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def get_or_create_subject(session: Session, subject_name: str) -> int:
    statement = select(Subject).where(Subject.subject_name == subject_name)
    result = session.exec(statement).first()
    if result:
        return result.subject_id
    else:
        new_subject = Subject(subject_name=subject_name)
        session.add(new_subject)
        session.commit()
        session.refresh(new_subject)
        return new_subject.subject_id


def get_or_create_topic(session: Session, topic_name: str, subject_id: int) -> int:
    statement = select(Topic).where(
        (Topic.topic_name == topic_name) & (Topic.subject_id == subject_id))
    result = session.exec(statement).first()
    if result:
        return result.topic_id
    else:
        new_topic = Topic(topic_name=topic_name, subject_id=subject_id)
        session.add(new_topic)
        session.commit()
        session.refresh(new_topic)
        return new_topic.topic_id


def convert_json_to_db(json_file: str, db_file: str, subject_name: str):
    engine = create_engine(f"sqlite:///{db_file}")
    SQLModel.metadata.create_all(engine)

    data = load_json_file(json_file)
    print(f"Loaded {len(data)} questions from {json_file}")

    with Session(engine) as session:
        # Create/get the subject first
        subject_id = get_or_create_subject(session, subject_name)

        for idx, question in enumerate(data):
            try:
                topic_name = question['topic']
                # This is the key (1, 2, 3, or 4)
                correct_answer_index = question['correct_answer']

                # Create question first (without correct_answer for now)
                new_question = Question(
                    topic_id=get_or_create_topic(
                        session, topic_name, subject_id),
                    question_text=question['question'],
                    correct_answer=None,  # Will set after creating answers
                    difficulty=question['difficulty']
                )
                session.add(new_question)
                session.commit()
                session.refresh(new_question)

                print(
                    f"  [{idx+1}] Created question: {new_question.question_text[:50]}...")

                # Create all answers and track the correct one
                correct_answer_id = None
                for answer_key, answer_text in question['answers'].items():
                    new_answer = Answer(
                        question_id=new_question.question_id,
                        answer_text=answer_text
                    )
                    session.add(new_answer)
                    session.commit()
                    session.refresh(new_answer)

                    # Check if this answer key matches the correct_answer index
                    if int(answer_key) == correct_answer_index:
                        correct_answer_id = new_answer.answer_id

                # Update question with correct answer ID
                if correct_answer_id:
                    new_question.correct_answer = correct_answer_id
                    session.add(new_question)
                    session.commit()
            except Exception as e:
                print(f"  ERROR in question {idx+1}: {e}")
                session.rollback()


if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert DIB.json
    dib_path = os.path.join(script_dir, "Legacy Files", "DIB.json")
    db_path = os.path.join(script_dir, "quiz.db")
    convert_json_to_db(dib_path, db_path, "Digital Business")
    print("✓ DIB.json converted successfully")

    # Convert POM.json
    pom_path = os.path.join(script_dir, "Legacy Files", "POM.json")
    convert_json_to_db(pom_path, db_path, "Principles of Management")
    print("✓ POM.json converted successfully")
