import asyncio
import ssl

import certifi
from yt_dlp import YoutubeDL

from .schemas import VideoInfo

ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())


def _video_info(url: str) -> VideoInfo:
    options = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "extract_flat": "in_playlist",
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        return VideoInfo.model_validate(info)


def _download_audio(url: str, name: str):
    options = {
        "format": "bestaudio/best",
        "outtmpl": f"{name}.m4a",
        "quiet": True,
        "no_warnings": True,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])


async def get_video_info(url: str) -> VideoInfo:
    """Get information about a YouTube video."""
    res = await asyncio.to_thread(_video_info, url)
    return res


async def download_audio(url: str, name: str) -> VideoInfo:
    """Download an audio from YouTube video"""
    res = await asyncio.to_thread(_download_audio, url, name)
    return res
