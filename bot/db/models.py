from pydantic import BaseModel, ValidationError
from enum import StrEnum, auto
from typing import Annotated, Mapping
from annotated_types import MinLen, Ge


class FileType(StrEnum):
    """File type enum"""
    txt = auto()
    img = auto()
    audio = auto()
    video = auto()


class Document(BaseModel):
    """Model for storing file properties"""
    id: Annotated[str, MinLen(8)]
    title: Annotated[str, MinLen(2)]
    type: FileType
    size: Annotated[int, Ge(1)]
    link: str

    def to_mongo(self) -> dict:
        """Convert Pydantic model to a MongoDB-compatible document"""
        doc = self.model_dump()
        doc["_id"] = doc.pop("id")
        return doc

    @staticmethod
    def to_model(doc: Mapping[str, any]) -> "Document" | "AudioDoc":
        """Convert a MongoDB document to a Pydantic model."""
        try:
            doc["id"] = str(doc.pop("_id"))

            if doc.get("type") == FileType.audio:
                return AudioDoc(**doc)
            else:
                return Document(**doc)

        except ValidationError as e:
            raise ValueError(f"Error converting Mongo document to model: {e}")


class AudioDoc(Document):
    """Meta-data for audio files"""
    duration: Annotated[int, Ge(1)]
