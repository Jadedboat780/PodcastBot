from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from fluentogram import TranslatorRunner

from .keyboard import KeyboardCommand, initial_buttons

if TYPE_CHECKING:
	from locales.stub import TranslatorRunner

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message, i18n: TranslatorRunner):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(KeyboardCommand.START, i18n))
	text = i18n.message.welcome()
	await message.answer(text=text, reply_markup=keyboard)


@router.message(Command("help"))
async def handle_help(message: Message, i18n: TranslatorRunner):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(KeyboardCommand.HELP, i18n))
	text = i18n.message.help()
	await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(F.data == "start")
async def cb_start(callback: CallbackQuery, i18n: TranslatorRunner):
	text = i18n.message.welcome()
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(KeyboardCommand.START, i18n))
	await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery, i18n: TranslatorRunner):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(KeyboardCommand.HELP, i18n))
	text = i18n.message.help()
	await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.message(StateFilter(None), Command(commands="cancel"))
async def handle_cancel(message: Message, i18n: TranslatorRunner):
	text = i18n.message.cancel()
	await message.answer(text=text)
