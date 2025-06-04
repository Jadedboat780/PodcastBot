from pydantic import BaseModel


class VideoInfo(BaseModel):
    id: str
    title: str
    duration:int | None
    is_live: bool
