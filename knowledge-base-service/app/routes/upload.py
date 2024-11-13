from flask import Flask, request, jsonify
from app.utils.validators import is_file_allowed, is_file_size_allowed
from app.services.auth_service import verify_user
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        return jsonify({"error": "Authorization token is required"}), 401

    # Step 1: Verify the user through the Auth service
    user_id = verify_user(auth_token)
    if not user_id:
        logging.debug("Failed to verify user.")
        return jsonify({"error": "Unauthorized"}), 401
    logging.debug(f"User ID verified: {user_id}")

    # Step 2: Check if file part is in request
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]

    # Step 3: Validate file type and size
    if not is_file_allowed(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    if not is_file_size_allowed(file):
        return jsonify({"error": f"File exceeds {UPLOAD_LIMIT_MB}MB limit"}), 400

    # Placeholder for file handling (storage and metadata)
    return jsonify({"message": "File validated successfully!"}), 200

if __name__ == "__main__":
    app.run(port=5000)
