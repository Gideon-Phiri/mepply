import dropbox
from dropbox.exceptions import AuthError
from config import DROPBOX_API_KEY, MONGO_URI
from pymongo import MongoClient
import gridfs


class FileManager:
    def __init__(self):
        # Initialize Dropbox client
        self.dbx = dropbox.Dropbox(DROPBOX_API_KEY)
        
        # Initialize MongoDB client and GridFS using URI from config
        client = MongoClient(MONGO_URI)
        db = client.get_database()  # Uses default database from the URI
        self.fs = gridfs.GridFS(db)

    def upload_to_dropbox(self, file, filename):
        """Uploads a file to Dropbox and returns the file metadata or None on failure."""
        try:
            # Generate a Dropbox path
            dropbox_path = f"/mepply/{filename}"

            # Upload the file to Dropbox
            self.dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

            # Create a shared link for the file
            shared_link = self.dbx.sharing_create_shared_link_with_settings(dropbox_path)
            return {"link": shared_link.url, "storage": "dropbox"}

        except AuthError as e:
            print(f"Dropbox AuthError: {e}")
            return None  # Trigger fallback to GridFS

        except dropbox.exceptions.ApiError as e:
            print(f"Dropbox upload error: {e}")
            return None  # Trigger fallback to GridFS

    def upload_to_gridfs(self, file, filename):
        """Uploads a file to MongoDB GridFS and returns file metadata."""
        try:
            # Save file to GridFS and get the file_id
            file_id = self.fs.put(file, filename=filename)
            return {"file_id": str(file_id), "storage": "mongodb"}
        except Exception as e:
            print(f"GridFS upload error: {e}")
            return None

    def upload_file(self, file, filename):
        """Attempts to upload to Dropbox,
        falling back to MongoDB GridFS if Dropbox upload fails."""
        result = self.upload_to_dropbox(file, filename)
        if result is None:
            # Reset file pointer to the start since `file.read()
            file.seek(0)
            result = self.upload_to_gridfs(file, filename)
        return result
