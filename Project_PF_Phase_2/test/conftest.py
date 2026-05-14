from pathlib import Path
import sys

import pytest
from sqlmodel import SQLModel, Session, create_engine


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain import models as _models  # noqa: F401


@pytest.fixture()
def sqlite_engine():
    """Create a fresh in-memory database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def db_session(sqlite_engine):
    """Create a database session for testing."""
    with Session(sqlite_engine) as session:
        yield session


@pytest.fixture()
def seeded_subject_topic(db_session):
    """Create one subject and one topic for database and integration tests."""
    from domain.models import Subject, Topic

    subject = Subject(subject_name="Digital Business")
    db_session.add(subject)
    db_session.commit()
    db_session.refresh(subject)

    topic = Topic(topic_name="AI", subject_id=subject.subject_id)
    db_session.add(topic)
    db_session.commit()
    db_session.refresh(topic)

    return subject, topic
