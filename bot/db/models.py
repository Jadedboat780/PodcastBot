from collections.abc import Mapping
from enum import StrEnum, auto
from typing import Annotated

from annotated_types import Ge, MinLen
from pydantic import BaseModel


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
	def to_model(doc: Mapping[str, any]) -> "Document":
		"""Convert a MongoDB document to a Pydantic model."""
		doc["id"] = str(doc.pop("_id"))

		if doc.get("type") == FileType.audio:
			return AudioDoc(**doc)
		else:
			return Document(**doc)


class AudioDoc(Document):
	"""Meta-data for audio files"""

	duration: Annotated[int, Ge(1)]
