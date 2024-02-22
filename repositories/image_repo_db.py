from datetime import datetime
from sqlalchemy.orm import Session
from models.tables import Image
from models.schemas import ImageUpdate
from sqlalchemy.sql.expression import func

import uuid


class ImageRepoDB:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_image_by_id(self, image_id: str):
        return self.db_session.query(Image).filter(Image.id == image_id).first()

    def get_all_images(self):
        return self.db_session.query(Image).all()

    def get_user_images(self, user_id: str):
        return self.db_session.query(Image).filter(Image.user_id == user_id).all()

    def create_image(self, user_id: str, filename: str):
        new_image = Image(
            id=str(uuid.uuid4()),
            image_name=filename,
            image_path=user_id + "/" + filename,
            user_id=user_id,
            rating=0,
        )
        self.db_session.add(new_image)
        self.db_session.commit()
        self.db_session.refresh(new_image)
        self.db_session.close()
        return new_image

    def update_image(self, image_id: str, image: ImageUpdate):
        existing_image = self.get_image_by_id(image_id)
        if existing_image:
            existing_image.image_desc = image.image_desc
            existing_image.updated_at = datetime.now()

            self.db_session.commit()
            self.db_session.refresh(existing_image)
            self.db_session.close()

            return existing_image
        return None

    def delete_image(self, image_id: str):
        image = self.get_image_by_id(image_id)
        if image:
            self.db_session.delete(image)
            self.db_session.commit()
            return image
        return None

    def get_random_image(self):
        random_image = self.db_session.query(Image).order_by(func.random()).first()
        return random_image
