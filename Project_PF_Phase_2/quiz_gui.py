from nicegui import ui

from quiz_engine import end_quiz_session, start_quiz_session, submit_answer
from quiz_service import (
    add_question,
    add_subject,
    add_topic,
    delete_question,
    get_all_subjects,
    get_or_create_user,
    get_questions_with_answers,
    get_subject_id_by_name,
    get_top_scores,
    get_topics_with_ids_by_subject,
)


state = {
    "username": "",
    "admin_status": False,
}


def refresh_screen() -> None:
    logged_in = bool(state["username"])
    login_card.visible = not logged_in
    app_card.visible = logged_in
    admin_panel.visible = logged_in and state["admin_status"]
    user_panel.visible = logged_in and not state["admin_status"]


def login_user() -> None:
    username = username_input.value.strip()
    if not username:
        ui.notify("Username cannot be empty")
        return

    try:
        user_info = get_or_create_user(username)
    except Exception as exc:
        ui.notify(f"Login failed: {exc}")
        return

    state["username"] = user_info["user_name"]
    state["admin_status"] = user_info["admin_status"]
    welcome_label.text = f"Welcome, {state['username']}"
    role_label.text = "Admin access" if state["admin_status"] else "User access"
    refresh_screen()
    ui.notify(f"Logged in as {state['username']}")


def logout_user() -> None:
    state["username"] = ""
    state["admin_status"] = False
    username_input.value = ""
    welcome_label.text = ""
    role_label.text = ""
    refresh_screen()
    ui.notify("Logged out")


def open_subject_menu() -> None:
    subjects = get_all_subjects()
    if not subjects:
        ui.notify("No subjects available")
        return

    with ui.dialog() as dlg:
        with ui.card().classes("w-96"):
            ui.label("Select a Quiz Subject:").classes("text-h6")
            subject_select = ui.select(subjects, label="Subject")
            difficulty_select = ui.select(
                ["Easy", "Medium", "Hard", "All difficulties"],
                value="Medium",
                label="Difficulty",
            )
            num_questions_input = ui.number(
                label="Number of questions",
                value=5,
                min=5,
                step=1,
            )

            def start_selected_quiz() -> None:
                subject = subject_select.value
                if not subject:
                    ui.notify("Select a subject")
                    return

                difficulty = difficulty_select.value
                if difficulty == "All difficulties":
                    difficulty = None
                else:
                    difficulty = difficulty.lower()

                topics = get_topics_with_ids_by_subject(subject)
                available_questions = []
                for topic in topics:
                    available_questions.extend(
                        get_questions_with_answers(
                            topic["topic_id"], difficulty)
                    )

                if not available_questions:
                    ui.notify("No questions available for that selection")
                    return

                num_questions = int(num_questions_input.value)
                if num_questions < 5:
                    ui.notify("Choose at least 5 questions")
                    return

                if num_questions > len(available_questions):
                    ui.notify(
                        f"Only {len(available_questions)} questions available")
                    return

                try:
                    session_id, first_question = start_quiz_session(
                        username=state["username"],
                        subject_name=subject,
                        num_questions=num_questions,
                        difficulty=difficulty,
                    )
                except Exception as exc:
                    ui.notify(f"Could not start quiz: {exc}")
                    return

                dlg.close()
                show_question_dialog(session_id, first_question)

            ui.button("Start Quiz", on_click=start_selected_quiz)
            ui.button("Cancel", on_click=dlg.close)

    dlg.open()


def show_question_dialog(session_id: str, question: dict) -> None:
    with ui.dialog() as dlg:
        with ui.card().classes("w-[32rem]"):
            ui.label(question.get("question_text", "Question")
                     ).classes("text-h6")
            ui.label(f"Difficulty: {question.get('difficulty', 'n/a')}")

            def answer_clicked(answer_id: int) -> None:
                try:
                    result = submit_answer(session_id, answer_id)
                except Exception as exc:
                    ui.notify(f"Error submitting answer: {exc}")
                    return

                dlg.close()
                ui.notify(
                    "Correct!" if result["is_correct"] else "Wrong answer")

                if result["quiz_complete"]:
                    summary = end_quiz_session(session_id)
                    with ui.dialog() as summary_dlg:
                        with ui.card().classes("w-80"):
                            ui.label("Quiz complete!").classes("text-h6")
                            ui.label(
                                f"Score: {summary['score']}/{summary['total_questions']}"
                            )
                            ui.label(f"Percentage: {summary['percentage']}%")
                            ui.label(f"Grade: {summary['grade']}/6")
                            ui.button("OK", on_click=summary_dlg.close)
                    summary_dlg.open()
                else:
                    show_question_dialog(session_id, result["next_question"])

            for answer in question.get("answers", []):
                ui.button(
                    answer["text"],
                    on_click=lambda a=answer["answer_id"]: answer_clicked(a),
                ).classes("w-full")

    dlg.open()


def view_scoreboard() -> None:
    scores = get_top_scores(limit=10)
    with ui.dialog() as dlg:
        with ui.card().classes("w-[36rem]"):
            ui.label("Top 10 Scores").classes("text-h6")
            if not scores:
                ui.label("No scores yet.")
            else:
                for idx, score in enumerate(scores, 1):
                    ui.label(
                        f"{idx}. {score['username']} - {score['score']} ({score['timestamp']})"
                    )
            ui.button("Close", on_click=dlg.close)
    dlg.open()


def add_subject_dialog() -> None:
    with ui.dialog() as dlg:
        with ui.card().classes("w-96"):
            ui.label("Add Subject").classes("text-h6")
            subject_input = ui.input("Subject name")

            def save_subject() -> None:
                if add_subject(subject_input.value.strip()):
                    ui.notify("Subject added")
                    dlg.close()
                else:
                    ui.notify("Could not add subject")

            ui.button("Save", on_click=save_subject)
            ui.button("Cancel", on_click=dlg.close)
    dlg.open()


def add_topic_dialog() -> None:
    subjects = get_all_subjects()
    if not subjects:
        ui.notify("No subjects available")
        return

    with ui.dialog() as dlg:
        with ui.card().classes("w-96"):
            ui.label("Add Topic").classes("text-h6")
            subject_select = ui.select(subjects, label="Subject")
            topic_input = ui.input("Topic name")

            def save_topic() -> None:
                subject_id = get_subject_id_by_name(subject_select.value)
                if not subject_id:
                    ui.notify("Select a valid subject")
                    return
                if add_topic(topic_input.value.strip(), subject_id):
                    ui.notify("Topic added")
                    dlg.close()
                else:
                    ui.notify("Could not add topic")

            ui.button("Save", on_click=save_topic)
            ui.button("Cancel", on_click=dlg.close)
    dlg.open()


def add_question_dialog() -> None:
    subjects = get_all_subjects()
    if not subjects:
        ui.notify("No subjects available")
        return

    with ui.dialog() as dlg:
        with ui.card().classes("w-[40rem]"):
            ui.label("Add Question").classes("text-h6")
            subject_select = ui.select(subjects, label="Subject")
            topic_select = ui.select([], label="Topic")

            def update_topics() -> None:
                subject = subject_select.value
                if not subject:
                    topic_select.options = []
                    return
                topics = get_topics_with_ids_by_subject(subject)
                topic_select.options = [topic["topic_name"]
                                        for topic in topics]

            ui.button("Load Topics", on_click=update_topics)

            question_input = ui.input("Question text")
            answer_inputs = [ui.input(f"Answer {idx}") for idx in range(1, 5)]
            correct_input = ui.number(
                "Correct answer number (1-4)", value=1, min=1, max=4)
            difficulty_input = ui.select(
                ["easy", "medium", "hard"], value="medium", label="Difficulty")

            def save_question() -> None:
                subject = subject_select.value
                topic_name = topic_select.value
                if not subject or not topic_name:
                    ui.notify("Select subject and topic")
                    return

                topics = get_topics_with_ids_by_subject(subject)
                topic = next(
                    (item for item in topics if item["topic_name"] == topic_name), None)
                if not topic:
                    ui.notify("Invalid topic")
                    return

                answers = [field.value.strip() for field in answer_inputs]
                if any(not answer for answer in answers):
                    ui.notify("Fill in all answer fields")
                    return

                if add_question(
                        topic_id=topic["topic_id"],
                        question_text=question_input.value.strip(),
                        answers=answers,
                        correct_answer_idx=int(correct_input.value) - 1,
                        difficulty=difficulty_input.value,
                ):
                    ui.notify("Question added")
                    dlg.close()
                else:
                    ui.notify("Could not add question")

            ui.button("Save", on_click=save_question)
            ui.button("Cancel", on_click=dlg.close)
    dlg.open()


def delete_question_dialog() -> None:
    with ui.dialog() as dlg:
        with ui.card().classes("w-80"):
            ui.label("Delete Question").classes("text-h6")
            question_input = ui.number("Question ID", min=1)

            def remove_question() -> None:
                try:
                    question_id = int(question_input.value)
                except Exception:
                    ui.notify("Enter a valid question ID")
                    return

                if delete_question(question_id):
                    ui.notify("Question deleted")
                    dlg.close()
                else:
                    ui.notify("Could not delete question")

            ui.button("Delete", on_click=remove_question)
            ui.button("Cancel", on_click=dlg.close)
    dlg.open()


ui.label("Quiz Application").classes("text-h4")

with ui.card().classes("w-96") as login_card:
    ui.label("Login").classes("text-h6")
    username_input = ui.input("Username")
    ui.button("Login", on_click=login_user)

with ui.column().classes("gap-2") as app_card:
    welcome_label = ui.label("")
    role_label = ui.label("")

    with ui.row():
        ui.button("Take a Quiz", on_click=open_subject_menu)
        ui.button("View Scoreboard", on_click=view_scoreboard)
        ui.button("Logout", on_click=logout_user)

    with ui.column() as user_panel:
        ui.label("User menu")

    with ui.column() as admin_panel:
        ui.label("Admin menu")
        ui.button("Add Subject", on_click=add_subject_dialog)
        ui.button("Add Topic", on_click=add_topic_dialog)
        ui.button("Add Question", on_click=add_question_dialog)
        ui.button("Delete Question", on_click=delete_question_dialog)


refresh_screen()

ui.run()
