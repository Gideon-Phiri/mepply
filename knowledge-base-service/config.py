import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
MONGODB_URI = os.getenv("MONGODB_URI")
DROPBOX_API_KEY = os.getenv("DROPBOX_API_KEY")
UPLOAD_LIMIT_MB = int(os.getenv("UPLOAD_LIMIT_MB", 10))
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "pdf,doc,docx").split(","))
