from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot.keyboards import Command, initial_buttons

from .messages import commands

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(Command.start))
	await message.answer(text=commands["welcome_message"], reply_markup=keyboard)


@router.callback_query(F.data == "start")
async def cb_start(callback: CallbackQuery):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(Command.start))
	await callback.message.edit_text(text=commands["welcome_message"], reply_markup=keyboard)


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery):
	keyboard = InlineKeyboardMarkup(inline_keyboard=initial_buttons(Command.start))
	await callback.message.edit_text(text=commands["help"], reply_markup=keyboard)
