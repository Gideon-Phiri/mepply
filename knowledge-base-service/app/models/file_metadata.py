from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI
import logging

class FileMetadata:
    def __init__(self):
        """Initialize MongoDB client and collection for user settings."""
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['file_metadata_db']
        self.collection = self.db['user_settings']

    def set_primary_storage(self, user_id, storage_type):
        """Sets the primary storage method for the user."""
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"primary_storage": storage_type}},
            upsert=True
        )
        logging.info(f"Primary storage set to {storage_type} for user {user_id}")

    def get_primary_storage(self, user_id):
        """Fetches the user's primary storage method."""
        user_settings = self.collection.find_one({"user_id": user_id})
        return user_settings.get("primary_storage") if user_settings else None

    def save_file_metadata(self, user_id, filename, storage_info):
        """Saves metadata for the uploaded file under the user's settings document."""
        current_file = {
            "filename": filename,
            "storage_type": storage_info["storage"],  # "dropbox" or "mongodb"
            "location": storage_info.get("link") or storage_info.get("file_id"),
            "uploaded_at": datetime.utcnow()
        }
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"current_file": current_file}},
            upsert=True
        )
        logging.info(f"File metadata saved successfully for user {user_id}")
        return current_file

    def get_file_metadata(self, user_id):
        """Fetches metadata for the user's current file."""
        user_settings = self.collection.find_one({"user_id": user_id})
        return user_settings.get("current_file") if user_settings else None

    def delete_file_metadata(self, user_id):
        """Deletes metadata for the user's current file."""
        result = self.collection.update_one(
            {"user_id": user_id},
            {"$unset": {"current_file": ""}}
        )
        logging.info(f"File metadata deleted for user {user_id}")
        return result
