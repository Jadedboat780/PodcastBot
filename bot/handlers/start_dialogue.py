from enum import StrEnum, auto
from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner


class KeyboardCommand(StrEnum):
    """Commands enum"""

    START = auto()
    HELP = auto()


def initial_buttons(command: KeyboardCommand, i18n: TranslatorRunner) -> list[list[InlineKeyboardButton]] | None:
    """Returns the inline-buttons for the initial message"""

    button_start = InlineKeyboardButton(text=i18n.button.start(), callback_data="start")
    button_help = InlineKeyboardButton(text=i18n.button.help(), callback_data="help")
    button_source = InlineKeyboardButton(text=i18n.button.source(), url="https://github.com/Jadedboat780/PodcastBot.git")

    if command == KeyboardCommand.START:
        return [[button_help], [button_source]]
    elif command == KeyboardCommand.HELP:
        return [[button_start], [button_source]]
    else:
        return None


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
