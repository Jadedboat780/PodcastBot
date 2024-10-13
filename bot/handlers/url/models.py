from pydantic import BaseModel


class VideoInfo(BaseModel):
    """Stores information about the video"""
    id: str
    title: str
    duration: int
    is_live: bool
