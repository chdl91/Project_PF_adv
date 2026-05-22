"""
Presentation Layer - NiceGUI browser interface (Stories 1-8)

QuizGUI receives the same services as QuizCLI so no business logic changes
when switching from CLI to browser.
"""

from typing import Optional

from nicegui import app, ui


class QuizGUI:
    def __init__(self, user_service, subject_service, question_service, score_service, quiz_session_service, admin_users=None, admin_password: str = ""):
        self.user_service = user_service
        self.subject_service = subject_service
        self.question_service = question_service
        self.score_service = score_service
        self.quiz_session_service = quiz_session_service
        self.admin_users = {user.lower() for user in (admin_users or [])}
        self.admin_password = admin_password

        self.state = {"username": "", "admin_status": False}

        # UI element references (assigned in run())
        self.login_card: Optional[ui.card] = None
        self.app_card: Optional[ui.column] = None
        self.user_panel: Optional[ui.column] = None
        self.admin_panel: Optional[ui.column] = None
        self.username_input: Optional[ui.input] = None
        self.password_input: Optional[ui.input] = None
        self.admin_checkbox: Optional[ui.checkbox] = None
        self.welcome_label: Optional[ui.label] = None
        self.role_label: Optional[ui.label] = None

    def refresh_screen(self):
        logged_in = bool(self.state["username"])
        self.login_card.visible = not logged_in
        self.app_card.visible = logged_in
        self.admin_panel.visible = logged_in and self.state["admin_status"]
        self.user_panel.visible = logged_in and not self.state["admin_status"]

    def login_user(self):
        username = self.username_input.value.strip()
        if not username:
            ui.notify("Username cannot be empty")
            return
        try:
            user_info = self.user_service.get_or_create_user(username)
        except Exception as exc:
            ui.notify(f"Login failed: {exc}")
            return
        entered_password = (self.password_input.value or "").strip()
        # Determine admin intent: checkbox explicit OR username listed as admin
        wants_admin = False
        if hasattr(self, "admin_checkbox") and self.admin_checkbox is not None:
            wants_admin = bool(self.admin_checkbox.value)
        # If user explicitly wants admin, require password
        if wants_admin:
            if not entered_password:
                ui.notify("Enter admin password to login as administrator")
                return
            if entered_password != self.admin_password:
                ui.notify("Invalid admin password")
                return

        self.state["username"] = user_info["user_name"]
        self.state["admin_status"] = (
            user_info["admin_status"] or wants_admin or username.lower(
            ) in self.admin_users
        )
        self.welcome_label.text = f"Welcome, {self.state['username']}"
        # Set role label text and styling for admin vs user
        if self.state["admin_status"]:
            self.role_label.text = "Admin access"
            # make it bold and red
            try:
                self.role_label.classes("text-weight-bold")
            except Exception:
                pass
            self.role_label.style("color: #dc2626; font-weight: 700;")
        else:
            self.role_label.text = "User access"
            # remove admin styling
            try:
                self.role_label.classes("")
            except Exception:
                pass
            self.role_label.style("")
        self.refresh_screen()
        ui.notify(f"Logged in as {self.state['username']}")

    def logout_user(self):
        self.state["username"] = ""
        self.state["admin_status"] = False
        self.username_input.value = ""
        self.password_input.value = ""
        self.welcome_label.text = ""
        # clear role label and styling
        self.role_label.text = ""
        try:
            self.role_label.classes("")
        except Exception:
            pass
        self.role_label.style("")
        self.refresh_screen()
        ui.notify("Logged out")

    def open_subject_menu(self):
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            ui.notify("No subjects available")
            return

        with ui.dialog() as dlg:
            with ui.card().classes("w-96"):
                ui.label("Select a Quiz Subject:").classes("text-h6")
                ui.label("Subject")
                subject_select = ui.select(subjects)
                ui.label("Topics")
                topic_select = ui.select([], multiple=True)
                select_all_topics = ui.checkbox("Select all topics")

                def update_topics():
                    subject = subject_select.value
                    if not subject:
                        topic_select.options = []
                        topic_select.value = []
                        select_all_topics.value = False
                        topic_select.update()
                        select_all_topics.update()
                        return

                    topics = self.subject_service.get_topics_with_ids_by_subject(
                        subject)
                    topic_options = [topic["topic_name"] for topic in topics]
                    topic_select.options = topic_options
                    topic_select.value = topic_options if select_all_topics.value else []
                    topic_select.update()

                def toggle_all_topics():
                    if select_all_topics.value:
                        topic_select.value = list(topic_select.options)
                    else:
                        topic_select.value = []
                    topic_select.update()

                subject_select.on("update:model-value",
                                  lambda _: update_topics())
                select_all_topics.on("update:model-value",
                                     lambda _: toggle_all_topics())
                ui.label("Difficulty")
                difficulty_select = ui.select(
                    ["Easy", "Medium", "Hard", "All difficulties"],
                    value="Medium",
                )
                ui.label("Number of questions")
                num_questions_input = ui.number(value=5, min=5, step=1)

                def start_selected_quiz():
                    subject = subject_select.value
                    if not subject:
                        ui.notify("Select a subject")
                        return

                    selected_topics = topic_select.value or []
                    if not selected_topics:
                        ui.notify("Select at least one topic")
                        return

                    if select_all_topics.value:
                        selected_topics = list(topic_select.options)

                    difficulty = None if difficulty_select.value == "All difficulties" else difficulty_select.value.lower()

                    topics = self.subject_service.get_topics_with_ids_by_subject(
                        subject)
                    selected_topic_ids = []
                    for topic_name in selected_topics:
                        selected_topic = next(
                            (item for item in topics if item["topic_name"]
                             == topic_name),
                            None,
                        )
                        if not selected_topic:
                            ui.notify("Select valid topics")
                            return
                        selected_topic_ids.append(selected_topic["topic_id"])

                    available = []
                    for topic_id in selected_topic_ids:
                        available.extend(
                            self.question_service.get_questions_with_answers(
                                topic_id, difficulty)
                        )

                    if not available:
                        ui.notify("No questions available for that selection")
                        return

                    num_q = int(num_questions_input.value)
                    if num_q < 5:
                        ui.notify("Choose at least 5 questions")
                        return
                    if num_q > len(available):
                        ui.notify(f"Only {len(available)} questions available")
                        return

                    try:
                        session_id, first_question = self.quiz_session_service.start_quiz_session(
                            username=self.state["username"],
                            subject_name=subject,
                            num_questions=num_q,
                            difficulty=difficulty,
                            topic_names=selected_topics,
                        )
                    except Exception as exc:
                        ui.notify(f"Could not start quiz: {exc}")
                        return

                    dlg.close()
                    self.show_question_dialog(session_id, first_question)

                ui.button("Start Quiz", on_click=start_selected_quiz)
                ui.button("Cancel", on_click=dlg.close)

        dlg.open()

    def show_question_dialog(self, session_id: str, question: dict):
        with ui.dialog() as dlg:
            with ui.card().classes("w-[32rem]"):
                ui.label(question.get("question_text", "Question")
                         ).classes("text-h6")
                ui.label(f"Difficulty: {question.get('difficulty', 'n/a')}")

                answer_buttons = []

                def answer_clicked(answer_id: int):
                    try:
                        result = self.quiz_session_service.submit_answer(
                            session_id, answer_id)
                    except Exception as exc:
                        ui.notify(f"Error submitting answer: {exc}")
                        return

                    # Disable all answer buttons
                    for btn in answer_buttons:
                        btn.disable()

                    # Show answer feedback dialog
                    with ui.dialog() as feedback_dlg:
                        with ui.card().classes("w-96"):
                            # Show if answer was correct or wrong
                            feedback_text = "✓ Correct!" if result["is_correct"] else "✗ Wrong answer"
                            feedback_color = "#10b981" if result["is_correct"] else "#ef4444"
                            ui.label(feedback_text).classes(
                                "text-h6").style(f"color: {feedback_color}; font-weight: 700;")

                            # Show the correct answer
                            ui.label("Correct answer:").classes(
                                "text-subtitle2 font-bold")
                            ui.label(result["correct_answer_text"]).classes(
                                "text-base").style("padding: 8px; background-color: #f3f4f6; border-radius: 4px;")

                            def continue_quiz():
                                feedback_dlg.close()
                                dlg.close()

                                if result["quiz_complete"]:
                                    summary = self.quiz_session_service.end_quiz_session(
                                        session_id)
                                    with ui.dialog() as summary_dlg:
                                        with ui.card().classes("w-80"):
                                            ui.label("Quiz complete!").classes(
                                                "text-h6")
                                            ui.label(
                                                f"Score: {summary['score']}/{summary['total_questions']}")
                                            ui.label(
                                                f"Percentage: {summary['percentage']}%")
                                            ui.label(
                                                f"Grade: {summary['grade']}/6")
                                            ui.button(
                                                "OK", on_click=summary_dlg.close)
                                    summary_dlg.open()
                                else:
                                    self.show_question_dialog(
                                        session_id, result["next_question"])

                            ui.button("Next Question",
                                      on_click=continue_quiz).classes("w-full")

                    feedback_dlg.open()

                for answer in question.get("answers", []):
                    btn = ui.button(
                        answer["text"],
                        on_click=lambda a=answer["answer_id"]: answer_clicked(
                            a),
                    ).classes("w-full")
                    answer_buttons.append(btn)

                def quit_quiz():
                    try:
                        summary = self.quiz_session_service.end_quiz_session(
                            session_id)
                    except Exception as exc:
                        ui.notify(f"Could not quit quiz: {exc}")
                        return

                    dlg.close()
                    with ui.dialog() as summary_dlg:
                        with ui.card().classes("w-80"):
                            ui.label("Quiz aborted").classes("text-h6")
                            ui.label(
                                f"Score: {summary['score']}/{summary['total_questions']}")
                            ui.label(
                                f"Percentage: {summary['percentage']}%")
                            ui.label(f"Grade: {summary['grade']}/6")
                            ui.button("OK", on_click=summary_dlg.close)
                    summary_dlg.open()

                with ui.row().classes("w-full"):
                    ui.button("Quit Quiz", on_click=quit_quiz).props("color=negative").classes("w-full").style(
                        "background-color: #dc2626 !important; color: white !important;")

        dlg.open()

    def view_scoreboard(self):
        scores = self.score_service.get_top_scores(limit=10)
        with ui.dialog() as dlg:
            with ui.card().classes("w-[36rem]"):
                ui.label("Top 10 Scores").classes("text-h6")
                if not scores:
                    ui.label("No scores yet.")
                else:
                    for idx, score in enumerate(scores, 1):
                        ui.label(
                            f"{idx}. {score['username']} — {score['subject']} — {score['score']}/{score['total']} ({score['timestamp'][:16]})")
                ui.button("Close", on_click=dlg.close)
        dlg.open()

    def add_subject_dialog(self):
        with ui.dialog() as dlg:
            with ui.card().classes("w-96"):
                ui.label("Add Subject").classes("text-h6")
                subject_input = ui.input("Subject name")

                def save_subject():
                    if self.subject_service.add_subject(subject_input.value.strip()):
                        ui.notify("Subject added")
                        dlg.close()
                    else:
                        ui.notify(
                            "Could not add subject (might already exist)")

                ui.button("Save", on_click=save_subject)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def add_topic_dialog(self):
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            ui.notify("No subjects available")
            return

        with ui.dialog() as dlg:
            with ui.card().classes("w-96"):
                ui.label("Add Topic").classes("text-h6")
                subject_select = ui.select(subjects, label="Subject")
                topic_input = ui.input("Topic name")

                def save_topic():
                    subject_id = self.subject_service.get_subject_id_by_name(
                        subject_select.value)
                    if not subject_id:
                        ui.notify("Select a valid subject")
                        return
                    if self.subject_service.add_topic(topic_input.value.strip(), subject_id):
                        ui.notify("Topic added")
                        dlg.close()
                    else:
                        ui.notify("Could not add topic")

                ui.button("Save", on_click=save_topic)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def add_question_dialog(self):
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            ui.notify("No subjects available")
            return

        with ui.dialog() as dlg:
            with ui.card().classes("w-[40rem]"):
                ui.label("Add Question").classes("text-h6")
                subject_select = ui.select(subjects, label="Subject")
                topic_select = ui.select([], label="Topic")

                def update_topics():
                    subject = subject_select.value
                    if not subject:
                        return
                    topics = self.subject_service.get_topics_with_ids_by_subject(
                        subject)
                    topic_select.options = [t["topic_name"] for t in topics]
                    topic_select.update()

                ui.button("Load Topics", on_click=update_topics)

                question_input = ui.input("Question text")
                answer_inputs = [ui.input(f"Answer {i}") for i in range(1, 5)]
                correct_input = ui.number(
                    "Correct answer number (1-4)", value=1, min=1, max=4)
                difficulty_input = ui.select(
                    ["easy", "medium", "hard"], value="medium", label="Difficulty")

                def save_question():
                    subject = subject_select.value
                    topic_name = topic_select.value
                    if not subject or not topic_name:
                        ui.notify("Select subject and topic")
                        return

                    topics = self.subject_service.get_topics_with_ids_by_subject(
                        subject)
                    topic = next(
                        (t for t in topics if t["topic_name"] == topic_name), None)
                    if not topic:
                        ui.notify("Invalid topic")
                        return

                    answers = [f.value.strip() for f in answer_inputs]
                    if any(not a for a in answers):
                        ui.notify("Fill in all answer fields")
                        return

                    if self.question_service.add_question(
                        topic_id=topic["topic_id"],
                        text=question_input.value.strip(),
                        answers=answers,
                        correct_idx=int(correct_input.value) - 1,
                        difficulty=difficulty_input.value,
                    ):
                        ui.notify("Question added")
                        dlg.close()
                    else:
                        ui.notify("Could not add question")

                ui.button("Save", on_click=save_question)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def delete_topic_dialog(self):
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            ui.notify("No subjects available")
            return

        with ui.dialog() as dlg:
            with ui.card().classes("w-96"):
                ui.label("Delete Topic").classes("text-h6")
                subject_select = ui.select(subjects, label="Subject")
                topic_select = ui.select([], label="Topic")

                def load_topics():
                    subject = subject_select.value
                    if not subject:
                        return
                    topics = self.subject_service.get_topics_with_ids_by_subject(subject)
                    topic_select.options = [t["topic_name"] for t in topics]
                    topic_select.update()

                ui.button("Load Topics", on_click=load_topics)

                def remove_topic():
                    subject = subject_select.value
                    topic_name = topic_select.value
                    if not subject or not topic_name:
                        ui.notify("Select a subject and topic")
                        return
                    topics = self.subject_service.get_topics_with_ids_by_subject(subject)
                    topic = next((t for t in topics if t["topic_name"] == topic_name), None)
                    if not topic:
                        ui.notify("Invalid topic")
                        return

                    with ui.dialog() as confirm_dlg:
                        with ui.card().classes("w-96"):
                            ui.label(f"Delete topic '{topic_name}' and all its questions?").classes("text-h6")
                            with ui.row():
                                def confirm_delete():
                                    if self.subject_service.delete_topic(topic["topic_id"]):
                                        ui.notify("Topic deleted")
                                        dlg.close()
                                        confirm_dlg.close()
                                    else:
                                        ui.notify("Could not delete topic")
                                        confirm_dlg.close()
                                ui.button("Yes, Delete", on_click=confirm_delete).classes("bg-red-500")
                                ui.button("Cancel", on_click=confirm_dlg.close).classes("bg-gray-500")
                    confirm_dlg.open()

                ui.button("Delete", on_click=remove_topic)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def delete_subject_dialog(self):
        subjects = self.subject_service.get_all_subjects()
        if not subjects:
            ui.notify("No subjects available")
            return

        with ui.dialog() as dlg:
            with ui.card().classes("w-96"):
                ui.label("Delete Subject").classes("text-h6")
                subject_select = ui.select(subjects, label="Subject")

                def remove_subject():
                    subject_name = subject_select.value
                    if not subject_name:
                        ui.notify("Select a subject")
                        return
                    subject_id = self.subject_service.get_subject_id_by_name(subject_name)
                    if not subject_id:
                        ui.notify("Invalid subject")
                        return

                    with ui.dialog() as confirm_dlg:
                        with ui.card().classes("w-96"):
                            ui.label(f"Delete subject '{subject_name}' and ALL its topics and questions?").classes("text-h6")
                            with ui.row():
                                def confirm_delete():
                                    if self.subject_service.delete_subject(subject_id):
                                        ui.notify("Subject deleted")
                                        dlg.close()
                                        confirm_dlg.close()
                                    else:
                                        ui.notify("Could not delete subject")
                                        confirm_dlg.close()
                                ui.button("Yes, Delete", on_click=confirm_delete).classes("bg-red-500")
                                ui.button("Cancel", on_click=confirm_dlg.close).classes("bg-gray-500")
                    confirm_dlg.open()

                ui.button("Delete", on_click=remove_subject)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def delete_question_dialog(self):
        with ui.dialog() as dlg:
            with ui.card().classes("w-80"):
                ui.label("Delete Question").classes("text-h6")
                question_id_input = ui.number("Question ID", min=1)

                def remove_question():
                    try:
                        qid = int(question_id_input.value)
                    except Exception:
                        ui.notify("Enter a valid question ID")
                        return

                    # Show confirmation dialog
                    with ui.dialog() as confirm_dlg:
                        with ui.card().classes("w-96"):
                            ui.label(f"Are you sure you want to delete question with ID {qid}?").classes(
                                "text-h6")

                            def confirm_delete():
                                if self.question_service.delete_question(qid):
                                    ui.notify("Question deleted successfully")
                                    dlg.close()
                                    confirm_dlg.close()
                                else:
                                    ui.notify("Could not delete question")
                                    confirm_dlg.close()

                            with ui.row():
                                ui.button("Yes, Delete", on_click=confirm_delete).classes(
                                    "bg-red-500")
                                ui.button("Cancel", on_click=confirm_dlg.close).classes(
                                    "bg-gray-500")

                    confirm_dlg.open()

                ui.button("Delete", on_click=remove_question)
                ui.button("Cancel", on_click=dlg.close)
        dlg.open()

    def run(self):
        with ui.column().classes("items-center justify-center w-full").style("min-height: 100vh;"):
            ui.label("Quiz Application").classes("text-h4")

            with ui.card().classes("w-96") as self.login_card:
                ui.label("Login").classes("text-h6")
                self.username_input = ui.input("Username")
                self.admin_checkbox = ui.checkbox("Login as administrator")
                self.password_input = ui.input(
                    "Admin password", password=True, password_toggle_button=True)
                self.password_input.visible = False

                def _update_password_visibility(_=None):
                    uname = (self.username_input.value or "").strip().lower()
                    show = bool(self.admin_checkbox.value) or (
                        uname in self.admin_users)
                    self.password_input.visible = show
                    self.password_input.update()

            self.username_input.on("update:model-value",
                                   _update_password_visibility)
            self.admin_checkbox.on("update:model-value",
                                   _update_password_visibility)
            ui.button("Login", on_click=self.login_user)

            with ui.column().classes("gap-2 items-center") as self.app_card:
                self.welcome_label = ui.label("")
                self.role_label = ui.label("")

                with ui.column().classes("items-center") as self.user_panel:
                    ui.label("User menu").classes("text-h6 text-weight-bold")

                with ui.row().classes("justify-center"):
                    ui.button("Take a Quiz", on_click=self.open_subject_menu)
                    ui.button("View Scoreboard", on_click=self.view_scoreboard)
                    ui.button("Logout", on_click=self.logout_user)

                with ui.column().classes("items-center") as self.admin_panel:
                    ui.label("Admin menu").classes("text-h6 text-weight-bold")
                    ui.label("Subject & Topic management")
                    with ui.row().classes("justify-center"):
                        ui.button("Add Subject", on_click=self.add_subject_dialog)
                        ui.button("Add Topic", on_click=self.add_topic_dialog)
                    with ui.row().classes("justify-center"):
                        ui.button("Delete Topic", on_click=self.delete_topic_dialog)
                        ui.button("Delete Subject", on_click=self.delete_subject_dialog)
                    ui.label("Question management")
                    with ui.row().classes("justify-center"):
                        ui.button("Add Question",
                                  on_click=self.add_question_dialog)
                        ui.button("Delete Question",
                                  on_click=self.delete_question_dialog)

        self.refresh_screen()
        ui.run(port=8080, reload=False)
