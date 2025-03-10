# Podcast bot
A Telegram bot that helps users easily download audio from YouTube videos

Stack: aiogram, aiobotocore, beanie, pyo3, uv, ruff

## How does this bot work?
The bot receives a YouTube video link, performs some checks, extracts the audio track, and sends it

## To start a project, you will need to:
```shell
# setting the version program
uv venv --python 3.12 

# creating a virtual environment and installing dependencies
uv sync

# activating virtual environment
source .venv/bin/activate

# building a library
maturin develop --uv -m audio-lib/Cargo.toml

# rename the env.example to env
mv .env.example .env

# project launch
uv run -m bot.main.py
```