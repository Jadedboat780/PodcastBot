from aiogram import Bot, Router
from aiogram.types import ErrorEvent

router = Router()


@router.errors()
async def handle_error(event: ErrorEvent, bot: Bot) -> None:
    message = event.update.message
    if message is None:
        return
    chat_id = message.chat.id
    text = str(event.exception)
    message_id = message.message_id
    await bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id)
