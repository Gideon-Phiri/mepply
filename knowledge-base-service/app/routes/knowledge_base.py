from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import KnowledgeBaseMetadata
from app.services.storage import get_storage_provider
from app.utils.auth import get_current_user
from app.utils.validators import validate_file_type, validate_file_size
from app.database import db
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/upload", response_model=KnowledgeBaseMetadata)
async def upload_knowledge_base(
    file: UploadFile, user_id: str = Depends(get_current_user)
):
    """
    Upload a knowledge base file for the authenticated user.

    This endpoint validates the file type and size, uploads it to the selected
    cloud storage provider, and stores metadata in the database.

    - **file**: File to be uploaded.
    - **user_id**: The ID of the authenticated user
    (retrieved from the auth-service).

    Returns metadata of the uploaded file.
    """
    try:
        # Validate file type and size
        validate_file_type(file.content_type)
        validate_file_size(file.spool_max_size)

        # Select storage provider and upload
        storage_provider = get_storage_provider()
        cloud_storage_path = await storage_provider.upload_file(
                file, file.filename, user_id)

        # Insert metadata into the database
        metadata = KnowledgeBaseMetadata(
            user_id=user_id,
            file_name=file.filename,
            cloud_storage_path=cloud_storage_path,
            uploaded_at=datetime.utcnow()
        )
        await db.knowledge_base.insert_one(metadata.dict(by_alias=True))

        return metadata

    except ValueError as e:
        logger.error(f"File validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {str(e)}")
        raise HTTPException(
                status_code=500, detail="An error occured during file upload")
