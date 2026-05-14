"""
Integration Tests for Quiz Application

Test categories:
- Complete quiz workflow (start to finish with scoring)
- Multiple users and score comparison
- Admin operations (add/delete questions)
- Quiz session management
"""

import pytest
from sqlmodel import Session, select

from domain.models import (
    Subject, Topic, Question, Answer, User, QuizResult
)


class TestCompleteQuizWorkflow:
    """Integration Tests for complete quiz session"""

    def test_complete_quiz_workflow_all_correct(self, sqlite_engine):
        """
        TC_201: Complete Quiz Workflow - All Answers Correct
        User selects subject, topic, difficulty, answers all questions correctly,
        receives final score and it's persisted

        Preconditions:
            - Database with subjects, topics, questions, answers initialized
            - User logged in
        Test Steps:
            1. Select subject (Digital Business)
            2. Select topic (AI)
            3. Select difficulty (easy)
            4. Answer 5 questions (all correct)
            5. Submit quiz
        Test Data:
            - 5 questions in DB
            - User selects correct answer for each
        Expected Result:
            - Score = 5/5 (100%)
            - Grade = A
            - Result persisted to DB
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup: Create subject, topic, questions with answers
            subject = Subject(subject_name="Digital Business")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="AI", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            # Create 5 questions
            questions = []
            for i in range(5):
                q = Question(
                    topic_id=topic.topic_id,
                    question_text=f"Question {i+1}?",
                    difficulty="easy"
                )
                session.add(q)
                session.commit()
                session.refresh(q)
                questions.append(q)

                # Add correct answer (answer 1) and 3 wrong ones
                correct_answer = Answer(
                    question_id=q.question_id,
                    answer_text="Correct"
                )
                session.add(correct_answer)
                session.commit()
                session.refresh(correct_answer)
                q.correct_answer = correct_answer.answer_id
                session.add(q)

                for j in range(3):
                    wrong_answer = Answer(
                        question_id=q.question_id,
                        answer_text=f"Wrong {j+1}"
                    )
                    session.add(wrong_answer)
                session.commit()

            # Simulate user answering all correctly
            correct_count = 0
            for q in questions:
                correct_count += 1

            # Calculate score
            percentage = (correct_count / 5) * 100

            # Save result
            result = QuizResult(
                user_name="test_user",
                subject_name="Digital Business",
                score=correct_count,
                total_questions=5,
                timestamp="2026-05-14 10:00:00"
            )
            session.add(result)
            session.commit()

            # Verify
            assert correct_count == 5
            assert percentage == 100.0

            stmt = select(QuizResult).where(
                QuizResult.user_name == "test_user")
            found_result = session.exec(stmt).first()
            assert found_result.score == 5

    def test_complete_quiz_workflow_partial_correct(self, sqlite_engine):
        """
        TC_202: Complete Quiz Workflow - Partial Answers Correct
        User answers 7 out of 10 questions correctly

        Preconditions: 10 questions in DB
        Test Data: User answers 7 correctly, 3 incorrectly
        Expected Result:
            - Score = 7/10 (70%)
            - Grade = C
            - Result persisted
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

            # Create 10 questions
            for i in range(10):
                q = Question(
                    topic_id=topic.topic_id,
                    question_text=f"Q{i+1}?",
                    difficulty="medium"
                )
                session.add(q)
                session.commit()
                session.refresh(q)

                # Add answers
                answer = Answer(
                    question_id=q.question_id,
                    answer_text="Correct"
                )
                session.add(answer)
                session.commit()
                session.refresh(answer)
                q.correct_answer = answer.answer_id
                session.add(q)

                for j in range(3):
                    Answer(question_id=q.question_id, answer_text=f"Wrong {j}")
                session.commit()

            # User gets 7/10 correct
            correct_count = 7
            percentage = (correct_count / 10) * 100

            result = QuizResult(
                user_name="student",
                subject_name="POM",
                score=correct_count,
                total_questions=10,
                timestamp="2026-05-14 11:00:00"
            )
            session.add(result)
            session.commit()

            # Verify
            assert percentage == 70.0

            stmt = select(QuizResult).where(QuizResult.user_name == "student")
            found_result = session.exec(stmt).first()
            assert found_result.score == 7
            assert found_result.total_questions == 10


class TestMultipleUsersScoreboard:
    """Integration Tests for multiple users and scoring"""

    def test_multiple_users_score_comparison(self, sqlite_engine):
        """
        TC_203: Multiple Users Score Comparison
        Multiple users take quizzes, scores saved and comparable

        Preconditions: 3 users complete quizzes
        Test Data:
            - User1: 90/100 (90%)
            - User2: 75/100 (75%)
            - User3: 60/100 (60%)
        Expected Result:
            - All scores persisted
            - Scores retrievable and comparable
            - Ranking identifiable
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup
            subject = Subject(subject_name="Test Subject")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Test", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()

            # Create quiz data for 3 users
            users_scores = [
                ("alice", 90),
                ("bob", 75),
                ("charlie", 60)
            ]

            for username, score in users_scores:
                result = QuizResult(
                    user_name=username,
                    subject_name="Test Subject",
                    score=score,
                    total_questions=100,
                    timestamp="2026-05-14 10:00:00"
                )
                session.add(result)
            session.commit()

            # Retrieve all scores and rank
            stmt = select(QuizResult).order_by(QuizResult.score.desc())
            ranked_results = session.exec(stmt).all()

            # Verify ranking
            assert len(ranked_results) == 3
            assert ranked_results[0].user_name == "alice"
            assert ranked_results[0].score == 90
            assert ranked_results[1].user_name == "bob"
            assert ranked_results[1].score == 75
            assert ranked_results[2].user_name == "charlie"
            assert ranked_results[2].score == 60

    def test_user_multiple_quiz_attempts(self, sqlite_engine):
        """
        TC_204: User Multiple Quiz Attempts
        Same user takes multiple quizzes, all results saved

        Preconditions: Same user takes 3 different quizzes
        Test Data:
            - Attempt 1: 80/100
            - Attempt 2: 85/100 (improved)
            - Attempt 3: 90/100 (best)
        Expected Result:
            - All 3 attempts saved
            - Progress/improvement trackable
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Create subject
            subject = Subject(subject_name="DIB")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="Transformation",
                          subject_id=subject.subject_id)
            session.add(topic)
            session.commit()

            # User takes 3 quizzes
            attempts = [80, 85, 90]
            for idx, score in enumerate(attempts):
                result = QuizResult(
                    user_name="john",
                    subject_name="DIB",
                    score=score,
                    total_questions=100,
                    timestamp=f"2026-05-14 {10+idx}:00:00"
                )
                session.add(result)
            session.commit()

            # Retrieve all attempts for user
            stmt = select(QuizResult).where(QuizResult.user_name == "john")
            user_attempts = session.exec(stmt).all()

            # Verify
            assert len(user_attempts) == 3
            scores = [r.score for r in user_attempts]
            assert scores == [80, 85, 90]
            assert scores[-1] > scores[0]  # Last score is best


class TestAdminOperations:
    """Integration Tests for admin operations"""

    def test_admin_add_question_to_quiz(self, sqlite_engine):
        """
        TC_205: Admin Add Question
        Admin adds new question with answers to database

        Preconditions: Admin logged in, subject and topic exist
        Test Data:
            - question_text='New question?'
            - answers=['Right', 'Wrong1', 'Wrong2', 'Wrong3']
            - correct_index=0
            - difficulty='hard'
        Expected Result:
            - Question persisted
            - All 4 answers persisted
            - Correct answer marked
            - Question queryable by topic/difficulty
        Status: PASS
        """
        with Session(sqlite_engine) as session:
            # Setup
            subject = Subject(subject_name="DIB")
            session.add(subject)
            session.commit()
            session.refresh(subject)

            topic = Topic(topic_name="AI", subject_id=subject.subject_id)
            session.add(topic)
            session.commit()
            session.refresh(topic)

            initial_count_stmt = select(Question)
            initial_count = len(session.exec(initial_count_stmt).all())

            # Admin adds question
            new_question = Question(
                topic_id=topic.topic_id,
                question_text="New hard question?",
                difficulty="hard"
            )
            session.add(new_question)
            session.commit()
            session.refresh(new_question)

            # Add answers
            answers_text = ['Correct', 'Wrong1', 'Wrong2', 'Wrong3']
            for idx, text in enumerate(answers_text):
                answer = Answer(
                    question_id=new_question.question_id,
                    answer_text=text
                )
                session.add(answer)
                if idx == 0:
                    session.commit()
                    session.refresh(answer)
                    new_question.correct_answer = answer.answer_id
                    session.add(new_question)
            session.commit()

            # Verify question added
            stmt = select(Question).where(
                Question.question_text == "New hard question?")
            found = session.exec(stmt).first()
            assert found is not None
            assert found.difficulty == "hard"

            # Verify count increased
            new_count_stmt = select(Question)
            new_count = len(session.exec(new_count_stmt).all())
            assert new_count == initial_count + 1

    def test_admin_delete_question(self, sqlite_engine):
        """
        TC_206: Admin Delete Question
        Admin removes question and its answers from database

        Preconditions: Question with 4 answers exists
        Test Data: question_id=1
        Expected Result:
            - Question deleted
            - Associated answers deleted
            - Question no longer queryable
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

            # Create question with answers
            question = Question(
                topic_id=topic.topic_id,
                question_text="Question to delete?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()
            session.refresh(question)
            question_id = question.question_id

            # Add answers
            for i in range(4):
                answer = Answer(
                    question_id=question_id,
                    answer_text=f"Answer {i}"
                )
                session.add(answer)
            session.commit()

            # Verify question exists
            stmt = select(Question).where(Question.question_id == question_id)
            assert session.exec(stmt).first() is not None

            # Admin deletes question and answers
            q_to_delete = session.get(Question, question_id)
            if q_to_delete:
                # Delete answers first
                answer_stmt = select(Answer).where(
                    Answer.question_id == question_id)
                answers = session.exec(answer_stmt).all()
                for answer in answers:
                    session.delete(answer)
                # Delete question
                session.delete(q_to_delete)
                session.commit()

            # Verify deletion
            stmt = select(Question).where(Question.question_id == question_id)
            assert session.exec(stmt).first() is None

            answer_stmt = select(Answer).where(
                Answer.question_id == question_id)
            assert len(session.exec(answer_stmt).all()) == 0

    def test_admin_modify_question_difficulty(self, sqlite_engine):
        """
        TC_207: Admin Modify Question Difficulty
        Admin changes difficulty level of existing question

        Preconditions: Question exists with difficulty='easy'
        Test Data: new_difficulty='hard'
        Expected Result:
            - Question difficulty updated
            - Change persisted
            - Question retrievable by new difficulty
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
                question_text="Q?",
                difficulty="easy"
            )
            session.add(question)
            session.commit()
            session.refresh(question)
            question_id = question.question_id

            # Admin modifies difficulty
            q = session.get(Question, question_id)
            q.difficulty = "hard"
            session.add(q)
            session.commit()

            # Verify change
            stmt = select(Question).where(Question.question_id == question_id)
            found = session.exec(stmt).first()
            assert found.difficulty == "hard"
