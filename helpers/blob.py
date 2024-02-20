from azure.storage.blob import BlobServiceClient

class Blob():
    def __init__(self,conn_str:str,container_name:str ):
        
        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str
        )
        self.container_client = self.blob_service_client.get_container_client(container_name)
