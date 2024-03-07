from fastapi import APIRouter, Security, File, UploadFile, HTTPException
from models.schemas import ImageUpdate
from services.image_service import ImageService
from services.user_service import UserService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.utils import decode_bearer_token


class ImageRoute:
    def __init__(
        self,
        image_service: ImageService,
        user_service: UserService,
    ):
        self.image_router = APIRouter()
        self.image_service = image_service
        self.user_service = user_service
        self.security = HTTPBearer()

        @self.image_router.post("/image")
        async def upload_image(
            file: UploadFile = File(...),
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):

            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")
                role = decoded_credentials.get("role")

                if not (role == "uploader" or role == "admin"):
                    raise HTTPException(
                        status_code=401, detail="No permission to upload images"
                    )

                if not file.content_type.startswith("image"):
                    raise HTTPException(
                        status_code=400, detail="Only image files are allowed"
                    )

                if self.image_service.check_image_existance(file.filename, user_id):
                    raise HTTPException(
                        status_code=409, detail="Image already exists !"
                    )

                filename = file.filename
                file_content = await file.read()

                if self.image_service.upload_image(user_id, filename, file_content):
                    new_image = self.image_service.create_image(user_id, file.filename)

                return {"message": "Upload successful", "image": new_image}

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.get("/image/all")
        def get_images(
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")

                if role == "admin":
                    images = self.image_service.get_all_images()
                    return images

                else:
                    raise HTTPException(
                        status_code=401, detail="No permission to view this route"
                    )

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.get("/image/all/me")
        def get_my_images(
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")
                images = self.image_service.get_user_images(user_id)
                return images

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.get("/image/all/{user_id}")
        def get_user_images(
            user_id: str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                id = decoded_credentials.get("id")
                if role == "admin" or user_id == id:
                    images = self.image_service.get_user_images(user_id)
                    return images
                else:
                    raise HTTPException(
                        status_code=401, detail="no permision to view this data"
                    )

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.get("/image/random")
        def get_random_images(
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                nb_users = user_service.get_number_of_users()
                if nb_users < 2:
                    raise HTTPException(status_code=500, detail="not enough users")
                random1 = self.image_service.get_random_image()
                random2 = self.image_service.get_random_image()
                while random1 == random2 or random1.user_id == random2.user_id:
                    random2 = self.image_service.get_random_image()

                return {"image 1 ": random1.id, "image 2 ": random2.id}
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.get("/image/{image_id}")
        def get_image_by_id(
            image_id: str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                role = decoded_credentials.get("role")
                id = decoded_credentials.get("id")
                existing_image = self.image_service.get_image_by_id(image_id)
                if not existing_image:
                    raise HTTPException(status_code=404, detail="Image not found")
                if role == "admin" or existing_image.user_id == id:
                    return existing_image
                else:
                    raise HTTPException(
                        status_code=401, detail="no permission to view this image"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.put("/image/{image_id}")
        def update_image(
            image_id: str,
            image: ImageUpdate,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")

                existing_image = self.image_service.get_image_by_id(image_id)
                if not existing_image:
                    raise HTTPException(status_code=404, detail="Image not found")
                if existing_image.user_id != user_id:
                    raise HTTPException(
                        status_code=401,
                        detail="No permission to update this image (not owner)",
                    )

                update_image = self.image_service.update_image(image_id, image)
                return update_image

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )

        @self.image_router.delete("/image/{image_id}")
        def delete_image(
            image_id: str,
            credentials: HTTPAuthorizationCredentials = Security(self.security),
        ):
            try:
                decoded_credentials = decode_bearer_token(credentials.credentials)
                user_id = decoded_credentials.get("id")
                role = decoded_credentials.get("role")

                existing_image = self.image_service.get_image_by_id(image_id)
                if not existing_image:
                    raise HTTPException(status_code=404, detail="Image not found")
                
                if existing_image.user_id != user_id and role!="admin" :
                    raise HTTPException(
                        status_code=401,
                        detail="No permission to delete this image",
                    )

                if self.image_service.delete_file(existing_image.image_path):
                    self.image_service.delete_image(image_id)
                else:
                    raise HTTPException(
                        status_code=400, detail="Image has not been deleted "
                    )
                return {"message": "image deleted successfully"}

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"An error occurred: {str(e)}"
                )
