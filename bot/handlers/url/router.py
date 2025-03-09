from aiogram import Bot, F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, FSInputFile, Message, URLInputFile

from bot.db import AudioDoc, FileType
from bot.storage import storage

from .errors import LargeFile, UrlToStream, UrlWrong
from .messages import error_messages
from .utils import download_audio, get_anecdote, url_validation

# 50MB
LIMIT_FILE_SIZE = 50_000_000

router = Router()


@router.message(F.text)
async def handle_url(message: Message):
	url = message.text
	video_id = url_validation(url)

	anecdote: str = get_anecdote()
	await message.answer(text=anecdote)

	if audio_doc := await AudioDoc.get(video_id):
		if audio_doc.size > LIMIT_FILE_SIZE:
			raise LargeFile(audio_doc.link)

		url_file = URLInputFile(audio_doc.link)
		await message.reply_audio(audio=url_file, title=audio_doc.title, duration=audio_doc.duration)
	else:
		video_info = await download_audio(url)
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

		if audio_doc.size > LIMIT_FILE_SIZE:
			raise LargeFile(audio_doc.link)

		await message.reply_audio(audio=audio_file, title=video_info.title, duration=video_info.duration)


@router.errors(ExceptionTypeFilter(UrlToStream))
async def handle_link_to_stream(event: ErrorEvent, bot: Bot) -> None:
	chat_id = event.update.message.chat.id
	message_id = event.update.message.message_id
	text = error_messages["url_to_stream"]
	await bot.send_message(text=text, chat_id=chat_id, reply_to_message_id=message_id)


@router.errors(ExceptionTypeFilter(UrlWrong))
async def handle_error_wrong_url(event: ErrorEvent, bot: Bot) -> None:
	chat_id = event.update.message.chat.id
	message_id = event.update.message.message_id
	text = error_messages["url_wrong"]
	await bot.send_message(text=text, chat_id=chat_id, reply_to_message_id=message_id)


@router.errors(ExceptionTypeFilter(LargeFile))
async def handle_error_link_to_stream(event: ErrorEvent, bot: Bot) -> None:
	file_link = str(event.exception)
	chat_id = event.update.message.chat.id
	message_id = event.update.message.message_id
	text = error_messages["large_file"] + file_link
	await bot.send_message(text=text, chat_id=chat_id, reply_to_message_id=message_id)


@router.errors()
async def handle_error_undefined(event: ErrorEvent, bot: Bot) -> None:
	chat_id = event.update.message.chat.id
	message_id = event.update.message.message_id
	text = error_messages["undefined"]
	await bot.send_message(text=text, chat_id=chat_id, reply_to_message_id=message_id)
