from enum import StrEnum, auto

from beanie import Document, Indexed
from pydantic import Field


class FileType(StrEnum):
	"""File type enum"""

	TXT = auto()
	IMAGE = auto()
	AUDIO = auto()
	VIDEO = auto()


class AudioDoc(Document):
	"""Document for audio files"""

	id: Indexed(str)
	title: str
	type: FileType = FileType.AUDIO
	size: int = Field(ge=1)
	link: str
	duration: int = Field(ge=1)

	class Settings:
		name = "audio_docs"
		use_cache = True
