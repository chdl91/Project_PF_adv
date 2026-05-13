"""
Presentation Layer - NiceGUI (browser-based interface)

To be implemented by the team. This file receives the same services
as QuizCLI so no business logic needs to change when switching interfaces.

Wiring example (in __main__.py):
    gui = QuizGUI(user_svc, subject_svc, question_svc, score_svc, quiz_session_svc)
    gui.run()
"""

from nicegui import ui


class QuizGUI:
    def __init__(self, user_service, subject_service, question_service, score_service, quiz_session_service):
        self.user_service = user_service
        self.subject_service = subject_service
        self.question_service = question_service
        self.score_service = score_service
        self.quiz_session_service = quiz_session_service

    def run(self):
        ui.label("Quiz App - NiceGUI interface coming soon!")
        ui.run()
