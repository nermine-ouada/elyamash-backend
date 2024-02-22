from sqlalchemy.orm import Session
from models.tables import Vote, Image
from models.schemas import VoteCreate
import uuid


class VoteRepository:
    def __init__(self, db_session: Session,k:int):
        self.db_session = db_session
        self.k=k

    def get_vote_by_id(self, vote_id: str):
        return self.db_session.query(Vote).filter(Vote.id == vote_id).first()

    def create_vote(self, voter_id: str, vote: VoteCreate, chosen_image_id: str):
        new_vote = Vote(
            id=str(uuid.uuid4()),
            voter_id=voter_id,
            image1_id=vote.image1,
            image2_id=vote.image2,
            score_image1=vote.score1,
            score_image2=vote.score2,
        )
        image1 = self.db_session.query(Image).filter(Image.id == vote.image1).first()
        image2 = self.db_session.query(Image).filter(Image.id == vote.image2).first()

        # probability of image 1 winning
        p1 = 1.0 / (1.0 + pow(10, ((image2.rating - image1.rating) / 400)))

        # probability of image 2 winning
        p2 = 1.0 / (1.0 + pow(10, ((image1.rating - image2.rating) / 400)))

        # adjustment range
        

        # if image 1 is chosen
        if chosen_image_id == image1.id:
            image1.rating += self.k * (1 + p1)
            image2.rating += self.k * (0 - p2)

        # if image 2 is chosen 
        else:
            image1.rating += self.k * (0 - p1)
            image2.rating += self.k * (1 + p2)

        self.db_session.add(new_vote)
        self.db_session.commit()
        self.db_session.refresh(image1)
        self.db_session.refresh(image2)
        self.db_session.refresh(new_vote)
        self.db_session.close()
        return new_vote
