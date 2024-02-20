from fastapi.security import OAuth2PasswordBearer
from routes.auth_route import AuthRoute
from services.user_service import UserService
from services.image_service import ImageService
from services.vote_service import VoteService

from repositories.user_repository import UserRepository
from repositories.image_repo_db import ImageRepoDB
from repositories.image_repo_blob import ImageRepoBlob
from repositories.vote_repository import VoteRepository

from helpers.database import Database
from helpers.blob import Blob

from routes.user_route import UserRoute
from routes.image_route import ImageRoute
from routes.vote_route import VoteRoute

from configuration.config import Settings

settings = Settings()
 
blob_strorage = Blob(settings.connection_string, settings.container_name)
database = Database(f"{settings.pg_dsn}")


user_repo = UserRepository(database.get_session())
user_service = UserService(user_repo)
user_route = UserRoute(user_service)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
auth_route = AuthRoute(user_service, oauth2_scheme)

image_repo_db = ImageRepoDB(database.get_session())
image_repo_blob = ImageRepoBlob(blob_strorage)
image_service = ImageService(image_repo_db, image_repo_blob)
image_route = ImageRoute(image_service, user_service)

vote_repo = VoteRepository(database.get_session(),settings.adjustment_range)
vote_service = VoteService(vote_repo)
vote_route = VoteRoute(vote_service, image_service, user_service)
