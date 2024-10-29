from abc import ABC, abstractmethod


class StorageProvider(ABC):
    """
    Abstract base class for storage providers.
    Defines methods for uploading and deleting files.
    """

    @abstractmethod
    async def upload_file(self, file, filename: str, user_id: str) -> str:
        """
        Uploads a file to the storage provider.
        Returns the URL of the uploaded file.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_url: str):
        """
        Deletes a file from the storage provider.
        """
        pass
