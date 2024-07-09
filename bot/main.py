from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

from bot.config import config
from bot.messages import commands

dp = Dispatcher()

button_start = InlineKeyboardButton(text='Начальное сообщение', callback_data='start')
button_help = InlineKeyboardButton(text='Помощь', callback_data='help')
button_github = InlineKeyboardButton(text='Исходный код этого проекта 💾', url='https://github.com/Jadedboat780/PodcastBot.git')


@dp.message(CommandStart())
async def handle_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_help], [button_github]])
    await message.answer(text=commands['welcome_message'], reply_markup=keyboard)


@dp.callback_query(F.data == 'start')
async def cb_start(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_help], [button_github]])
    await callback.message.edit_text(text=commands['welcome_message'], reply_markup=keyboard)


@dp.callback_query(F.data == 'help')
async def cb_help(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_start], [button_github]])
    await callback.message.edit_text(text=commands['help'], reply_markup=keyboard)


if __name__ == '__main__':
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
