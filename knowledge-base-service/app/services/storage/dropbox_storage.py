import dropbox
from app.config import settings
from app.services.storage.storage_provider import StorageProvider


class DropboxStorageProvider(StorageProvider):
    """
    Dropbox provider for handling file uploads and deletions.
    """

    def __init__(self):
        self.client = dropbox.Dropbox(settings.dropbox_access_token)

    async def upload_file(self, file, filename: str, user_id: str) -> str:
        """
        Uploads a file to Dropbox.
        """
        dropbox_path = f"/{user_id}/{filename}"
        self.client.files_upload(file.file.read(), dropbox_path)
        shared_link = self.client.sharing_create_shared_link(dropbox_path)
        return shared_link.url

    async def delete_file(self, file_url: str):
        """
        Deletes a file from Dropbox.
        """
        dropbox_path = file_url.split("/home")[1]
        self.client.files_delete(dropbox_path)
