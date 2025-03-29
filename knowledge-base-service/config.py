import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
MONGO_URI = os.getenv("MONGO_URI")
MONGODB_METADATA_DB = os.getenv("MONGODB_METADATA_DB")
MONGODB_STORAGE_DB = os.getenv("MONGODB_STORAGE_DB")
DROPBOX_API_KEY = os.getenv("DROPBOX_API_KEY")
UPLOAD_LIMIT_MB = int(os.getenv("UPLOAD_LIMIT_MB", 10))
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "pdf,doc,docx").split(","))
