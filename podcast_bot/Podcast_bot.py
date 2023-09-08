from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
import aiofiles.os as aos

from audio_lib import sync

import re
from typing import Optional

from Podcast_bot_message import welcome_message, commands_dict
from config import TOKEN

import time

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()

button_1: InlineKeyboardButton = InlineKeyboardButton(text='Начальное сообщение', callback_data='start')
button_2: InlineKeyboardButton = InlineKeyboardButton(text='Помощь', callback_data='help')
button_3: InlineKeyboardButton = InlineKeyboardButton(text='Директория проекта', callback_data='GitHub')


@dp.message(CommandStart())
async def start(message: Message):
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_2], [button_3]])
    await message.answer(text=welcome_message, reply_markup=keyboard)


@dp.callback_query(F.data == 'start')
async def start_button(callback: CallbackQuery):
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_2], [button_3]])
    await callback.message.edit_text(text=welcome_message, reply_markup=keyboard)


@dp.callback_query(F.data == 'help')
async def help_button(callback: CallbackQuery):
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_3]])
    await callback.message.edit_text(text=commands_dict['help'], reply_markup=keyboard)


@dp.callback_query(F.data == 'GitHub')
async def github_button(callback: CallbackQuery):
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    await callback.message.edit_text(text=commands_dict['GitHub_Directory'], reply_markup=keyboard)


def url_replace(url: str, /) -> str:
    name = re.sub(".+\?[vsi]+=", "", url)
    name = re.sub("&t=[0-9]+s", "", name)
    return name


@dp.message()
async def url_link(message: Message):
    url: str = message.text

    if url == 'https://www.youtube.com' or url == 'https://www.youtube.com/':
        await message.reply(text="Зачем вы отправляете ссылку на главную страницу ютуба?")

    else:
        try:
            start = time.perf_counter()

            id: int = message.from_user.id
            name: str = url_replace(url)
            dirs: list[str] = await aos.listdir('audio')

            if name not in dirs:
                sync.yt_dlp(url, name)
                dirs: list[str] = await aos.listdir(f'audio/{name}')
                for opus_file in dirs:
                    send_file: FSInputFile = FSInputFile(path=f'audio/{name}/{opus_file}', filename=opus_file)
                    await bot.send_voice(chat_id=id, voice=send_file, caption=send_file.filename)

            else:
                dirs: list[str] = await aos.listdir(f'audio/{name}')
                for opus_file in dirs:
                    send_file: FSInputFile = FSInputFile(path=f'audio/{name}/{opus_file}', filename=opus_file)
                    await bot.send_voice(chat_id=id, voice=send_file, caption=send_file.filename)

        except ValueError:
            await message.reply(text="Неправильный url")

        except IOError as err:
            await message.reply(text=err)

        except Exception as err:
            print(f"URL: {url} \n NAME: {name} \n ERR: {err}")

        finally:
            print(time.perf_counter() - start)


if __name__ == '__main__':
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())