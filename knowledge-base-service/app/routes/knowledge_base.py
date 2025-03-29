# knowledge_base.py
from fastapi import APIRouter, Header, HTTPException, UploadFile, File, Body
from app.services.auth_service import verify_user
from app.services.file_manager import FileManager
from app.models.file_metadata import FileMetadata
from app.utils.validators import is_file_allowed, is_file_size_allowed
import logging

router = APIRouter()
file_manager = FileManager()
metadata_manager = FileMetadata()

@router.put("/settings")
async def set_storage_type(authorization: str = Header(None), storage_type: str = Body(...)):
    """Set the user's preferred storage type."""
    user_id, _ = verify_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if storage_type not in ["dropbox", "mongodb"]:
        raise HTTPException(status_code=400, detail="Invalid storage type")

    try:
        metadata_manager.set_primary_storage(user_id, storage_type)
        return {"message": f"Storage type set to {storage_type}"}
    except Exception as e:
        logging.error(f"Error setting storage type: {e}")
        raise HTTPException(status_code=500, detail="Failed to set storage type")


@router.post("/upload")
async def upload_file(authorization: str = Header(None), file: UploadFile = File(...)):
    """Upload a file after user verification."""

    user_id, _ = verify_user(authorization)  # Simplified verification
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    existing_file = metadata_manager.get_file_metadata(user_id)
    if existing_file:
        raise HTTPException(status_code=403, detail="You already have a file. Delete it first.")

    if not is_file_allowed(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    if not is_file_size_allowed(file):
        raise HTTPException(status_code=400, detail="File exceeds size limit")

    primary_storage = metadata_manager.get_primary_storage(user_id)
    filename = file.filename
    storage_result = None

    try:
        if primary_storage == "dropbox":
            storage_result = file_manager.upload_to_dropbox(await file.read(), filename)
        elif primary_storage == "mongodb" or primary_storage is None:
            storage_result = file_manager.upload_to_gridfs(await file.read(), filename)
        else:
            raise HTTPException(status_code=500, detail="Invalid storage configuration")

        if storage_result:
            metadata_manager.save_file_metadata(user_id, filename, storage_result)
            return {"message": "File uploaded successfully!", "storage": storage_result}
        else:
             raise HTTPException(status_code=500, detail="File upload failed")
    except Exception as e:
        logging.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")


@router.delete("/file")
async def delete_file(authorization: str = Header(None)):
    """Delete the user's uploaded file."""
    user_id, _ = verify_user(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    metadata = metadata_manager.get_file_metadata(user_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="No file found for deletion")

    try:
        if metadata["storage_type"] == "dropbox":
            result = file_manager.delete_from_dropbox(metadata["location"])
        else:
            result = file_manager.delete_from_gridfs(metadata["location"])

        if result:
            metadata_manager.delete_file_metadata(user_id)
            return {"message": "File deleted successfully!"}
        else:
            raise HTTPException(status_code=500, detail="File deletion failed")
    except Exception as e:
        logging.error(f"Error during file deletion: {e}")
        raise HTTPException(status_code=500, detail="File deletion failed")
