from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from services.user_service import UserService
from datetime import datetime, timedelta
from utils.utils import check_password
from schemas.schemas import Token


SECRET_KEY: str = "2znmyRG!&)oloEKphqFQQ@6{]Q7T&W4S79GAbdqvNX{U2!3ZqR;Rv!:^G}@D-=O)"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: float = 30


class AuthRoute:

    def __init__(
        self,
        user_service: UserService,
        oauth2_scheme: OAuth2PasswordBearer,
    ):
        self.auth_router = APIRouter()
        self.user_service = user_service
        self.oauth2_scheme = oauth2_scheme

        @staticmethod
        def get_user(username: str):
            user = user_service.get_user_by_username(username)
            if user:
                return user
            return None

        def authenticate_user(username: str, password: str):
            user = get_user(username)
            if not user:
                return False
            if not check_password(password, user.hashed_password):
                return False

            return user

        def create_access_token(data: dict, expires_delta: timedelta):
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=15)

            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt

        @self.auth_router.post("/token")
        def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
        ):

            user = authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={
                    "sub": user.username,
                    "id": user.id,
                    "role": user.role,
                    "date": str(datetime.now()),
                },
                expires_delta=access_token_expires,
            )
            return Token(access_token=access_token, token_type="bearer")
