from app.services.storage.gcp_storage import GCPStorageProvider
from app.services.storage.dropbox_storage import DropboxStorageProvider
from app.config import settings


def get_storage_provider():
    """
    Returns an instance of the configured storage provider.
    """
    if settings.storage_provider == "gcp":
        return GCPStorageProvider()
    elif settings.storage_provider == "dropbox":
        return DropboxStorageProvider()
    else:
        raise ValueError("Invalid storage provider specified.")
