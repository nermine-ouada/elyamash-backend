from repositories.image_repo_db import ImageRepoDB
from repositories.image_repo_blob import ImageRepoBlob
from schemas.schemas import ImageUpdate


class ImageService:
    def __init__(self, image_repo_db: ImageRepoDB, image_repo_blob: ImageRepoBlob):
        self.image_repo_db = image_repo_db
        self.image_repo_blob = image_repo_blob

    def get_image_by_id(self, image_id: str):
        return self.image_repo_db.get_image_by_id(image_id)

    def get_all_images(self):
        return self.image_repo_db.get_all_images()

    def get_user_images(self, user_id: str):
        return self.image_repo_db.get_user_images(user_id)

    def upload_image(self, user_id: str, filename: str, file: bytes):
        return self.image_repo_blob.create_upload_file(user_id, filename, file)

    def create_image(self, user_id: str, filename: str):
        return self.image_repo_db.create_image(user_id, filename)

    def update_image(self, image_id: str, image: ImageUpdate):
        return self.image_repo_db.update_image(image_id, image)

    def delete_image(self, image_id: str):
        return self.image_repo_db.delete_image(image_id)

    def delete_file(self, file_path: str):
        return self.image_repo_blob.delete_file(file_path)

    def check_image_existance(self, image_name: str, user_id: str):
        return self.image_repo_blob.check_image_existance(image_name, user_id)

    def get_random_image(self):
        return self.image_repo_db.get_random_image()
