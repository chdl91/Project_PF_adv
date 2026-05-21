"""Database tests for question and result persistence."""

import pytest
from sqlmodel import select

from domain.models import Answer, Question, QuizResult, Subject, Topic, User


def test_persist_question_with_answers(seeded_subject_topic, db_session):
    """TC_007: Save a question with four answers and verify the correct answer link."""
    _, topic = seeded_subject_topic

    question = Question(
        topic_id=topic.topic_id,
        question_text="What is AI?",
        difficulty="easy",
    )
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)

    answer_texts = ["Automation", "Analytics",
                    "Artificial Intelligence", "Accounting"]
    created_answers = []
    for index, answer_text in enumerate(answer_texts):
        answer = Answer(question_id=question.question_id,
                        answer_text=answer_text)
        db_session.add(answer)
        db_session.commit()
        db_session.refresh(answer)
        created_answers.append(answer)
        if index == 2:
            question.correct_answer = answer.answer_id
            db_session.add(question)
            db_session.commit()

    answers = db_session.exec(
        select(Answer).where(Answer.question_id == question.question_id)
    ).all()
    found = db_session.exec(
        select(Question).where(Question.question_id == question.question_id)
    ).first()

    assert len(answers) == 4
    assert {a.answer_text for a in answers} == set(answer_texts)
    assert found.correct_answer == created_answers[2].answer_id


def test_filter_questions_by_difficulty_and_topic(seeded_subject_topic, db_session):
    """TC_008: Query questions by both topic and difficulty in one statement."""
    _, topic = seeded_subject_topic

    other_topic = Topic(topic_name="IoT", subject_id=topic.subject_id)
    db_session.add(other_topic)
    db_session.commit()
    db_session.refresh(other_topic)

    seed_data = [
        (topic.topic_id, "easy", "AI easy 1"),
        (topic.topic_id, "medium", "AI medium 1"),
        (topic.topic_id, "medium", "AI medium 2"),
        (other_topic.topic_id, "medium", "IoT medium"),
    ]
    for topic_id, difficulty, text in seed_data:
        db_session.add(
            Question(topic_id=topic_id, question_text=text,
                     difficulty=difficulty)
        )
    db_session.commit()

    results = db_session.exec(
        select(Question).where(
            Question.topic_id == topic.topic_id,
            Question.difficulty == "medium",
        ).order_by(Question.question_text)
    ).all()

    assert [result.question_text for result in results] == [
        "AI medium 1", "AI medium 2"]


def test_save_quiz_result_and_scoreboard_order(seeded_subject_topic, db_session):
    """TC_009: Store quiz results and verify the leaderboard order and average score."""
    subject, _ = seeded_subject_topic

    for username, score in [("alice", 92), ("bob", 75), ("carla", 88)]:
        db_session.add(
            QuizResult(
                user_name=username,
                subject_name=subject.subject_name,
                score=score,
                total_questions=10,
                timestamp="2026-05-14 10:00:00",
            )
        )
    db_session.commit()

    results = db_session.exec(
        select(QuizResult).order_by(
            QuizResult.score.desc(), QuizResult.user_name.asc())
    ).all()

    assert [result.user_name for result in results] == [
        "alice", "carla", "bob"]
    assert sum(result.score for result in results) / \
        len(results) == pytest.approx(85.0)
