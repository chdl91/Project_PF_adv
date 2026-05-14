from domain import models
from pathlib import Path
import sys

import pytest
from sqlmodel import SQLModel, create_engine, Session


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import models once at module level


@pytest.fixture(scope="function")
def sqlite_engine():
    """Create a fresh in-memory database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(sqlite_engine):
    """Create a database session for testing."""
    with Session(sqlite_engine) as session:
        yield session
