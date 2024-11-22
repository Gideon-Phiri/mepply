from flask import Flask, request, jsonify
from app.utils.validators import is_file_allowed, is_file_size_allowed
from app.services.auth_service import verify_user
from app.services.file_manager import FileManager
from app.models.file_metadata import FileMetadata
import logging


app = Flask(__name__)
file_manager = FileManager()
metadata_manager = FileMetadata()

@app.route("/upload", methods=["POST"])
def upload_file():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        logging.error("Authorization token is missing.")
        return jsonify({"error": "Authorization token is required"}), 401

    user_id = verify_user(auth_token)
    if not user_id:
        logging.error("User verification failed.")
        return jsonify({"error": "Unauthorized"}), 401

    existing_file = metadata_manager.get_file_metadata(user_id)
    if existing_file:
        logging.info("User already has an uploaded file.")
        return jsonify({"error": "You already have an uploaded file. Delete it before uploading a new one."}), 403

    if "file" not in request.files:
        logging.error("No file part in the request.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if not is_file_allowed(file.filename):
        logging.error(f"File type '{file.filename}' not allowed.")
        return jsonify({"error": "File type not allowed"}), 400
    if not is_file_size_allowed(file):
        logging.error("File size exceeds limit.")
        return jsonify({"error": "File exceeds size limit"}), 400

    primary_storage = metadata_manager.get_primary_storage(user_id)
    logging.debug(f"Primary storage for user {user_id}: {primary_storage}")

    filename = file.filename
    storage_result = None
    if primary_storage == "dropbox":
        logging.debug("Attempting to upload to Dropbox.")
        storage_result = file_manager.upload_to_dropbox(file, filename)
    elif primary_storage == "mongodb" or primary_storage is None:
        logging.debug("Attempting to upload to MongoDB GridFS.")
        storage_result = file_manager.upload_to_gridfs(file, filename)

    if storage_result:
        metadata_manager.save_file_metadata(user_id, filename, storage_result)
        logging.info("File uploaded and metadata saved successfully.")
        return jsonify({
            "message": "File uploaded successfully!",
            "storage": storage_result
        }), 200
    else:
        logging.error("File upload failed during storage operation.")
        return jsonify({"error": "File upload failed"}), 500

@app.route("/file", methods=["DELETE"])
def delete_file():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({"error": "Authorization token is required"}), 401

    user_id = verify_user(auth_token)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    metadata = metadata_manager.get_file_metadata(user_id)
    if not metadata:
        logging.debug("No file metadata found for user.")
        return jsonify({"error": "No file found for deletion"}), 404

    logging.debug(f"File metadata found: {metadata}")

    if metadata["storage_type"] == "dropbox":
        result = file_manager.delete_from_dropbox(metadata["location"])
    else:
        result = file_manager.delete_from_gridfs(metadata["location"])

    if result:
        metadata_manager.delete_file_metadata(user_id)
        logging.debug("File metadata deleted successfully.")
        return jsonify({"message": "File deleted successfully!"}), 200
    else:
        logging.error("File deletion failed in storage.")
        return jsonify({"error": "File deletion failed"}), 500

@app.route("/set-storage", methods=["POST"])
def set_storage():
    auth_token = request.headers.get("Authorization")
    storage_type = request.json.get("storage_type")

    if storage_type not in ["dropbox", "mongodb"]:
        return jsonify({"error": "Invalid storage type"}), 400

    user_id = verify_user(auth_token)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    metadata_manager.set_primary_storage(user_id, storage_type)
    return jsonify({"message": f"Primary storage set to {storage_type}"}), 200
