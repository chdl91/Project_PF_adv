"""
Presentation Layer - CLI (Stories 1-8)

QuizCLI handles all user input and terminal output.
All business logic lives in the services and QuizSessionService.
Swap this class for QuizGUI to move to a browser interface without
touching any other layer.
"""

from typing import Optional


class QuizCLI:
    """Command-line interface for the quiz application."""

    def __init__(self, user_service, subject_service, question_service, score_service, quiz_session_service):
        self.user_service = user_service
        self.subject_service = subject_service
        self.question_service = question_service
        self.score_service = score_service
        self.quiz_session_service = quiz_session_service

    def run(self):
        """Entry point: login then route to user or admin mode."""
        user = self.login()
        if user["admin_status"]:
            print("\nLaunching Admin Mode...")
            self.admin_mode(user["user_name"])
        else:
            print("\nLaunching User Mode...")
            self.user_mode(user["user_name"])

    def login(self) -> dict:
        """Login or create a new account. Returns user info dict."""
        print("\n" + "=" * 60)
        print("  WELCOME TO QUIZ APPLICATION")
        print("=" * 60)

        username = input("\nEnter your username: ").strip()
        if not username:
            print(" Username cannot be empty!")
            return self.login()

        try:
            user_info = self.user_service.get_or_create_user(username)

            if user_info["is_new"]:
                print(f" Welcome, {username}! Your account has been created.")
            else:
                print(f" Welcome back, {username}!")

            print("  [ADMIN ACCESS]" if user_info["admin_status"] else "  [USER ACCESS]")
            return user_info

        except Exception as e:
            print(f" Error during login: {e}")
            print("Please try again.")
            return self.login()

    def print_menu(self, options: list) -> int:
        """Display a numbered menu and return the validated 1-based selection."""
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = input("Select an option: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Invalid choice. Please try again.")
            return self.print_menu(options)
        return int(choice)

    def get_input(self, prompt: str) -> str:
        """Prompt for non-empty input, retrying until satisfied."""
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            return self.get_input(prompt)
        return value

    def select_subject(self) -> Optional[str]:
        """Let the user pick a subject. Returns None if none exist."""
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            print("No subjects available. Please contact admin.")
            return None
        print("\nAvailable Subjects:")
        return subjects[self.print_menu(subjects) - 1]

    def select_difficulty(self) -> Optional[str]:
        """Returns lowercase 'easy'/'medium'/'hard', or None for all."""
        difficulties = ["Easy", "Medium", "Hard", "All difficulties"]
        print("\nSelect Difficulty:")
        choice = self.print_menu(difficulties)
        return None if choice == 4 else difficulties[choice - 1].lower()

    def select_num_questions(self, max_questions: int = 20) -> int:
        """Ask how many questions to answer (5 to max_questions)."""
        min_q = 5
        num = input(f"\nHow many questions? ({min_q}-{max_questions}): ").strip()
        if not num.isdigit() or int(num) < min_q or int(num) > max_questions:
            print(f"Please enter a number between {min_q} and {max_questions}.")
            return self.select_num_questions(max_questions)
        return int(num)

    def view_scoreboard(self):
        """Display the top 10 scores (Story 7)."""
        print("\n" + "=" * 60)
        print("  TOP 10 SCORES")
        print("=" * 60)

        scores = self.score_service.get_top_scores(limit=10)
        if not scores:
            print("\nNo scores yet. Be the first to take a quiz!")
            return

        print(f"\n{'Rank':<6}{'Username':<18}{'Subject':<26}{'Score':<10}{'Date'}")
        print("-" * 70)
        for i, entry in enumerate(scores, 1):
            username = entry["username"][:15]
            subject = entry["subject"][:23]
            score = f"{entry['score']}/{entry['total']}"
            timestamp = entry["timestamp"][:16] if entry["timestamp"] else "N/A"
            print(f"{i:<6}{username:<18}{subject:<26}{score:<10}{timestamp}")

    def run_quiz(
        self,
        username: str,
        subject_name: str,
        num_questions: int,
        difficulty: Optional[str] = None
    ):
        """Run a complete quiz session (Stories 2, 3, 5, 6)."""
        print("\n" + "=" * 60)
        print(f"  STARTING QUIZ - {subject_name}")
        print("=" * 60)

        try:
            session_id, current_question = self.quiz_session_service.start_quiz_session(
                username=username,
                subject_name=subject_name,
                num_questions=num_questions,
                difficulty=difficulty
            )
            print(f"\nQuiz started! {num_questions} questions.\n")

            question_num = 1
            while True:
                print("-" * 60)
                print(f"Question {question_num}/{num_questions}  [{current_question['difficulty'].upper()}]")
                print("-" * 60)
                print(f"\n{current_question['question_text']}\n")

                answers = current_question["answers"]
                for i, answer in enumerate(answers, 1):
                    print(f"{i}. {answer['text']}")

                while True:
                    try:
                        choice = int(input("\nYour answer (1-4): ").strip())
                        if 1 <= choice <= len(answers):
                            selected_answer_id = answers[choice - 1]["answer_id"]
                            break
                        print(f"Please enter a number between 1 and {len(answers)}")
                    except ValueError:
                        print("Please enter a valid number")

                result = self.quiz_session_service.submit_answer(session_id, selected_answer_id)

                if result["is_correct"]:
                    print("\nCORRECT!")
                else:
                    print("\nWrong answer.")
                    correct_id = current_question["correct_answer_id"]
                    correct = next(a for a in answers if a["answer_id"] == correct_id)
                    print(f"Correct answer: {correct['text']}")

                print(f"Score: {result['score']}/{result['total_questions']}")

                if result["quiz_complete"]:
                    print("\n" + "=" * 60)
                    print("QUIZ COMPLETE!")
                    print("=" * 60)
                    break

                current_question = result["next_question"]
                question_num += 1
                input("\nPress Enter for next question...")

            final = self.quiz_session_service.end_quiz_session(session_id)
            print("\n" + "=" * 60)
            print("  FINAL RESULTS")
            print("=" * 60)
            print(f"Username:    {final['username']}")
            print(f"Subject:     {final['subject_name']}")
            print(f"Score:       {final['score']}/{final['total_questions']}")
            print(f"Percentage:  {final['percentage']}%")
            print(f"Grade:       {final['grade']}/6")
            print("\nResults saved to database!")

        except Exception as e:
            print(f"\nError: {e}")

    def user_mode(self, username: str):
        """User menu: Take a Quiz, View Scoreboard, Logout (Stories 1-7)."""
        while True:
            print("\n" + "=" * 60)
            print(f"  USER MENU - Welcome {username}")
            print("=" * 60)

            choice = self.print_menu(["Take a Quiz", "View Scoreboard", "Logout"])

            if choice == 1:
                subject = self.select_subject()
                if not subject:
                    continue

                difficulty = self.select_difficulty()

                topics = self.subject_service.get_topics_with_ids_by_subject(subject)
                available = []
                for topic in topics:
                    available.extend(
                        self.question_service.get_questions_with_answers(topic["topic_id"], difficulty)
                    )

                if not available:
                    print("No questions available for this subject/difficulty combination.")
                    continue

                num_questions = self.select_num_questions(len(available))
                self.run_quiz(username, subject, num_questions, difficulty)

            elif choice == 2:
                self.view_scoreboard()

            elif choice == 3:
                print(f"\nGoodbye, {username}!")
                break

    def admin_mode(self, username: str):
        """Admin menu: manage subjects, topics, questions (Story 8)."""
        while True:
            print("\n" + "=" * 60)
            print(f"  ADMIN MENU - Welcome {username}")
            print("=" * 60)

            choice = self.print_menu([
                "Add Subject", "Add Topic", "Add Question", "Delete Question", "Logout"
            ])

            if choice == 1:
                name = self.get_input("\nEnter subject name: ")
                if self.subject_service.add_subject(name):
                    print("Subject added successfully!")
                else:
                    print("Failed to add subject (might already exist)")

            elif choice == 2:
                subject = self.select_subject()
                if subject:
                    subject_id = self.subject_service.get_subject_id_by_name(subject)
                    if subject_id:
                        topic_name = self.get_input("\nEnter topic name: ")
                        if self.subject_service.add_topic(topic_name, subject_id):
                            print("Topic added successfully!")

            elif choice == 3:
                subject = self.select_subject()
                if subject:
                    topics = self.subject_service.get_topics_with_ids_by_subject(subject)
                    if topics:
                        print("\nSelect topic:")
                        topic_idx = self.print_menu([t["topic_name"] for t in topics])
                        topic_id = topics[topic_idx - 1]["topic_id"]

                        question_text = self.get_input("Enter question: ")
                        answers = [self.get_input(f"Answer {i}: ") for i in range(1, 5)]

                        while True:
                            try:
                                correct_idx = int(input("\nWhich answer is correct? (1-4): "))
                                if 1 <= correct_idx <= 4:
                                    correct_idx -= 1
                                    break
                                print("Please enter 1-4")
                            except ValueError:
                                print("Please enter a number")

                        difficulty = self.select_difficulty() or "medium"
                        if self.question_service.add_question(
                            topic_id, question_text, answers, correct_idx, difficulty
                        ):
                            print("Question added successfully!")

            elif choice == 4:
                qid_str = self.get_input("Enter question ID to delete: ")
                try:
                    if self.question_service.delete_question(int(qid_str)):
                        print("Question deleted successfully!")
                except ValueError:
                    print("Invalid question ID")

            elif choice == 5:
                print(f"\nGoodbye, {username}!")
                break
