from fastapi import HTTPException
from app.config import settings


def validate_file_type(file_type: str):
    """
    Validates that the uploaded file type is allowed.

    Args:
        file_type (str): MIME type of the file to validate.

    Raises:
        HTTPException: If the file type is not supported.
    """
    if file_type not in [
            f"application/{ft}" for ft in settings.allowed_file_types]:
        raise HTTPException(status_code=400, detail="Unsupported file type")


def validate_file_size(file_size: int):
    """
    Validates that the uploaded file size does not exceed the allowed limit.
    Args:

        file_size (int): Size of the file to validate in bytes.
    Raises:

        HTTPException: If the file size exceeds the allowed limit.
    """
    if file_size > settings.max_file_size:
        raise HTTPException(
                status_code=400, detail="File exceeds maximum size limit")
