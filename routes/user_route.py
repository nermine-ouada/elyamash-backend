from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.schemas import UserCreate, UserUpdate
from services.user_service import UserService
from utils.utils import decode_bearer_token


class UserRoute:
    def __init__(self, user_service: UserService):
        self.user_router = APIRouter()
        self.user_service = user_service
        self.security = HTTPBearer()

        @self.user_router.post("/user")
        def create_user(
            user: UserCreate,
        ):
            try:
                existing_user = self.user_service.get_user_by_email(email=user.email)
                if existing_user:
                    raise HTTPException(
                        status_code=409, detail="Email is already registered"
                    )

                existing_user = self.user_service.get_user_by_username(user.username)
                if existing_user:
                    raise HTTPException(
                        status_code=409, detail="username is already registered"
                    )

                new_user = self.user_service.create_user(user)
                return new_user
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.user_router.get("/user/all")
        def get_users(
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                if role == "admin":
                    users = self.user_service.get_all_users()
                    return users
                else:
                    raise HTTPException(
                        status_code=401, detail="no permission to view this route"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.user_router.get("/user/me")
        def read_personal_info(
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")
                existing_user = self.user_service.get_user_by_id(user_id)
                if not existing_user:
                    raise HTTPException(status_code=404, detail="user not found")
                return existing_user
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.user_router.get("/user/{user_id}")
        def read_user(
            user_id: str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                if role == "admin":
                    existing_user = self.user_service.get_user_by_id(user_id)
                    if not existing_user:
                        raise HTTPException(status_code=404, detail="user not found")
                    return existing_user
                else:
                    raise HTTPException(
                        status_code=401, detail="no permission to view this route"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.user_router.put("/user/{user_id}")
        def update_my_info(
            user: UserUpdate,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")
                role = decoded_credentials.get("role")
                existing_user = self.user_service.get_user_by_id(user_id)
                if not existing_user:
                    raise HTTPException(status_code=404, detail="user not found")

                existing_username = self.user_service.get_user_by_username(
                    user.username
                )
                if existing_username or existing_user.username == user.username:
                    raise HTTPException(
                        status_code=409, detail="username is already registered"
                    )
                update_user = self.user_service.update_user(user_id=user_id, user=user)
                return update_user

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.user_router.delete("/user/{user_id}")
        def delete_user(
            user_id: str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                if role != "admin" :
                    raise HTTPException(
                        status_code=401, detail="no permission to update this user"
                    )
                existing_user = self.user_service.get_user_by_id(user_id=user_id)
                if not existing_user:
                    raise HTTPException(status_code=404, detail="User not found")
                existing_user = self.user_service.delete_user(user_id)
                return {"message": "User deleted successfully"}

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )
