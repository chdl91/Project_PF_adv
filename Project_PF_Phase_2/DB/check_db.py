import os
from sqlmodel import SQLModel, create_engine, Session, select
from DB_classes import Topic, Question, Answer

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "quiz.db")

print(f"Database file: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}\n")

engine = create_engine(f"sqlite:///{db_path}")

with Session(engine) as session:
    # Check topics
    topics = session.exec(select(Topic)).all()
    print(f"Total Topics: {len(topics)}")
    for topic in topics[:3]:
        print(f"  - {topic.topic_id}: {topic.topic_name}")

    # Check questions
    questions = session.exec(select(Question)).all()
    print(f"\nTotal Questions: {len(questions)}")
    for q in questions[:3]:
        print(
            f"  - Q{q.question_id}: topic_id={q.topic_id}, text='{q.question_text[:40]}...', correct_answer={q.correct_answer}")

    # Check answers
    answers = session.exec(select(Answer)).all()
    print(f"\nTotal Answers: {len(answers)}")
    for a in answers[:5]:
        print(
            f"  - A{a.answer_id}: question_id={a.question_id}, text='{a.answer_text[:40]}...'")
