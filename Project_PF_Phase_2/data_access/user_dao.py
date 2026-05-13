from typing import Optional
from sqlmodel import select, col
from domain.models import User


class UserDAO:
    """Database access for the User table (login / account management only)."""

    def __init__(self, database):
        self.database = database

    def find_by_name(self, username: str) -> Optional[User]:
        with self.database.get_session() as session:
            return session.exec(
                select(User)
                .where(User.user_name == username)
                .order_by(col(User.user_id))
            ).first()

    def create(self, username: str) -> User:
        with self.database.get_session() as session:
            user = User(user_name=username[:30], admin_status=False)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
