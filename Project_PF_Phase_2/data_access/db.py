import os
from sqlmodel import SQLModel, create_engine, Session

script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.normpath(os.path.join(script_dir, "..", "DB", "quiz.db"))


class Database:
    """
    Facade: single place for engine creation, schema setup, and session lifecycle.
    Pass a different db_path to swap databases (e.g. for testing).
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)
