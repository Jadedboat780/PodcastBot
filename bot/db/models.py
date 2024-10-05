from pydantic import BaseModel
from enum import StrEnum, auto
from typing import Annotated
from annotated_types import MinLen, Ge

class FileType(StrEnum):
    text = auto()
    audio = auto()
    video = auto()

class Document(BaseModel):
    """Model for storing file properties"""
    id: str
    type: FileType

    def to_mongo(self) -> dict:
        """Convert Pydantic model to a MongoDB-compatible document"""
        doc = self.model_dump()
        doc["_id"] = doc.pop("id")
        return doc

class Audio(Document):
    """Meta-data for audio files"""
    title: Annotated[str, MinLen(2)]
    duration: Annotated[int, Ge(1)]