from data_access.user_dao import UserDAO


class UserService:
    """Business logic for user login and account creation."""

    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_or_create_user(self, username: str) -> dict:
        try:
            existing = self.user_dao.find_by_name(username)
            if existing:
                return {
                    "user_id": existing.user_id,
                    "user_name": existing.user_name,
                    "admin_status": existing.admin_status,
                    "is_new": False
                }

            new_user = self.user_dao.create(username)
            print(f"Welcome {username}! New account created.")
            return {
                "user_id": new_user.user_id,
                "user_name": new_user.user_name,
                "admin_status": new_user.admin_status,
                "is_new": True
            }
        except Exception as e:
            raise Exception(f"Error during login: {e}")
