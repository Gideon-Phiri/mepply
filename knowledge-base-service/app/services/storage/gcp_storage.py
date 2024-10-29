from google.cloud import storage
from app.config import settings
from app.services.storage.storage_provider import StorageProvider


class GCPStorageProvider(StorageProvider):
    """
    Google Cloud Storage provider for handling file uploads and deletions.
    """

    def __init__(self):
        self.client = storage.Client.from_service_account_json(
                settings.google_cloud_credentials)
        self.bucket_name = "knowledge-base-bucket"

    async def upload_file(self, file, filename: str, user_id: str) -> str:
        """
        Uploads a file to Google Cloud Storage.
        """
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(f"{user_id}/{filename}")

        blob.upload_from_string(
                file.file.read(), content_type=file.content_type)
        return blob.public_url

    async def delete_file(self, file_url: str):
        """
        Deletes a file from Google Cloud Storage.
        """
        bucket = self.client.bucket(self.bucket_name)
        blob_name = file_url.split(self.bucket_name + "/")[1]
        blob = bucket.blob(blob_name)
        blob.delete()
