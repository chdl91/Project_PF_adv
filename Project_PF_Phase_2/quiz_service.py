import os
import datetime
import zoneinfo
from typing import List, Optional, Union
from sqlmodel import create_engine, Session, select, col
from DB_classes import Subject, Topic, Question, Answer, User

script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(script_dir, "DB", "quiz.db")


class UserService:
    """Handles user authentication and account creation."""

    def __init__(self, engine):
        self.engine = engine

    def get_or_create_user(self, username: str) -> dict:
        try:
            with Session(self.engine) as session:
                statement = select(User).where(
                    User.user_name == username).order_by(col(User.user_id))
                existing_user = session.exec(statement).first()

                if existing_user:
                    return {
                        "user_id": existing_user.user_id,
                        "user_name": existing_user.user_name,
                        "admin_status": existing_user.admin_status,
                        "is_new": False
                    }

                new_user = User(
                    user_name=username[:30],
                    user_score=0,
                    admin_status=False
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)

                print(f"Welcome {username}! New account created.")

                return {
                    "user_id": new_user.user_id,
                    "user_name": new_user.user_name,
                    "admin_status": new_user.admin_status,
                    "is_new": True
                }

        except Exception as e:
            raise Exception(f"Error during login: {e}")


class SubjectService:
    """Handles subjects and topics: read, create, delete."""

    def __init__(self, engine):
        self.engine = engine

    def get_subject_id_by_name(self, subject_name: str) -> Optional[int]:
        try:
            with Session(self.engine) as session:
                statement = select(Subject).where(
                    Subject.subject_name == subject_name)
                subject = session.exec(statement).first()
                return subject.subject_id if subject else None
        except Exception as e:
            print(f"Error fetching subject ID: {e}")
            return None

    def get_all_subjects(self) -> List[str]:
        try:
            with Session(self.engine) as session:
                results = session.exec(select(Subject)).all()
                return [subject.subject_name for subject in results]
        except Exception as e:
            raise Exception(f"Error occurred while fetching subjects: {e}")

    def get_topics_by_subject(self, subject_name: str) -> List[str]:
        try:
            with Session(self.engine) as session:
                subject = session.exec(
                    select(Subject).where(Subject.subject_name == subject_name)
                ).first()
                if not subject:
                    raise Exception(
                        f"Subject '{subject_name}' not found in the database.")

                topics = session.exec(
                    select(Topic).where(Topic.subject_id == subject.subject_id)
                ).all()
                return [topic.topic_name for topic in topics]
        except Exception as e:
            raise Exception(
                f"Error occurred while fetching topics for subject '{subject_name}': {e}")

    def get_topics_with_ids_by_subject(self, subject_name: str) -> List[dict]:
        try:
            with Session(self.engine) as session:
                subject = session.exec(
                    select(Subject).where(Subject.subject_name == subject_name)
                ).first()
                if not subject:
                    raise Exception(
                        f"Subject '{subject_name}' not found in the database.")

                topics = session.exec(
                    select(Topic).where(Topic.subject_id == subject.subject_id)
                ).all()
                return [
                    {"topic_id": topic.topic_id, "topic_name": topic.topic_name}
                    for topic in topics
                ]
        except Exception as e:
            raise Exception(
                f"Error occurred while fetching topics for subject '{subject_name}': {e}")

    def add_subject(self, subject_name: str) -> bool:
        try:
            with Session(self.engine) as session:
                existing = session.exec(
                    select(Subject).where(Subject.subject_name == subject_name)
                ).first()
                if existing:
                    print(f" Subject '{subject_name}' already exists.")
                    return False

                new_subject = Subject(subject_name=subject_name)
                session.add(new_subject)
                session.commit()
                session.refresh(new_subject)
                print(
                    f" Subject '{subject_name}' added successfully (ID: {new_subject.subject_id})")
                return True
        except Exception as e:
            print(f"Error adding subject: {e}")
            return False

    def add_topic(self, topic_name: str, subject_id: int) -> bool:
        try:
            with Session(self.engine) as session:
                subject = session.get(Subject, subject_id)
                if not subject:
                    print(f" Subject with ID {subject_id} not found.")
                    return False

                existing = session.exec(
                    select(Topic).where(
                        (Topic.topic_name == topic_name) & (
                            Topic.subject_id == subject_id)
                    )
                ).first()
                if existing:
                    print(
                        f" Topic '{topic_name}' already exists in subject '{subject.subject_name}'.")
                    return False

                new_topic = Topic(topic_name=topic_name, subject_id=subject_id)
                session.add(new_topic)
                session.commit()
                session.refresh(new_topic)
                print(
                    f" Topic '{topic_name}' added to '{subject.subject_name}' (ID: {new_topic.topic_id})")
                return True
        except Exception as e:
            print(f"Error adding topic: {e}")
            return False

    def delete_topic(self, topic_id: int, confirm: bool = False) -> Union[dict, bool]:
        try:
            with Session(self.engine) as session:
                topic = session.get(Topic, topic_id)
                if not topic:
                    print(f" Topic with ID {topic_id} not found.")
                    return False if confirm else {}

                questions = session.exec(
                    select(Question).where(Question.topic_id == topic_id)
                ).all()

                total_answers = sum(
                    len(session.exec(select(Answer).where(
                        Answer.question_id == q.question_id)).all())
                    for q in questions
                )

                preview_dict = {
                    "topic_id": topic_id,
                    "topic_name": topic.topic_name,
                    "questions_count": len(questions),
                    "answers_count": total_answers,
                    "message": (
                        f" WARNING: Deleting topic '{topic.topic_name}' will remove "
                        f"{len(questions)} questions and {total_answers} answers. "
                        f"Call with confirm=True to proceed."
                    )
                }

                if not confirm:
                    print(preview_dict["message"])
                    return preview_dict

                for question in questions:
                    for answer in session.exec(
                        select(Answer).where(
                            Answer.question_id == question.question_id)
                    ).all():
                        session.delete(answer)
                    session.delete(question)

                session.delete(topic)
                session.commit()
                print(
                    f" Topic '{topic.topic_name}' and {len(questions)} questions deleted")
                return True
        except Exception as e:
            print(f"Error deleting topic: {e}")
            return False if confirm else {}

    def delete_subject(self, subject_id: int, confirm: bool = False) -> Union[dict, bool]:
        try:
            with Session(self.engine) as session:
                subject = session.get(Subject, subject_id)
                if not subject:
                    print(f" Subject with ID {subject_id} not found.")
                    return False if confirm else {}

                topics = session.exec(
                    select(Topic).where(Topic.subject_id == subject_id)
                ).all()

                total_questions = 0
                total_answers = 0
                for topic in topics:
                    questions = session.exec(
                        select(Question).where(
                            Question.topic_id == topic.topic_id)
                    ).all()
                    total_questions += len(questions)
                    for q in questions:
                        total_answers += len(
                            session.exec(select(Answer).where(
                                Answer.question_id == q.question_id)).all()
                        )

                preview_dict = {
                    "subject_id": subject_id,
                    "subject_name": subject.subject_name,
                    "topics_count": len(topics),
                    "questions_count": total_questions,
                    "answers_count": total_answers,
                    "message": (
                        f" CRITICAL WARNING: Deleting subject '{subject.subject_name}' will remove "
                        f"{len(topics)} topics, {total_questions} questions, and {total_answers} answers. "
                        f"Call with confirm=True to proceed."
                    )
                }

                if not confirm:
                    print(preview_dict["message"])
                    return preview_dict

                for topic in topics:
                    for question in session.exec(
                        select(Question).where(
                            Question.topic_id == topic.topic_id)
                    ).all():
                        for answer in session.exec(
                            select(Answer).where(
                                Answer.question_id == question.question_id)
                        ).all():
                            session.delete(answer)
                        session.delete(question)
                    session.delete(topic)

                session.delete(subject)
                session.commit()
                print(
                    f" Subject '{subject.subject_name}' and {len(topics)} topics "
                    f"with {total_questions} questions deleted"
                )
                return True
        except Exception as e:
            print(f"Error deleting subject: {e}")
            return False if confirm else {}


class QuestionService:
    """Handles questions and answers: read, create, delete."""

    def __init__(self, engine):
        self.engine = engine

    def get_questions_with_answers(self, topic_id: int, difficulty: Optional[str] = None) -> List[dict]:
        try:
            with Session(self.engine) as session:
                if difficulty:
                    statement = select(Question).where(
                        (Question.topic_id == topic_id) &
                        (Question.difficulty == difficulty.lower())
                    )
                else:
                    statement = select(Question).where(
                        Question.topic_id == topic_id)

                questions = session.exec(statement).all()
                questions_data = []
                for question in questions:
                    answers = session.exec(
                        select(Answer).where(
                            Answer.question_id == question.question_id)
                    ).all()
                    questions_data.append({
                        "question_id": question.question_id,
                        "question_text": question.question_text,
                        "difficulty": question.difficulty,
                        "correct_answer_id": question.correct_answer,
                        "answers": [
                            {"answer_id": a.answer_id, "text": a.answer_text}
                            for a in answers
                        ]
                    })
                return questions_data
        except Exception as e:
            print(f"Error retrieving questions: {e}")
            return []

    def add_question(
        self,
        topic_id: int,
        question_text: str,
        answers: List[str],
        correct_answer_idx: int,
        difficulty: str = "medium"
    ) -> bool:
        try:
            if not answers or len(answers) < 2:
                print(" At least 2 answer options required.")
                return False

            if correct_answer_idx < 0 or correct_answer_idx >= len(answers):
                print(
                    f" Correct answer index {correct_answer_idx} out of range [0-{len(answers)-1}].")
                return False

            valid_difficulties = ["easy", "medium", "hard"]
            if difficulty.lower() not in valid_difficulties:
                print(
                    f" Difficulty must be one of: {', '.join(valid_difficulties)}")
                return False

            with Session(self.engine) as session:
                topic = session.get(Topic, topic_id)
                if not topic:
                    print(f" Topic with ID {topic_id} not found.")
                    return False

                new_question = Question(
                    topic_id=topic_id,
                    question_text=question_text,
                    difficulty=difficulty.lower()
                )
                session.add(new_question)
                session.flush()

                correct_answer_obj = None
                for idx, answer_text in enumerate(answers):
                    new_answer = Answer(
                        question_id=new_question.question_id,
                        answer_text=answer_text
                    )
                    session.add(new_answer)
                    session.flush()
                    if idx == correct_answer_idx:
                        correct_answer_obj = new_answer

                if correct_answer_obj is None:
                    session.rollback()
                    print(" Error: Could not find correct answer.")
                    return False

                new_question.correct_answer = correct_answer_obj.answer_id
                session.commit()
                session.refresh(new_question)
                print(
                    f" Question added to topic '{topic.topic_name}' "
                    f"(ID: {new_question.question_id}) with {len(answers)} answers"
                )
                return True
        except Exception as e:
            print(f"Error adding question: {e}")
            return False

    def delete_question(self, question_id: int) -> bool:
        try:
            with Session(self.engine) as session:
                question = session.get(Question, question_id)
                if not question:
                    print(f" Question with ID {question_id} not found.")
                    return False

                answers = session.exec(
                    select(Answer).where(Answer.question_id == question_id)
                ).all()
                for answer in answers:
                    session.delete(answer)

                session.delete(question)
                session.commit()
                print(
                    f" Question (ID: {question_id}) and its {len(answers)} answers deleted")
                return True
        except Exception as e:
            print(f"Error deleting question: {e}")
            return False


class ScoreService:
    """Handles saving quiz results and retrieving the scoreboard."""

    def __init__(self, engine):
        self.engine = engine

    def save_quiz_result(
        self, username: str, subject_name: str, score: int, total_questions: int
    ) -> bool:
        try:
            tz = zoneinfo.ZoneInfo("Europe/Zurich")
            timestamp = datetime.datetime.now(tz).isoformat()

            with Session(self.engine) as session:
                percentage = (score / total_questions *
                              100) if total_questions > 0 else 0

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

                new_result = User(
                    user_name=username[:30],
                    user_score=score,
                    user_timestamp=timestamp,
                    admin_status=False
                )
                session.add(new_result)
                session.commit()
                session.refresh(new_result)
                print(
                    f" Result saved for {username} ({subject_name}): {score}/{total_questions} "
                    f"({percentage:.1f}%) - Grade: {grade}"
                )
                return True
        except Exception as e:
            print(f"Error saving quiz result: {e}")
            return False

    def get_top_scores(self, limit: int = 10) -> List[dict]:
        try:
            with Session(self.engine) as session:
                statement = select(User).order_by(
                    col(User.user_score).desc()).limit(limit)
                results = session.exec(statement).all()
                return [
                    {
                        "username": user.user_name,
                        "score": user.user_score,
                        "timestamp": user.user_timestamp
                    }
                    for user in results
                ]
        except Exception as e:
            print(f"Error retrieving top scores: {e}")
            return []


if __name__ == "__main__":
    from sqlmodel import SQLModel
    engine = create_engine(f"sqlite:///{DB_PATH}")
    SQLModel.metadata.create_all(engine)

    subject_svc = SubjectService(engine)
    question_svc = QuestionService(engine)

    print("Starting test...")
    try:
        subjects = subject_svc.get_all_subjects()
        print(f"Subjects found: {subjects}")
        print(f"Number of subjects: {len(subjects)}\n")

        if subjects:
            topics = subject_svc.get_topics_by_subject(subjects[0])
            print(f"Topics for subject '{subjects[0]}': {topics}")
            print(f"Number of topics: {len(topics)}\n")

            questions = question_svc.get_questions_with_answers(
                topic_id=1, difficulty=None)
            print(f"Questions for topic_id=1: {len(questions)} questions")
            if questions:
                print(f"\nFirst question:")
                print(f"  Text: {questions[0]['question_text']}")
                print(f"  Difficulty: {questions[0]['difficulty']}")
                print(f"  Answers: {questions[0]['answers']}")

    except Exception as e:
        print(f"Error: {e}")
