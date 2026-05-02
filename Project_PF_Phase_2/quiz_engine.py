"""
Quiz Engine - Core business logic for quiz execution (Stories 2, 3, 5, 6)

In-memory session management:
- Tracks quiz state (current question, answers submitted, score)
- Validates user answers
- Manages quiz progression
- Integrates with quiz_service for data access
"""

import uuid
import datetime
import zoneinfo
import random
from typing import Dict, Optional, Tuple, List
from quiz_service import (
    get_questions_with_answers,
    get_topics_with_ids_by_subject,
    save_quiz_result
)

# Global session storage (in-memory dict)
# Key: session_id (UUID string)
# Value: session_data dict with all quiz state
ACTIVE_SESSIONS: Dict[str, dict] = {}


def start_quiz_session(
    username: str,
    subject_name: str,
    num_questions: int,
    difficulty: Optional[str] = None
) -> Tuple[str, dict]:
    """
    Start a new quiz session and get the first question (Story 2, 3).

    **Purpose:**
    Initialize a quiz session. Called when user clicks "Start Quiz" after
    selecting a subject and difficulty level.

    **What it does:**
    1. Get all topic IDs for the subject
    2. Collect questions from those topics (filtered by difficulty if provided)
    3. Randomly select num_questions from the pool
    4. Create a session dict to track state during the quiz
    5. Store session in ACTIVE_SESSIONS global dict
    6. Return session_id + first question to display

    **Session structure (stored in ACTIVE_SESSIONS):**
    {
        "username": "Alice",
        "subject_name": "Digital Business",
        "difficulty": "easy",
        "questions": [...list of all question dicts...],
        "current_idx": 0,                  # Which question are we on (0-based)
        "user_answers": [3, 1, 4, ...],   # answer_ids user has clicked
        "score": 1,                        # Number correct so far
        "start_time": datetime_object,
        "end_time": None
    }

    Args:
        username (str): Player's username
        subject_name (str): Subject to quiz on (e.g., "Digital Business")
        num_questions (int): How many questions to answer
        difficulty (Optional[str]): Filter by difficulty ("easy", "medium", "hard") or None for all

    Returns:
        Tuple[str, dict]: (session_id, first_question_dict)

    Raises:
        ValueError: If subject not found or not enough questions available
    """
    try:
        topics = get_topics_with_ids_by_subject(subject_name)
        if not topics:
            raise ValueError(f"Subject '{subject_name}' has no topics")

        all_questions = []
        for topic in topics:
            topic_id = topic["topic_id"]
            topic_name = topic["topic_name"]

            questions = get_questions_with_answers(topic_id, difficulty)
            all_questions.extend(questions)

        if not all_questions:
            raise ValueError(
                f"No questions found for subject '{subject_name}' with difficulty {difficulty}"
            )

        if len(all_questions) < num_questions:
            raise ValueError(
                f"Only {len(all_questions)} questions available, but {num_questions} requested"
            )

        selected_questions = random.sample(all_questions, num_questions)

        session_id = str(uuid.uuid4())  # Generate unique session ID
        tz = zoneinfo.ZoneInfo("Europe/Zurich")

        session_data = {
            "username": username,
            "subject_name": subject_name,
            "difficulty": difficulty,
            "questions": selected_questions,
            "current_idx": 0,              # Start at first question
            "user_answers": [],            # No answers yet
            "score": 0,                    # No points yet
            "start_time": datetime.datetime.now(tz),
            "end_time": None
        }

        ACTIVE_SESSIONS[session_id] = session_data

        first_question = selected_questions[0]

        return session_id, first_question

    except Exception as e:
        print(f"Error starting quiz session: {e}")
        raise


def validate_answer(session_id: str, selected_answer_id: int) -> bool:
    """
    Validate the user's answer for the current question (Story 5).

    **Purpose:**
    Check if the user's selected answer is correct.

    **What it does:**
    1. Get the session from ACTIVE_SESSIONS
    2. Get the current question (using current_idx)
    3. Compare user's selected_answer_id with question's correct_answer_id
    4. Return True if correct, False if wrong

    Args:
        session_id (str): UUID of the quiz session
        selected_answer_id (int): The answer ID user clicked

    Returns:
        bool: True if answer is correct, False if wrong
    """
    session = ACTIVE_SESSIONS[session_id]
    current_question = session["questions"][session["current_idx"]]

    is_correct = selected_answer_id == current_question["correct_answer_id"]

    return is_correct


# ============================================================================
# FUNCTION 3: submit_answer() - We'll build this together
# ============================================================================
def submit_answer(session_id: str, selected_answer_id: int) -> dict:
    """
    Submit an answer and get validation + next question (Story 5, 6).

    **Purpose:**
    Process user's answer submission. Called when user clicks an answer option.

    **What it does:**
    1. Validate the answer (call validate_answer)
    2. Store the answer in session
    3. Update score if correct
    4. Advance to next question (current_idx += 1)
    5. Check if quiz is complete
    6. Return feedback with next question

    Args:
        session_id (str): UUID of the quiz session
        selected_answer_id (int): The answer ID user selected

    Returns:
        dict: Feedback dict with structure:
        {
            "is_correct": bool,
            "score": int,
            "current_question_num": int,      # 1-based (question 1, 2, 3...)
            "total_questions": int,
            "next_question": dict or None,    # None if quiz complete
            "quiz_complete": bool
        }
    """
    session = ACTIVE_SESSIONS[session_id]

    is_correct = validate_answer(session_id, selected_answer_id)

    session["user_answers"].append(selected_answer_id)

    if is_correct:
        session["score"] += 1

    session["current_idx"] += 1

    total_questions = len(session["questions"])
    quiz_complete = session["current_idx"] >= total_questions

    next_question = None
    if not quiz_complete:
        next_question = session["questions"][session["current_idx"]]

    # Return feedback
    return {
        "is_correct": is_correct,
        "score": session["score"],
        # Now points to next question
        "current_question_num": session["current_idx"],
        "total_questions": total_questions,
        "next_question": next_question,
        "quiz_complete": quiz_complete
    }


def get_quiz_progress(session_id: str) -> dict:
    session = ACTIVE_SESSIONS[session_id]
    return {
        "current_question_num": session["current_idx"] + 1,
        "score": session["score"],
        "total_questions": len(session["questions"]),
        "percentage": round((session["score"] / len(session["questions"])) * 100, 2)
    }


def end_quiz_session(session_id: str) -> dict:
    """
    End the quiz, save result, and return final stats (Story 6).

    **Purpose:**
    Finalize the quiz, persist results to database, and clean up session.

    **What it does:**
    1. Get the session
    2. Calculate end time
    3. Call save_quiz_result to persist to database (handles Swiss grading)
    4. Delete session from ACTIVE_SESSIONS
    5. Return final summary with score and grade

    Args:
        session_id (str): UUID of the quiz session

    Returns:
        dict: Final stats {username, subject_name, score, total_questions, percentage, etc.}
    """
    session = ACTIVE_SESSIONS[session_id]

    # Store end time
    session["end_time"] = datetime.datetime.now(session["start_time"].tzinfo)

    # Save to database (save_quiz_result handles Swiss grading internally)
    save_quiz_result(
        username=session["username"],
        subject_name=session["subject_name"],
        score=session["score"],
        total_questions=len(session["questions"])
    )

    # Prepare summary
    summary = {
        "username": session["username"],
        "subject_name": session["subject_name"],
        "score": session["score"],
        "total_questions": len(session["questions"]),
        "percentage": round((session["score"] / len(session["questions"])) * 100, 2)
    }

    # Clean up session
    del ACTIVE_SESSIONS[session_id]

    return summary


if __name__ == "__main__":
    """
    Test the complete quiz flow:
    1. Start a quiz session
    2. Submit answers
    3. Check progress
    4. End the quiz
    """
    print("=" * 60)
    print("TESTING QUIZ ENGINE - Complete Flow")
    print("=" * 60)

    try:
        # Step 1: Start a quiz
        print("\n[1] Starting quiz session...")
        session_id, first_question = start_quiz_session(
            username="TestUser",
            subject_name="Digital Business",
            num_questions=5,
            difficulty="easy"
        )
        print(f"✓ Session created: {session_id}")
        print(f"✓ First question: {first_question['question_text'][:60]}...")
        print(f"✓ Correct answer ID: {first_question['correct_answer_id']}")

        # Step 2: Submit some answers
        print("\n[2] Submitting answers...")

        # Answer 1 (let's try the correct answer)
        correct_answer_id = first_question["correct_answer_id"]
        result1 = submit_answer(session_id, correct_answer_id)
        print(
            f"✓ Answer 1: {'CORRECT ✓' if result1['is_correct'] else 'WRONG ✗'}")
        print(f"  Score: {result1['score']}/{result1['total_questions']}")
        print(
            f"  Progress: {result1['current_question_num']}/{result1['total_questions']}")

        # Answer 2 (wrong answer)
        wrong_answer_id = first_question["answers"][0]["answer_id"]
        if wrong_answer_id == correct_answer_id:
            wrong_answer_id = first_question["answers"][1]["answer_id"]

        result2 = submit_answer(session_id, wrong_answer_id)
        print(
            f"✓ Answer 2: {'CORRECT ✓' if result2['is_correct'] else 'WRONG ✗'}")
        print(f"  Score: {result2['score']}/{result2['total_questions']}")

        # Answer 3, 4, 5
        for i in range(3):
            next_q = result2["next_question"] if i == 0 else ACTIVE_SESSIONS[
                session_id]["questions"][ACTIVE_SESSIONS[session_id]["current_idx"]]
            correct_id = next_q["correct_answer_id"]
            result = submit_answer(session_id, correct_id)
            print(
                f"✓ Answer {i+3}: {'CORRECT ✓' if result['is_correct'] else 'WRONG ✗'}")
            print(f"  Score: {result['score']}/{result['total_questions']}")
            result2 = result

        # Step 3: Check progress before ending
        print("\n[3] Final progress check...")
        progress = get_quiz_progress(session_id)
        print(
            f"✓ Current question: {progress['current_question_num']}/{progress['total_questions']}")
        print(f"✓ Score: {progress['score']}/{progress['total_questions']}")
        print(f"✓ Percentage: {progress['percentage']}%")

        # Step 4: End the quiz
        print("\n[4] Ending quiz session...")
        final_stats = end_quiz_session(session_id)
        print(f"✓ Quiz finished!")
        print(f"  Username: {final_stats['username']}")
        print(f"  Subject: {final_stats['subject_name']}")
        print(
            f"  Final Score: {final_stats['score']}/{final_stats['total_questions']} ({final_stats['percentage']}%)")

        # Check that session was cleaned up
        if session_id not in ACTIVE_SESSIONS:
            print(f"✓ Session cleaned up from memory")
        else:
            print(f"✗ WARNING: Session still in memory!")

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
