from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_LIMIT_MB


def is_file_allowed(filename):
    """Check if the file extension is allowed."""
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    return ext in ALLOWED_EXTENSIONS

def is_file_size_allowed(file):
    """Check if the file size is within the allowed limit."""
    file.seek(0, 2)  # Move the cursor to the end of the file
    file_size_mb = file.tell() / (1024 * 1024)  # Get file size in MB
    file.seek(0)  # Reset the file cursor to the beginning
    return file_size_mb <= UPLOAD_LIMIT_MB
