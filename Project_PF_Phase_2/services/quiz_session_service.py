"""
Quiz Session Service - manages active quiz sessions in memory.
(Stories 2, 3, 5, 6)
"""

import uuid
import datetime
import zoneinfo
import random
from typing import Dict, Optional, Tuple


class QuizSessionService:
    """
    Manages active quiz sessions in memory.

    Receives SubjectService, QuestionService, and ScoreService via constructor
    so any of them can be swapped (e.g. for testing or a different backend).
    """

    def __init__(self, subject_service, question_service, score_service):
        self.subject_service = subject_service
        self.question_service = question_service
        self.score_service = score_service
        self.active_sessions: Dict[str, dict] = {}

    def start_quiz_session(
        self,
        username: str,
        subject_name: str,
        num_questions: int,
        difficulty: Optional[str] = None,
        topic_names: Optional[list[str]] = None,
        topic_name: Optional[str] = None
    ) -> Tuple[str, dict]:
        """
        Start a new quiz session and return (session_id, first_question).

        Session structure:
        {
            "username", "subject_name", "difficulty",
            "questions": [...],
            "current_idx": int,
            "user_answers": [answer_ids],
            "score": int,
            "start_time": datetime,
            "end_time": None
        }
        """
        try:
            topics = self.subject_service.get_topics_with_ids_by_subject(
                subject_name)
            if not topics:
                raise ValueError(f"Subject '{subject_name}' has no topics")

            selected_topic_names = topic_names or (
                [] if topic_name is None else [topic_name])
            if selected_topic_names:
                topics = [
                    topic for topic in topics if topic["topic_name"] in selected_topic_names]
                if not topics:
                    raise ValueError(
                        f"Topic '{', '.join(selected_topic_names)}' not found in subject '{subject_name}'")

            all_questions = []
            for topic in topics:
                all_questions.extend(
                    self.question_service.get_questions_with_answers(
                        topic["topic_id"], difficulty)
                )

            if not all_questions:
                raise ValueError(
                    f"No questions found for subject '{subject_name}' with difficulty '{difficulty}'"
                )
            if len(all_questions) < num_questions:
                raise ValueError(
                    f"Only {len(all_questions)} questions available, but {num_questions} requested"
                )

            selected = random.sample(all_questions, num_questions)
            session_id = str(uuid.uuid4())
            tz = zoneinfo.ZoneInfo("Europe/Zurich")

            self.active_sessions[session_id] = {
                "username": username,
                "subject_name": subject_name,
                "difficulty": difficulty,
                "questions": selected,
                "current_idx": 0,
                "user_answers": [],
                "score": 0,
                "start_time": datetime.datetime.now(tz),
                "end_time": None
            }

            return session_id, selected[0]

        except Exception:
            raise

    def validate_answer(self, session_id: str, selected_answer_id: int) -> bool:
        """Return True if the selected answer matches the current question's correct answer."""
        session = self.active_sessions[session_id]
        current = session["questions"][session["current_idx"]]
        return selected_answer_id == current["correct_answer_id"]

    def submit_answer(self, session_id: str, selected_answer_id: int) -> dict:
        """
        Record the answer, advance to the next question, and return feedback.

        Returns:
            {is_correct, score, current_question_num, total_questions, next_question, quiz_complete, correct_answer_text}
        """
        session = self.active_sessions[session_id]
        is_correct = self.validate_answer(session_id, selected_answer_id)
        current_question = session["questions"][session["current_idx"]]

        # Get the correct answer text
        correct_answer_id = current_question["correct_answer_id"]
        correct_answer_text = next(
            (answer["text"] for answer in current_question["answers"]
             if answer["answer_id"] == correct_answer_id),
            "No answer available"
        )

        session["user_answers"].append(selected_answer_id)
        if is_correct:
            session["score"] += 1
        session["current_idx"] += 1

        total = len(session["questions"])
        quiz_complete = session["current_idx"] >= total
        next_question = None if quiz_complete else session["questions"][session["current_idx"]]

        return {
            "is_correct": is_correct,
            "score": session["score"],
            "current_question_num": session["current_idx"],
            "total_questions": total,
            "next_question": next_question,
            "quiz_complete": quiz_complete,
            "correct_answer_text": correct_answer_text
        }

    def get_quiz_progress(self, session_id: str) -> dict:
        """Return a progress snapshot for an active session."""
        session = self.active_sessions[session_id]
        total = len(session["questions"])
        return {
            "current_question_num": session["current_idx"] + 1,
            "score": session["score"],
            "total_questions": total,
            "percentage": round((session["score"] / total) * 100, 2)
        }

    def end_quiz_session(self, session_id: str) -> dict:
        """
        Finalise the quiz: save result to database, remove session, return summary.

        Returns:
            {username, subject_name, score, total_questions, percentage, grade}
        """
        session = self.active_sessions[session_id]
        session["end_time"] = datetime.datetime.now(
            session["start_time"].tzinfo)

        self.score_service.save_quiz_result(
            username=session["username"],
            subject_name=session["subject_name"],
            score=session["score"],
            total_questions=len(session["questions"])
        )

        from services.score_service import ScoreService
        total = len(session["questions"])
        percentage = round((session["score"] / total) * 100, 2)
        grade = ScoreService.calculate_grade(percentage)

        summary = {
            "username": session["username"],
            "subject_name": session["subject_name"],
            "score": session["score"],
            "total_questions": total,
            "percentage": percentage,
            "grade": grade
        }

        del self.active_sessions[session_id]
        return summary
