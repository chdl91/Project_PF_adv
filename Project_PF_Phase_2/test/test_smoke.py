import sqlite3

from sqlmodel import Session, select

from domain.models import Subject


def test_sqlite_integrity_check_on_fresh_database(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("create table example(id integer primary key, name text)")
        result = conn.execute("pragma integrity_check;").fetchone()[0]
    finally:
        conn.close()

    assert result == "ok"


def test_sqlmodel_can_create_and_query_subject(sqlite_engine):
    with Session(sqlite_engine) as session:
        subject = Subject(subject_name="Testing")
        session.add(subject)
        session.commit()
        session.refresh(subject)

        found = session.exec(
            select(Subject).where(Subject.subject_name == "Testing")
        ).first()

    assert found is not None
    assert found.subject_name == "Testing"
