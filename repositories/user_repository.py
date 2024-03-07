from datetime import datetime
from sqlalchemy.orm import Session
from models.tables import User
from models.schemas import UserCreate, UserUpdate
from utils.utils import hash_password
import uuid


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: str):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate):
        new_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role,
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        self.db_session.close()
        return new_user

    def get_all_users(self):
        return self.db_session.query(User).all()

    def get_number_of_users(self):
        return self.db_session.query(User).count()

    def get_user_by_username(self, username: str):
        return self.db_session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()

    def update_user(self, user_id: str, user_update: UserUpdate):
        existing_user = self.get_user_by_id(user_id)
        if existing_user:
            if user_update.fullname is not None:
                existing_user.full_name = user_update.fullname
            if user_update.username is not None:
                existing_user.username = user_update.username
            if user_update.age is not None:
                existing_user.age = user_update.age
            if user_update.password is not None:
                existing_user.hashed_password = hash_password(user_update.password)
            existing_user.updated_at = datetime.now()
            self.db_session.commit()
            self.db_session.refresh(existing_user)
            self.db_session.close()

            return existing_user
        return None

    def delete_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()

            return user
        return None
