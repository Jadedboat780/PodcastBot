from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import FSInputFile, Message, URLInputFile

import audio_lib
from bot.db import AudioDoc, FileType
from bot.storage import storage
from bot.utils import get_anecdote, url_validation

router = Router()


@router.message(F.text)
async def handle_url(message: Message):
    url = message.text
    video_id = url_validation(url)

    if video_id is None:
        raise AiogramError("Incorrect url")

    if message.from_user.language_code == "ru":
        anecdote = get_anecdote()
        await message.answer(text=anecdote)

    if audio_doc := await AudioDoc.get(video_id):
        url_file = URLInputFile(audio_doc.link)
        await message.reply_audio(audio=url_file, title=audio_doc.title, duration=audio_doc.duration)
    else:
        video_info = await audio_lib.yt.get_video_info(url)
        if video_info.is_live:
            raise AiogramError("The url leads to a direct stream")
        await audio_lib.yt.download_audio(url, video_info.id)

        audio_file = FSInputFile(f"{video_info.id}.m4a")
        file_size = await storage.upload_file(".", audio_file.filename, is_delete=True)

        audio_doc = AudioDoc(
            id=video_id,
            title=video_info.title,
            type=FileType.AUDIO,
            size=file_size,
            link=await storage.file_link(audio_file.filename),
            duration=video_info.duration,
        )
        await audio_doc.insert()

        url_file = URLInputFile(audio_doc.link)
        await message.reply_audio(audio=url_file, title=audio_doc.title, duration=audio_doc.duration)
