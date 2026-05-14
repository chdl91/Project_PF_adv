"""
Database Tests for Quiz Application

Test categories:
- Question persistence and retrieval
- Score persistence
- Query filtering (difficulty, topic, subject)
- Database integrity
"""

import pytest
from sqlmodel import Session, select

from domain.models import Subject, Topic, Question, Answer, User, QuizResult


class TestQuestionPersistence:
    """DB Tests for question persistence"""

    def test_persist_and_retrieve_question(self, sqlite_engine):
        """
        TC_101: Persist and Retrieve Question
        Save a question to DB and retrieve it

        Preconditions: In-memory SQLite DB initialized
        Test Data: 
            - subject_name='Digital Business'
            - topic_name='AI'
            - question_text='What is AI?'
            - difficulty='easy'
        Expected: Question retrieved matches saved data
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Create subject
            subject = Subject(subject_name="Digital Business")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            # Create topic
            topic = Topic(topic_name="AI", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            # Create question
            question = Question(
                topic_id=topic.topic_id,
                question_text="What is AI?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()
            session.refresh(question)

            # Retrieve
            stmt = select(Question).where(
                Question.question_text == "What is AI?")
            found = session.exec(stmt).first()

            assert found is not None
            assert found.question_text == "What is AI?"
            assert found.difficulty == "easy"

    def test_retrieve_questions_by_difficulty(self, sqlite_engine):
        """
        TC_102: Retrieve Questions by Difficulty
        Query all questions with specific difficulty level

        Preconditions: 3 questions in DB (1 easy, 1 medium, 1 hard)
        Test Data: difficulty='medium'
        Expected: Returns only 1 question (medium difficulty)
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup
            subject = Subject(subject_name="POM")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Leadership",
                          subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            # Add questions with different difficulties
            for difficulty in ["easy", "medium", "hard"]:
                q = Question(
                    topic_id=topic.topic_id,
                    question_text=f"Question {difficulty}",
                    difficulty=difficulty
                )
                session.add(q)
            session.commit()

            # Query medium difficulty
            stmt = select(Question).where(Question.difficulty == "medium")
            results = session.exec(stmt).all()

            assert len(results) == 1
            assert results[0].difficulty == "medium"

    def test_retrieve_questions_by_topic(self, sqlite_engine):
        """
        TC_103: Retrieve Questions by Topic
        Query all questions from specific topic

        Preconditions: 2 topics with questions
        Test Data: topic_name='AI'
        Expected: Returns only questions from AI topic
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup
            subject = Subject(subject_name="Digital Business")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            # Create two topics
            topic_ai = Topic(topic_name="AI", subject_id=subject.subject_id)
            topic_iot = Topic(topic_name="IoT", subject_id=subject.subject_id)
            session.add(topic_ai)
            session.add(topic_iot)
            session.commit()
            session.refresh(topic_ai)
            session.refresh(topic_iot)

            # Add questions to different topics
            q1 = Question(topic_id=topic_ai.topic_id,
                          question_text="AI Question", difficulty="easy")
            q2 = Question(topic_id=topic_iot.topic_id,
                          question_text="IoT Question", difficulty="easy")
            session.add(q1)
            session.add(q2)
            session.commit()

            # Query AI topic
            stmt = select(Question).where(
                Question.topic_id == topic_ai.topic_id)
            results = session.exec(stmt).all()

            assert len(results) == 1
            assert results[0].question_text == "AI Question"

    def test_retrieve_questions_with_answers(self, sqlite_engine):
        """
        TC_104: Retrieve Questions with Answers
        Ensure answers are correctly linked to questions

        Preconditions: Question with 4 answer options
        Test Data: 1 correct answer + 3 incorrect answers
        Expected: All 4 answers retrieved, 1 marked as correct
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup
            subject = Subject(subject_name="Test")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Test", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            # Create question
            question = Question(
                topic_id=topic.topic_id,
                question_text="Test?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()
            session.refresh(question)

            # Add answers
            answers_text = ["Correct Answer", "Wrong 1", "Wrong 2", "Wrong 3"]
            for idx, text in enumerate(answers_text):
                answer = Answer(
                    question_id=question.question_id,
                    answer_text=text
                )
                session.add(answer)
                session.commit()
                session.refresh(answer)
                if idx == 0:  # First is correct
                    question.correct_answer = answer.answer_id
                    session.add(question)
            session.commit()

            # Retrieve answers
            stmt = select(Answer).where(
                Answer.question_id == question.question_id)
            answers = session.exec(stmt).all()

            assert len(answers) == 4
            assert question.correct_answer == answers[0].answer_id


class TestScorePersistence:
    """DB Tests for score persistence"""

    def test_save_quiz_result(self, sqlite_engine):
        """
        TC_105: Save Quiz Result
        Persist quiz result with score and timestamp

        Preconditions: User completed quiz
        Test Data:
            - user_name='test_user'
            - score=85
            - total_questions=10
        Expected: Result saved and retrievable
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Create user
            user = User(user_name="test_user")
            session.add(user)
            session.commit()
            session.refresh(user)

            # Create quiz result
            result = QuizResult(
                user_name="test_user",
                subject_name="Digital Business",
                score=85,
                total_questions=10,
                timestamp="2026-05-14 10:00:00"
            )
            session.add(result)
            session.commit()
            session.refresh(result)

            # Retrieve
            stmt = select(QuizResult).where(
                QuizResult.user_name == "test_user")
            found = session.exec(stmt).first()

            assert found is not None
            assert found.score == 85
            assert found.total_questions == 10

    def test_multiple_user_scores(self, sqlite_engine):
        """
        TC_106: Multiple User Scores
        Save scores for different users, retrieve individually

        Preconditions: 3 users complete quizzes
        Test Data: user1_score=90, user2_score=75, user3_score=60
        Expected: Each user's score retrievable independently
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Create users
            users_data = [
                ("alice", 90),
                ("bob", 75),
                ("charlie", 60)
            ]

            for username, score in users_data:
                result = QuizResult(
                    user_name=username,
                    subject_name="DIB",
                    score=score,
                    total_questions=10,
                    timestamp="2026-05-14 10:00:00"
                )
                session.add(result)
            session.commit()

            # Retrieve and verify each
            for username, expected_score in users_data:
                stmt = select(QuizResult).where(
                    QuizResult.user_name == username)
                result = session.exec(stmt).first()
                assert result.score == expected_score

    def test_empty_database_query(self, sqlite_engine):
        """
        TC_107: Empty Database Query
        Query empty database returns no results

        Preconditions: Empty DB
        Test Data: None
        Expected: Query returns empty list
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            stmt = select(QuizResult)
            results = session.exec(stmt).all()

            assert len(results) == 0


class TestDataIntegrity:
    """DB Tests for data integrity"""

    def test_question_topic_foreign_key(self, sqlite_engine):
        """
        TC_108: Question-Topic Foreign Key
        Verify question-topic relationship maintained

        Preconditions: Question created with topic_id
        Test Data: topic_id=1
        Expected: Question correctly linked to topic
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            subject = Subject(subject_name="Test")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Test", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            question = Question(
                topic_id=topic.topic_id,
                question_text="Q?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()

            # Verify relationship
            stmt = select(Question).where(
                Question.question_id == question.question_id)
            found_q = session.exec(stmt).first()

            assert found_q.topic_id == topic.topic_id

    def test_answer_question_foreign_key(self, sqlite_engine):
        """
        TC_109: Answer-Question Foreign Key
        Verify answer-question relationship maintained

        Preconditions: Answer created with question_id
        Test Data: question_id=1
        Expected: Answer correctly linked to question
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            subject = Subject(subject_name="Test")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Test", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            question = Question(
                topic_id=topic.topic_id,
                question_text="Q?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()
            session.refresh(question)

            answer = Answer(
                question_id=question.question_id,
                answer_text="Answer text"
            )
            session.add(answer)
            session.commit()

            # Verify relationship
            stmt = select(Answer).where(Answer.answer_id == answer.answer_id)
            found_a = session.exec(stmt).first()

            assert found_a.question_id == question.question_id
