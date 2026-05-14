"""Integration tests for the main quiz workflows."""

from sqlmodel import select

from domain.models import Answer, Question, QuizResult, Subject, Topic


def _add_question_with_answers(db_session, topic_id, question_text, difficulty):
    question = Question(
        topic_id=topic_id,
        question_text=question_text,
        difficulty=difficulty,
    )
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)

    correct_answer = Answer(
        question_id=question.question_id, answer_text="Correct")
    db_session.add(correct_answer)
    db_session.commit()
    db_session.refresh(correct_answer)

    question.correct_answer = correct_answer.answer_id
    db_session.add(question)

    for value in ["Wrong 1", "Wrong 2", "Wrong 3"]:
        db_session.add(
            Answer(question_id=question.question_id, answer_text=value))
    db_session.commit()

    return question, correct_answer


def test_quiz_workflow_mixed_answers(db_session):
    """TC_010: A quiz run should persist a non-perfect score correctly."""
    subject = Subject(subject_name="Digital Business")
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)

    topic = Topic(topic_name="AI", subject_id=subject.subject_id)
    db_session.add(topic)
    db_session.commit()
    db_session.refresh(topic)

    questions = []
    for index in range(5):
        question, correct_answer = _add_question_with_answers(
            db_session,
            topic.topic_id,
            f"Question {index + 1}?",
            "easy",
        )
        questions.append((question, correct_answer))

    selected_answers = [
        questions[0][1].answer_id,
        questions[1][1].answer_id,
        questions[2][1].answer_id,
        questions[3][1].answer_id,
        questions[4][1].answer_id + 1,
    ]
    correct_count = sum(
        1 for (question, correct_answer), selected in zip(questions, selected_answers)
        if selected == correct_answer.answer_id
    )

    result = QuizResult(
        user_name="test_user",
        subject_name="Digital Business",
        score=correct_count,
        total_questions=len(questions),
        timestamp="2026-05-14 10:00:00",
    )
    db_session.add(result)
    db_session.commit()

    found = db_session.exec(
        select(QuizResult).where(QuizResult.user_name == "test_user")
    ).first()

    assert correct_count == 4
    assert found.score == 4
    assert found.total_questions == 5


def test_admin_can_update_and_delete_question(db_session):
    """TC_011: Admin can update a question and remove it with all answers."""
    subject = Subject(subject_name="POM")
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)

    topic = Topic(topic_name="Leadership", subject_id=subject.subject_id)
    db_session.add(topic)
    db_session.commit()
    db_session.refresh(topic)

    question, correct_answer = _add_question_with_answers(
        db_session,
        topic.topic_id,
        "Question to update?",
        "easy",
    )

    question.difficulty = "hard"
    db_session.add(question)
    db_session.commit()

    updated_question = db_session.get(Question, question.question_id)
    assert updated_question.difficulty == "hard"
    assert db_session.exec(
        select(Question).where(
            Question.question_id == question.question_id,
            Question.difficulty == "hard",
        )
    ).first() is not None

    for answer in db_session.exec(
        select(Answer).where(Answer.question_id == question.question_id)
    ).all():
        db_session.delete(answer)
    db_session.delete(question)
    db_session.commit()

    assert db_session.get(Question, question.question_id) is None
    assert db_session.exec(
        select(Answer).where(Answer.question_id == question.question_id)
    ).all() == []


def test_scoreboard_orders_multiple_attempts(db_session):
    """TC_012: Scoreboard should order several attempts from highest to lowest."""
    subject = Subject(subject_name="Digital Business")
    db_session.add(subject)
    db_session.commit()

    for username, score in [
        ("alice", 91),
        ("alice", 78),
        ("bob", 88),
    ]:
        db_session.add(
            QuizResult(
                user_name=username,
                subject_name=subject.subject_name,
                score=score,
                total_questions=10,
                timestamp="2026-05-14 12:00:00",
            )
        )
    db_session.commit()

    results = db_session.exec(
        select(QuizResult).order_by(
            QuizResult.score.desc(), QuizResult.timestamp.desc())
    ).all()

    assert [result.score for result in results] == [91, 88, 78]
    assert results[0].user_name == "alice"
