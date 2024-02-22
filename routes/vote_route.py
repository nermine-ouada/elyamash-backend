from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.schemas import VoteCreate
from services.vote_service import VoteService
from services.image_service import ImageService
from services.user_service import UserService
from utils.utils import decode_bearer_token


class VoteRoute:
    def __init__(
        self,
        vote_service: VoteService,
        image_service: ImageService,
        user_service: UserService,
        
    ):
        self.vote_router = APIRouter()
        self.vote_service = vote_service
        self.user_service = user_service
        self.image_service = image_service
        self.security = HTTPBearer()

        @self.vote_router.post("/vote")
        def create_vote(
            vote: VoteCreate,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                nb_users = user_service.get_number_of_users()
                if nb_users < 2:
                    raise HTTPException(status_code=500, detail="not enough users")
                decoded_credentials = decode_bearer_token(credentials.credentials)
                voter_id = decoded_credentials.get("id")
                existing_user = self.user_service.get_user_by_id(voter_id)
                if not existing_user:
                    raise HTTPException(status_code=404, detail="User not found")

                existing_img1 = self.image_service.get_image_by_id(vote.image1)
                if not existing_img1:
                    raise HTTPException(status_code=404, detail="images not found")

                existing_img2 = self.image_service.get_image_by_id(vote.image2)
                if not existing_img2:
                    raise HTTPException(status_code=404, detail="image2 not found")

                if existing_img1 == existing_img2:
                    raise HTTPException(
                        status_code=409, detail="Images must be diffrent"
                    )

                if vote.score1 == vote.score2:
                    raise HTTPException(
                        status_code=400, detail="choose image no draw accepted"
                    )
                if vote.score1 == 1 and vote.score2 == 0:
                    chosen_image = existing_img1.id
                elif vote.score2 == 1 and vote.score1 == 0:
                    chosen_image = existing_img2.id
                else:
                    raise HTTPException(
                        status_code=400, detail="invalid score"
                    )
                new_vote = self.vote_service.create_vote(voter_id, vote, chosen_image)

                return {"message":"success vote","vote":new_vote}
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.vote_router.get("/vote")
        def get_vote_by_id(
            vote_id:str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                if role=="admin":
                    existing_vote = self.vote_service.get_vote_by_id(vote_id)
                    if not existing_vote:
                        raise HTTPException(status_code=404, detail="Vote not found")
                    return existing_vote
                else :
                    raise HTTPException(status_code=401,detail="no permission to view this route")
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )
