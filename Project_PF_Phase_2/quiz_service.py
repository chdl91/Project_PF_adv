import os
from typing import List, Optional, Union
from sqlmodel import SQLModel, create_engine, Session, select
from DB_classes import Subject, Topic, Question, Answer, User

# Set up database connection (works even if Folder is moved, as it uses relative path)
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(script_dir, "DB", "quiz.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}")


def get_all_subjects() -> List[str]:
    """
    Retrieves all subject names from the database.

    Returns:
        List[str]: A list of subject names.

    Raises:
        Exception: If there is an error during database access.
    """
    try:
        with Session(ENGINE) as session:
            statement = select(Subject)
            results = session.exec(statement).all()
            return [subject.subject_name for subject in results]
    except Exception as e:
        raise Exception(f"Error occurred while fetching subjects: {e}")


def get_topics_by_subject(subject_name: str) -> List[str]:
    """
    Retrieves all topic names for a given subject.

    Args:
        subject_name (str): The name of the subject.

    Returns:
        List[str]: A list of topic names associated with the subject.

    Raises:
        Exception: If there is an error during database access or if the subject is not found.
    """
    try:
        with Session(ENGINE) as session:
            subject_select = select(Subject).where(
                Subject.subject_name == subject_name)
            subject = session.exec(subject_select).first()
            if not subject:
                raise Exception(
                    f"Subject '{subject_name}' not found in the database.")

            topic_select = select(Topic).where(
                Topic.subject_id == subject.subject_id)
            topics = session.exec(topic_select).all()
            return [topic.topic_name for topic in topics]
    except Exception as e:
        raise Exception(
            f"Error occurred while fetching topics for subject '{subject_name}': {e}")


def get_topics_with_ids_by_subject(subject_name: str) -> List[dict]:
    """
    Retrieves all topic names AND IDs for a given subject (for quiz_engine).

    Args:
        subject_name (str): The name of the subject.

    Returns:
        List[dict]: List of dicts with "topic_id" and "topic_name" keys.

        Example:
        [
            {"topic_id": 1, "topic_name": "Digitalization"},
            {"topic_id": 2, "topic_name": "Business Model Canvas"},
            ...
        ]

    Raises:
        Exception: If there is an error during database access or if the subject is not found.
    """
    try:
        with Session(ENGINE) as session:
            subject_select = select(Subject).where(
                Subject.subject_name == subject_name)
            subject = session.exec(subject_select).first()
            if not subject:
                raise Exception(
                    f"Subject '{subject_name}' not found in the database.")

            topic_select = select(Topic).where(
                Topic.subject_id == subject.subject_id)
            topics = session.exec(topic_select).all()
            return [
                {"topic_id": topic.topic_id, "topic_name": topic.topic_name}
                for topic in topics
            ]
    except Exception as e:
        raise Exception(
            f"Error occurred while fetching topics for subject '{subject_name}': {e}")


def get_questions_with_answers(topic_id: int, difficulty: Optional[str] = None) -> List[dict]:
    """
    Retrieves questions and their corresponding answers for a given topic and optional difficulty level.

    Args:
        topic_id (int): The ID of the topic.
        difficulty (Optional[str]): The difficulty level to filter questions (e.g., "easy", "medium", "hard"). If None, retrieves all difficulties.

    Returns:
        List[dict]: A list of dictionaries, each containing question text, correct answer, and a list of possible answers.

    Raises:
        Exception: If there is an error during database access or if the topic is not found.
    """
    try:
        with Session(ENGINE) as session:
            if difficulty:
                # Compare difficulty in lowercase (both sides normalized)
                statement = select(Question).where(
                    (Question.topic_id == topic_id) & (Question.difficulty == difficulty.lower()))
            else:
                statement = select(Question).where(
                    Question.topic_id == topic_id)

            questions = session.exec(statement).all()

            questions_data = []
            for question in questions:
                answers_statement = select(Answer).where(
                    Answer.question_id == question.question_id)
                answers = session.exec(answers_statement).all()

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


def save_quiz_result(username: str, subject_name: str, score: int, total_questions: int) -> bool:
    """
    Save a quiz result to the database (Story 6).

    Args:
        username: Username (max 30 chars)
        subject_name: Subject name (e.g., "Digital Business")
        score: Number of correct answers
        total_questions: Total questions in the quiz

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        import datetime
        import zoneinfo

        # Create timestamp in Europe/Zurich timezone
        tz = zoneinfo.ZoneInfo("Europe/Zurich")
        now = datetime.datetime.now(tz)
        timestamp = now.isoformat()

        with Session(ENGINE) as session:
            percentage = (score / total_questions *
                          100) if total_questions > 0 else 0

            if percentage >= 90:
                grade = 6  # Excellent
            elif percentage >= 80:
                grade = 5  # Very Good
            elif percentage >= 70:
                grade = 4  # Satisfactory
            elif percentage >= 60:
                grade = 3  # Failing
            elif percentage >= 50:
                grade = 2  # Back to square one
            else:
                grade = 1  # BYE FHNW 4 eva

            # Create and save the User result
            new_result = User(
                user_name=username[:30],  # Max 30 chars
                user_score=score,
                user_timestamp=timestamp,
                admin_status=False
            )

            session.add(new_result)
            session.commit()
            session.refresh(new_result)

            print(
                f" Result saved for {username}: {score}/{total_questions} ({percentage:.1f}%) - Grade: {grade}")
            return True

    except Exception as e:
        print(f"Error saving quiz result: {e}")
        return False


def get_top_scores(limit: int = 10) -> List[dict]:
    """
    Retrieves the top scores from the database (Story 7 - Scoreboard).

    Args:
        limit (int): Maximum number of top scores to retrieve (default: 10).

    Returns:
        List[dict]: A list of dictionaries containing username, score, and timestamp, sorted by score descending.

    Raises:
        Exception: If there is an error during database access.
    """
    try:
        with Session(ENGINE) as session:
            statement = select(User).order_by(
                User.user_score.desc()).limit(limit)
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


def add_subject(subject_name: str) -> bool:
    """
    Add a new subject to the database (Story 8 - Admin: Add Subject).

    Args:
        subject_name (str): Name of the new subject.

    Returns:
        bool: True if added successfully, False otherwise.
    """
    try:
        with Session(ENGINE) as session:
            # Check if subject already exists
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


def add_topic(topic_name: str, subject_id: int) -> bool:
    """
    Add a new topic to a subject (Story 8 - Admin: Add Topic).

    Args:
        topic_name (str): Name of the new topic.
        subject_id (int): ID of the subject to add the topic to.

    Returns:
        bool: True if added successfully, False otherwise.
    """
    try:
        with Session(ENGINE) as session:
            # Verify subject exists
            subject = session.get(Subject, subject_id)
            if not subject:
                print(f" Subject with ID {subject_id} not found.")
                return False

            # Check if topic already exists in this subject
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


def add_question(topic_id: int, question_text: str, answers: List[str], correct_answer_idx: int, difficulty: str = "medium") -> bool:
    """
    Add a new question with answers to a topic (Story 8 - Admin: Add Question).

    Args:
        topic_id (int): ID of the topic to add the question to.
        question_text (str): Text of the question.
        answers (List[str]): List of answer options (typically 4).
        correct_answer_idx (int): Index (0-based) of the correct answer in the answers list.
        difficulty (str): Difficulty level ("easy", "medium", "hard").

    Returns:
        bool: True if added successfully, False otherwise.
    """
    try:
        # Validate inputs
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

        with Session(ENGINE) as session:
            # Verify topic exists
            topic = session.get(Topic, topic_id)
            if not topic:
                print(f" Topic with ID {topic_id} not found.")
                return False

            # Create question
            new_question = Question(
                topic_id=topic_id,
                question_text=question_text,
                difficulty=difficulty.lower()
            )
            session.add(new_question)
            session.flush()  # Flush to get the question_id without committing

            # Create answers
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

            # Link correct answer to question
            if correct_answer_obj is not None:
                new_question.correct_answer = correct_answer_obj.answer_id
            else:
                session.rollback()
                print(
                    " Error: Could not find correct answer (validation should have caught this).")
                return False

            session.commit()
            session.refresh(new_question)

            print(
                f" Question added to topic '{topic.topic_name}' (ID: {new_question.question_id}) with {len(answers)} answers")
            return True
    except Exception as e:
        print(f"Error adding question: {e}")
        return False


def delete_question(question_id: int) -> bool:
    """
    Delete a question and its answers (Story 8 - Admin: Remove Question).

    Args:
        question_id (int): ID of the question to delete.

    Returns:
        bool: True if deleted successfully, False otherwise.
    """
    try:
        with Session(ENGINE) as session:
            question = session.get(Question, question_id)
            if not question:
                print(f" Question with ID {question_id} not found.")
                return False

            # Delete all answers first
            answers = session.exec(
                select(Answer).where(Answer.question_id == question_id)
            ).all()

            for answer in answers:
                session.delete(answer)

            # Delete question
            session.delete(question)
            session.commit()

            print(
                f" Question (ID: {question_id}) and its {len(answers)} answers deleted")
            return True
    except Exception as e:
        print(f"Error deleting question: {e}")
        return False


def delete_topic(topic_id: int, confirm: bool = False) -> Union[dict, bool]:
    """
    Delete a topic and all its questions (with cascade) (Story 8 - Admin: Remove Topic).

    First call with confirm=False to see what will be deleted (warning).
    Then call with confirm=True to actually delete.

    Args:
        topic_id (int): ID of the topic to delete.
        confirm (bool): If False, returns preview of deletion. If True, performs deletion.

    Returns:
        Union[dict, bool]: If confirm=False, returns dict with deletion preview. If confirm=True, returns bool.
    """
    try:
        with Session(ENGINE) as session:
            topic = session.get(Topic, topic_id)
            if not topic:
                print(f" Topic with ID {topic_id} not found.")
                return False if confirm else {}

            # Count related items
            questions = session.exec(
                select(Question).where(Question.topic_id == topic_id)
            ).all()

            total_answers = 0
            for q in questions:
                answers = session.exec(
                    select(Answer).where(Answer.question_id == q.question_id)
                ).all()
                total_answers += len(answers)

            preview_dict = {
                "topic_id": topic_id,
                "topic_name": topic.topic_name,
                "questions_count": len(questions),
                "answers_count": total_answers,
                "message": f" WARNING: Deleting topic '{topic.topic_name}' will remove {len(questions)} questions and {total_answers} answers. Call with confirm=True to proceed."
            }

            if not confirm:
                print(preview_dict["message"])
                return preview_dict

            # Actually delete (only if confirm=True)
            if confirm:
                for question in questions:
                    answers = session.exec(
                        select(Answer).where(
                            Answer.question_id == question.question_id)
                    ).all()
                    for answer in answers:
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


def delete_subject(subject_id: int, confirm: bool = False) -> Union[dict, bool]:
    """
    Delete a subject and all its topics and questions (with cascade) (Story 8 - Admin: Remove Subject).

    First call with confirm=False to see what will be deleted (warning).
    Then call with confirm=True to actually delete.

    Args:
        subject_id (int): ID of the subject to delete.
        confirm (bool): If False, returns preview of deletion. If True, performs deletion.

    Returns:
        Union[dict, bool]: If confirm=False, returns dict with deletion preview. If confirm=True, returns bool.
    """
    try:
        with Session(ENGINE) as session:
            subject = session.get(Subject, subject_id)
            if not subject:
                print(f" Subject with ID {subject_id} not found.")
                return False if confirm else {}

            # Count related items
            topics = session.exec(
                select(Topic).where(Topic.subject_id == subject_id)
            ).all()

            total_questions = 0
            total_answers = 0
            for topic in topics:
                questions = session.exec(
                    select(Question).where(Question.topic_id == topic.topic_id)
                ).all()
                total_questions += len(questions)

                for q in questions:
                    answers = session.exec(
                        select(Answer).where(
                            Answer.question_id == q.question_id)
                    ).all()
                    total_answers += len(answers)

            preview_dict = {
                "subject_id": subject_id,
                "subject_name": subject.subject_name,
                "topics_count": len(topics),
                "questions_count": total_questions,
                "answers_count": total_answers,
                "message": f" CRITICAL WARNING: Deleting subject '{subject.subject_name}' will remove {len(topics)} topics, {total_questions} questions, and {total_answers} answers. Call with confirm=True to proceed."
            }

            if not confirm:
                print(preview_dict["message"])
                return preview_dict

            # Actually delete (cascade - only if confirm=True)
            if confirm:
                for topic in topics:
                    questions = session.exec(
                        select(Question).where(
                            Question.topic_id == topic.topic_id)
                    ).all()

                    for question in questions:
                        answers = session.exec(
                            select(Answer).where(
                                Answer.question_id == question.question_id)
                        ).all()
                        for answer in answers:
                            session.delete(answer)
                        session.delete(question)

                    session.delete(topic)

                session.delete(subject)
                session.commit()

            print(
                f" Subject '{subject.subject_name}' and {len(topics)} topics with {total_questions} questions deleted")
            return True
    except Exception as e:
        print(f"Error deleting subject: {e}")
        return False if confirm else {}


# Test the function
if __name__ == "__main__":
    print("Starting test...")
    try:
        subjects = get_all_subjects()
        print(f"Subjects found: {subjects}")
        print(f"Number of subjects: {len(subjects)}\n")

        if subjects:
            topics = get_topics_by_subject(subjects[0])
            print(f"Topics for subject '{subjects[0]}': {topics}")
            print(f"Number of topics: {len(topics)}\n")

            # Get topic_id for the first topic (we need to query for it)
            # For now, let's use topic_id = 1 and test
            questions = get_questions_with_answers(topic_id=1, difficulty=None)
            print(f"Questions for topic_id=1: {len(questions)} questions")
            if questions:
                print(f"\nFirst question:")
                print(f"  Text: {questions[0]['question_text']}")
                print(f"  Difficulty: {questions[0]['difficulty']}")
                print(f"  Answers: {questions[0]['answers']}")

    except Exception as e:
        print(f"Error: {e}")
