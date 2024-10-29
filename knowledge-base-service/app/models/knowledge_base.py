from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class KnowledgeBaseMetadata(BaseModel):
    """
    MongoDB model for knowledge base metadata, storing user file information.
    """
    id: str = Field(..., alias="_id")
    user_id: str
    file_name: str
    cloud_storage_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False


class KnowledgeBaseCreate(BaseModel):
    user_id: str
    file: bytes  # Uploaded file content
    file_name: str
