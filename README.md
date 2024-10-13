# Podcast bot
A Telegram bot that helps users easily download audio from YouTube videos

Stack: aiogram, pyo3, aiobotocore, motor

## How does this bot work?
The bot receives a YouTube video link, performs some checks, extracts the audio track, and sends it

## To start a project, you will need to:
1) Replace the examples of environment variables from the env.example file with their own values
2) Execute commands
```shell
# create virtual environment
python3 -m venv venv 
venv\Scripts\activate.bat # Linux/MacOs
source venv/bin/activate  # Windows

# install poetry and project dependencies
pip install poetry
poetry install

# building a library
maturin develop -m audio-lib/Cargo.toml

# start the project
poetry run bot-start 
```

## About the library for working with audio
The audio_lib library is used to download audio tracks from videos. 
This library was written by me using the Rust programming language and can be found in the audio-lib directory.

Modules:
* audio_lib - provides a synchronous version of the functions
* audio_lib.asyncio - provides an asynchronous version of the functions

Functools:
```python3
def get_video_info(url: str) -> VideoInfo: ...
"""Provides information about the video"""

def download_audio(url: str, name: str) -> None: ...
"""Downloads an audio track from the video."""
```

Classes:
```python3
class VideoInfo:
    """Stores information about the video"""
    id: str
    title: str
    duration: str
    is_live: bool
```
