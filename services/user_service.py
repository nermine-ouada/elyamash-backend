from repositories.user_repository import UserRepository
from schemas.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def get_number_of_users(self):
        return self.user_repository.get_number_of_users()

    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    def get_user_by_username(self, username: str):
        return self.user_repository.get_user_by_username(username)
        # ... (save the user to the database)

    def create_user(self, user: UserCreate):
        return self.user_repository.create_user(user)

    def update_user(self, user_id: str, user: UserUpdate):
        return self.user_repository.update_user(user_id, user)

    def delete_user(self, user_id: str):
        return self.user_repository.delete_user(user_id)
