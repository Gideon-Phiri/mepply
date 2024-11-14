from flask import Flask, request, jsonify
from app.utils.validators import is_file_allowed, is_file_size_allowed
from app.services.auth_service import verify_user
from app.services.file_manager import FileManager
import logging

app = Flask(__name__)
file_manager = FileManager()

@app.route("/upload", methods=["POST"])
def upload_file():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({"error": "Authorization token is required"}), 401

    # Verify user
    user_id = verify_user(auth_token)
    if not user_id:
        logging.debug("Failed to verify user.")
        return jsonify({"error": "Unauthorized"}), 401
    logging.debug(f"User ID verified: {user_id}")

    # Check file in request
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]

    # Validate file type and size
    if not is_file_allowed(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    if not is_file_size_allowed(file):
        return jsonify({"error": f"File exceeds {UPLOAD_LIMIT_MB}MB limit"}), 400

    # Determine storage method (Dropbox or GridFS based on user preference)
    # Here we assume Dropbox is default; logic could change with user settings
    filename = file.filename
    storage_result = file_manager.upload_to_dropbox(file, filename) or file_manager.upload_to_gridfs(file, filename)

    if storage_result:
        # Save metadata (additional metadata saving to MongoDB can be added here)
        return jsonify({
            "message": "File uploaded successfully!",
            "storage": storage_result
        }), 200
    else:
        return jsonify({"error": "File upload failed"}), 500
