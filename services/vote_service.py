from repositories.vote_repository import VoteRepository
from schemas.schemas import VoteCreate


class VoteService:
    def __init__(self, vote_repository: VoteRepository):
        self.vote_repository = vote_repository

    def get_vote_by_id(self, vote_id: str):
        return self.vote_repository.get_vote_by_id(vote_id)

    def create_vote(self, voter_id: str, vote: VoteCreate,chosen_image:str):
        return self.vote_repository.create_vote(voter_id, vote,chosen_image)
