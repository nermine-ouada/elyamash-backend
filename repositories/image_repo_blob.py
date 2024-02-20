from helpers.blob import Blob
from azure.core.exceptions import ResourceNotFoundError


class ImageRepoBlob:
    def __init__(self, blob: Blob):
        self.blob = blob

    def create_upload_file(self, user_id: str, filename: str, file: bytes):
        try:
            folder_name = user_id
            blob_name = f"{folder_name}/{filename}"
            # Upload the file to Azure Blob Storage
            blob_client = self.blob.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(file, overwrite=True)
            return True
        except Exception as e:
            return False

    def delete_file(self,  file_path: str):
        # Delete the file from Azure Blob Storage
        try:
            blob_client = self.blob.container_client.get_blob_client(file_path)
            blob_client.delete_blob()
            return True
        except Exception as e:
            return False

    def check_image_existance(self, image_name: str, user_id: str):
        try:
            folder_name = user_id
            blob_name = f"{folder_name}/{image_name}"
            # Check if the blob exists
            blob_client = self.blob.container_client.get_blob_client(blob_name)
            blob_properties = blob_client.get_blob_properties()

            # Blob exists
            return True

        except ResourceNotFoundError:
            # Blob doesn't exist
            return False
