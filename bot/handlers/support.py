from typing import TYPE_CHECKING

from aiogram import Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from fluentogram import TranslatorRunner

from bot.config import config

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

router = Router()


class WriteInSupport(StatesGroup):
    waiting_message = State()


@router.message(Command("support"))
async def handle_support(message: Message, i18n: TranslatorRunner, state: FSMContext):
    text = i18n.support.message()
    await message.answer(text=text)
    await state.set_state(WriteInSupport.waiting_message)


@router.message(Command(commands="cancel"))
async def handle_cancel(message: Message, i18n: TranslatorRunner, state: FSMContext):
    text = i18n.support.cancel()
    await message.answer(text=text)
    await state.clear()


@router.message(StateFilter(WriteInSupport.waiting_message))
async def user_send_massage(message: Message, i18n: TranslatorRunner, state: FSMContext, bot: Bot):
    username = message.from_user.username if message.from_user else None
    text = f"User `{username}` send message:\n\n {message.text}"
    await bot.send_message(chat_id=config.admin_id, text=text)

    text = i18n.support.send_message()
    await message.answer(text=text)
    await state.clear()
