"""
Quiz CLI Interface - User and Admin Modes (Stories 1-8)

Main entry point for the quiz application.
- User Mode: Take quizzes, view scores
- Admin Mode: Add/remove questions, topics, subjects
"""

from typing import Optional

from quiz_service import (
    get_or_create_user,
    get_all_subjects,
    get_subject_id_by_name,
    get_topics_with_ids_by_subject,
    get_questions_with_answers,
    get_top_scores,
    add_subject,
    add_topic,
    add_question,
    delete_question,
    delete_topic,
    delete_subject
)

from quiz_engine import (
    start_quiz_session,
    submit_answer,
    get_quiz_progress,
    end_quiz_session,
    ACTIVE_SESSIONS
)


def login() -> dict:
    """
    Login or create new user account.

    **Purpose:**
    Authenticate user. If username doesn't exist, create new account.
    Determine if user is admin or regular user.

    **Flow:**
    1. Ask user for username
    2. Call get_or_create_user() from quiz_service
    3. Return user info including admin_status

    **Returns:**
    {
        "user_id": int,
        "user_name": str,
        "admin_status": bool,  # True = Admin, False = Regular User
        "is_new": bool         # True if just created
    }
    """
    print("\n" + "=" * 60)
    print("  WELCOME TO QUIZ APPLICATION")
    print("=" * 60)

    username = input("\nEnter your username: ").strip()

    if not username:
        print(" Username cannot be empty!")
        return login()  # Ask again

    try:
        user_info = get_or_create_user(username)

        # Show welcome message
        if user_info["is_new"]:
            print(f" Welcome, {username}! Your account has been created.")
        else:
            print(f" Welcome back, {username}!")

        # Show access level
        if user_info["admin_status"]:
            print("  [ADMIN ACCESS]")
        else:
            print("  [USER ACCESS]")

        return user_info

    except Exception as e:
        print(f" Error during login: {e}")
        print("Please try again.")
        return login()


def main():
    """
    Main entry point for the application.
    """
    # Step 1: Login
    user = login()

    # Step 2: Route based on admin status
    if user["admin_status"]:
        print("\n📋 Launching Admin Mode...")
        admin_mode(user["user_name"])
    else:
        print("\n🎮 Launching User Mode...")
        user_mode(user["user_name"])


def print_menu(options: list) -> int:
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Select an option: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("Invalid choice. Please try again.")
        return print_menu(options)
    return int(choice)


def get_input(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        print("Input cannot be empty. Please try again.")
        return get_input(prompt)
    return value


def select_subject() -> Optional[str]:
    subject = get_all_subjects()
    if not subject:
        print("No subjects available. Please contact admin.")
        return None
    print("\nAvailable Subjects:")
    choice = print_menu(subject)
    return subject[choice - 1]


def select_difficulty() -> Optional[str]:
    """
    Let user select difficulty level (or all).

    Returns lowercase: "easy", "medium", "hard", or None (for all)
    """
    difficulties = ["Easy", "Medium", "Hard", "All difficulties"]
    print("\nSelect Difficulty:")
    choice = print_menu(difficulties)

    if choice == 4:
        return None  # "All difficulties" means no filter

    return difficulties[choice - 1].lower()  # Convert to lowercase


def select_num_questions(max_questions: int = 20) -> int:
    """
    Ask user how many questions to answer.

    Args:
        max_questions: Maximum questions available (default 20)

    Returns:
        int: Number of questions (5 to max_questions)
    """
    min_questions = 5
    prompt = f"\nHow many questions would you like? ({min_questions}-{max_questions}): "
    num = input(prompt).strip()

    if not num.isdigit() or int(num) < min_questions or int(num) > max_questions:
        print(
            f"Please enter a number between {min_questions} and {max_questions}.")
        return select_num_questions(max_questions)

    return int(num)


def view_scoreboard():
    """Display top 10 scores (Story 7)."""
    print("\n" + "=" * 60)
    print("  TOP 10 SCORES")
    print("=" * 60)

    scores = get_top_scores(limit=10)

    if not scores:
        print("\n📊 No scores yet. Be the first to take a quiz!")
        return

    print(f"\n{'Rank':<6}{'Username':<20}{'Score':<15}{'Date':<20}")
    print("-" * 60)

    for i, score_entry in enumerate(scores, 1):
        username = score_entry["username"][:15]
        score = score_entry["score"]
        timestamp = score_entry["timestamp"][:
                                             16] if score_entry["timestamp"] else "N/A"

        print(f"{i:<6}{username:<20}{score:<15}{timestamp:<20}")


def run_quiz(username: str, subject_name: str, num_questions: int, difficulty: Optional[str] = None):
    """
    Run a complete quiz session (Stories 2, 3, 5, 6).
    """
    print("\n" + "=" * 60)
    print(f"  STARTING QUIZ - {subject_name}")
    print("=" * 60)

    try:
        # Start quiz session
        session_id, first_question = start_quiz_session(
            username=username,
            subject_name=subject_name,
            num_questions=num_questions,
            difficulty=difficulty
        )

        print(f"\n✓ Quiz started! {num_questions} questions.\n")

        question_num = 1

        # Quiz loop
        while True:
            # Display question
            print("-" * 60)
            print(f"Question {question_num}/{num_questions}")
            print(f"Difficulty: {first_question['difficulty'].upper()}")
            print("-" * 60)
            print(f"\n{first_question['question_text']}\n")

            # Display answers
            answers = first_question["answers"]
            for i, answer in enumerate(answers, 1):
                print(f"{i}. {answer['text']}")

            # Get user's answer
            while True:
                try:
                    answer_choice = int(input("\nYour answer (1-4): ").strip())
                    if 1 <= answer_choice <= len(answers):
                        selected_answer_id = answers[answer_choice -
                                                     1]["answer_id"]
                        break
                    else:
                        print(
                            f"Please enter a number between 1 and {len(answers)}")
                except ValueError:
                    print("Please enter a valid number")

            # Submit answer
            result = submit_answer(session_id, selected_answer_id)

            # Show feedback
            if result["is_correct"]:
                print("\n✓ CORRECT! 🎉")
            else:
                print("\n✗ Wrong answer 😞")
                correct_id = first_question["correct_answer_id"]
                correct_answer = next(
                    a for a in answers if a["answer_id"] == correct_id)
                print(f"Correct answer: {correct_answer['text']}")

            print(f"Score: {result['score']}/{result['total_questions']}")

            # Check if quiz complete
            if result["quiz_complete"]:
                print("\n" + "=" * 60)
                print("✓ QUIZ COMPLETE!")
                print("=" * 60)
                break

            # Next question
            first_question = result["next_question"]
            question_num += 1
            input("\nPress Enter for next question...")

        # End session and show results
        final_stats = end_quiz_session(session_id)

        print("\n" + "=" * 60)
        print("  FINAL RESULTS")
        print("=" * 60)
        print(f"Username:    {final_stats['username']}")
        print(f"Subject:     {final_stats['subject_name']}")
        print(
            f"Score:       {final_stats['score']}/{final_stats['total_questions']}")
        print(f"Percentage:  {final_stats['percentage']}%")
        print(f"Grade:       {final_stats['grade']}/6")
        print("\n✓ Results saved to database!")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def user_mode(username: str):
    """Main user mode menu (Stories 1-7)."""
    while True:
        print("\n" + "=" * 60)
        print(f"  USER MENU - Welcome {username}")
        print("=" * 60)

        options = [
            "Take a Quiz",
            "View Scoreboard",
            "Logout"
        ]

        choice = print_menu(options)

        if choice == 1:
            # Take a quiz
            subject = select_subject()
            if not subject:
                continue

            # Get available questions for this subject+difficulty
            difficulty = select_difficulty()

            topics = get_topics_with_ids_by_subject(subject)
            available_questions = []
            for topic in topics:
                available_questions.extend(
                    get_questions_with_answers(topic["topic_id"], difficulty))

            if not available_questions:
                print(
                    "❌ No questions available for this subject/difficulty combination.")
                continue

            max_q = len(available_questions)
            num_questions = select_num_questions(max_q)

            run_quiz(username, subject, num_questions, difficulty)

        elif choice == 2:
            # View scoreboard
            view_scoreboard()

        elif choice == 3:
            # Logout
            print(f"\n👋 Goodbye, {username}!")
            break


def admin_mode(username: str):
    """Admin mode menu (Story 8)."""
    while True:
        print("\n" + "=" * 60)
        print(f"  ADMIN MENU - Welcome {username}")
        print("=" * 60)

        options = [
            "Add Subject",
            "Add Topic",
            "Add Question",
            "Delete Question",
            "Logout"
        ]

        choice = print_menu(options)

        if choice == 1:
            # Add subject
            subject_name = get_input("\nEnter subject name")
            if add_subject(subject_name):
                print("✓ Subject added successfully!")
            else:
                print("❌ Failed to add subject (might already exist)")

        elif choice == 2:
            # Add topic
            subject = select_subject()
            if subject:
                subject_id = get_subject_id_by_name(subject)
                if subject_id:
                    topic_name = get_input("\nEnter topic name: ")
                    if add_topic(topic_name, subject_id):
                        print("✓ Topic added successfully!")

        elif choice == 3:
            # Add question
            subject = select_subject()
            if subject:
                topics = get_topics_with_ids_by_subject(subject)
                if topics:
                    print("\nSelect topic:")
                    topic_names = [t["topic_name"] for t in topics]
                    choice_idx = print_menu(topic_names)
                    topic_id = topics[choice_idx - 1]["topic_id"]

                    question_text = get_input("Enter question")

                    answers = []
                    print("\nEnter 4 answers:")
                    for i in range(1, 5):
                        answer = get_input(f"Answer {i}")
                        answers.append(answer)

                    while True:
                        try:
                            correct_idx = int(
                                input("\nWhich answer is correct? (1-4): "))
                            if 1 <= correct_idx <= 4:
                                correct_idx -= 1
                                break
                            else:
                                print("Please enter 1-4")
                        except ValueError:
                            print("Please enter a number")

                    difficulty = select_difficulty()
                    if not difficulty:
                        difficulty = "medium"

                    if add_question(topic_id, question_text, answers, correct_idx, difficulty):
                        print("✓ Question added successfully!")

        elif choice == 4:
            # Delete question
            question_id = get_input("Enter question ID to delete")
            try:
                question_id = int(question_id)
                if delete_question(question_id):
                    print("✓ Question deleted successfully!")
            except ValueError:
                print("❌ Invalid question ID")

        elif choice == 5:
            # Logout
            print(f"\n👋 Goodbye, {username}!")
            break


if __name__ == "__main__":
    main()
