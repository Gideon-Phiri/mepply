import dropbox
from dropbox.exceptions import AuthError
from pymongo import MongoClient
import gridfs
from config import DROPBOX_API_KEY, MONGO_URI
import logging

class FileManager:
    def __init__(self):
        """Initialize Dropbox and MongoDB GridFS clients."""
        self.dbx = dropbox.Dropbox(DROPBOX_API_KEY)
        self.mongo_client = MongoClient(MONGO_URI)
        self.db = self.mongo_client['file_storage_db']
        self.fs = gridfs.GridFS(self.db)

    def upload_to_dropbox(self, file, filename):
        """Uploads a file to Dropbox and returns the file metadata."""
        try:
            dropbox_path = f"/uploads/{filename}"
            logging.debug(f"Uploading file to Dropbox at path: {dropbox_path}")
            self.dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            shared_link = self.dbx.sharing_create_shared_link_with_settings(dropbox_path)
            logging.info("File uploaded to Dropbox successfully.")
            return {"link": shared_link.url, "storage": "dropbox"}
        except AuthError as e:
            logging.error(f"Dropbox AuthError: {e}")
            return None
        except dropbox.exceptions.ApiError as e:
            logging.error(f"Dropbox API error: {e}")
            return None

    def upload_to_gridfs(self, file, filename):
        """Uploads a file to MongoDB GridFS and returns file metadata."""
        try:
            logging.debug("Uploading file to MongoDB GridFS.")
            file_id = self.fs.put(file, filename=filename)
            logging.info("File uploaded to MongoDB GridFS successfully.")
            return {"file_id": str(file_id), "storage": "mongodb"}
        except Exception as e:
            logging.error(f"GridFS upload error: {e}")
            return None

    def delete_from_dropbox(self, link):
        """Deletes a file from Dropbox using its path."""
        try:
            if link.startswith("https://www.dropbox.com") or link.startswith("https://dl.dropboxusercontent.com"):
                path = "/" + "/".join(link.split('/')[-2:])
            else:
                path = link
            logging.debug(f"Attempting to delete Dropbox file at path: {path}")
            self.dbx.files_delete_v2(path)
            logging.info("File deleted successfully from Dropbox.")
            return True
        except dropbox.exceptions.ApiError as e:
            logging.error(f"Dropbox deletion error: {e}")
            return False

    def delete_from_gridfs(self, file_id):
        """Deletes a file from MongoDB GridFS using its file_id."""
        try:
            logging.debug(f"Attempting to delete file from GridFS with file_id: {file_id}")
            self.fs.delete(file_id)
            logging.info("File deleted successfully from MongoDB GridFS.")
            return True
        except Exception as e:
            logging.error(f"GridFS deletion error: {e}")
            return False
