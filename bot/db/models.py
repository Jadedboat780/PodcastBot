from pydantic import BaseModel


class AudioFile(BaseModel):
    """Meta-data for audio files"""
    title: str
    duration: int


class StorageModel(BaseModel):
    id: str
    type: AudioFile

    def to_mongo(self):
        doc = self.model_dump()
        doc["_id"] = doc.pop("id")
        return doc
