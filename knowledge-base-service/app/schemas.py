from pydantic import BaseModel, Field
from datetime import datetime


class KnowledgeBaseMetadata(BaseModel):
    """
    Schema for representing metadata of a knowledge base file.
    """
    user_id: str
    file_name: str
    cloud_storage_path: str
    uploaded_at: datetime
    processed: bool = False
