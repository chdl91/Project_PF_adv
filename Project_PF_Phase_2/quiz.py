"""
Quiz CLI Interface - User and Admin Modes (Stories 1-8)

Main entry point for the quiz application.
- User Mode: Take quizzes, view scores
- Admin Mode: Add/remove questions, topics, subjects
"""

from quiz_service import (
    get_or_create_user,
    get_all_subjects,
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
        # admin_mode()  # We'll build this next
        print("[Admin Mode - Coming Soon]")
    else:
        print("\n🎮 Launching User Mode...")
        # user_mode()  # We'll build this next
        print("[User Mode - Coming Soon]")


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


def select_subject() -> str:
    subject = get_all_subjects()
    if not subject:
        print("No subjects available. Please contact admin.")
        return None
    print("\nAvailable Subjects:")
    choice = print_menu(subject)
    return subject[choice - 1]


def select_difficulty() -> str:
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


if __name__ == "__main__":
    main()
