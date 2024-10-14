from random import randint
from urllib.parse import parse_qs, urlparse

from audio_lib import asyncio as audio_lib

from .errors import UrlToStream, UrlWrong
from .messages import base_anecdotes
from .models import VideoInfo


def url_validation(url: str) -> str:
	"""Checks the validity of the YouTube url"""
	url_parse = urlparse(url)

	if url_parse.netloc == "youtu.be":
		video_id = url_parse.path.replace("/", "")
		return video_id
	elif url_parse.netloc == "www.youtube.com" and url_parse.path == "/watch":
		query_params: dict[str:str] = parse_qs(url_parse.query)
		video_id = query_params.get("v")[0]
		return video_id
	elif url_parse.netloc == "www.youtube.com" and "/live" in url_parse.path:
		video_id = url_parse.path.replace("/live/", "")
		return video_id
	else:
		raise UrlWrong


def get_anecdote() -> str:
	"""Returns a random joke"""
	random_num: int = randint(0, len(base_anecdotes) - 1)
	return base_anecdotes[random_num]


async def download_audio(url: str) -> VideoInfo:
	"""Downloading audio from a video by url"""
	info = await audio_lib.get_video_info(url)
	if info.is_live:
		raise UrlToStream

	await audio_lib.download_audio(url, info.id)
	return info
