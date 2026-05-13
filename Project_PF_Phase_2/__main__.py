"""
Application entry point.

Wires all layers together:
    Database (Facade)
        -> DAOs (data_access)
            -> Services (services)
                -> UI (ui/cli.py  or  ui/gui.py)

Run from the Project_PF_Phase_2/ directory:
    python __main__.py
"""

from data_access.db import Database
from data_access.user_dao import UserDAO
from data_access.subject_dao import SubjectDAO
from data_access.question_dao import QuestionDAO
from data_access.score_dao import ScoreDAO

from services.user_service import UserService
from services.subject_service import SubjectService
from services.question_service import QuestionService
from services.score_service import ScoreService
from services.quiz_session_service import QuizSessionService

from ui.cli import QuizCLI


def main():
    # --- Data layer ---
    db = Database()

    user_dao     = UserDAO(db)
    subject_dao  = SubjectDAO(db)
    question_dao = QuestionDAO(db)
    score_dao    = ScoreDAO(db)

    # --- Service layer ---
    user_svc         = UserService(user_dao)
    subject_svc      = SubjectService(subject_dao)
    question_svc     = QuestionService(question_dao)
    score_svc        = ScoreService(score_dao)
    quiz_session_svc = QuizSessionService(subject_svc, question_svc, score_svc)

    # --- Presentation layer ---
    # Switch QuizCLI -> QuizGUI here when the browser interface is ready
    cli = QuizCLI(user_svc, subject_svc, question_svc, score_svc, quiz_session_svc)
    cli.run()


if __name__ == "__main__":
    main()
