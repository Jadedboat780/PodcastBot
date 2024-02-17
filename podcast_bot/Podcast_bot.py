from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
import aiofiles.os as aos
from audio_lib import async_mod

from messages import welcome_message, commands_dict, url_error
from additional_functions import random_anecdote, pattern_url
from config import TOKEN, admin_id

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


async def send_audio(url_id: str, user_id: int, /):
    '''Отправляет все аудио, которые есть в папке'''
    dirs: list[str] = await aos.listdir(f'audio/{url_id}')
    for opus_file in dirs:
        send_file: FSInputFile = FSInputFile(path=f'audio/{url_id}/{opus_file}')
        await bot.send_audio(chat_id=user_id, audio=send_file, caption=opus_file)


@dp.message()
async def url_link(message: Message):
    '''Принимает сообщение с ссылккой на видео и производит с ней необходимые действия'''
    url: str = message.text

    if url == "https://www.youtube.com" or url == "https://www.youtube.com/":
        await message.reply(text="Зачем вы отправляете ссылку на главную страницу ютуба?")

    elif any(link in url for link in ("youtube.com", "youtu.be")):
        try:
            anecdote: str = random_anecdote()
            await message.answer(text=anecdote)  # отправка случайного несмешного анекдота

            url_id: str = pattern_url(url)  # хранит id ссылки
            dirs: list[str] = await aos.listdir('audio')  # получение списка сохранённых ранее аудио
            user_id: int = message.from_user.id  # хранит id пользователя

            if url_id not in dirs:
                is_streaming: bool = await async_mod.is_streaming(url)  # проверка: ведёт ли ссылка на прямую трансляцию

                if is_streaming:
                    raise IOError(url_error[2])
                else:
                    await async_mod.download_audio(url, url_id)  # скачивание аудио дорожки из видео
                    await aos.mkdir(f'audio/{url_id}')  # создание папки для хранения частей аудио
                    await async_mod.audio_separation(url_id, 45)  # разделение аудио файла на несколько частей по 45 минут
                    await aos.unlink(f'{url_id}.opus')  # удаление исходного аудио
                    await send_audio(url_id, user_id)  # отправка сохранённого аудио

            else:
                await send_audio(url_id, user_id)  # отправка ранее сохранённого аудио

        except IOError as err:
            await message.reply(text=str(err))

        except BaseException as err:
            await bot.send_message(chat_id=admin_id,
                                   text=f"Error: {str(err)}\nLink: {url}")  # отправляет мне сообщение о непредвиденной ошибке
            await message.answer(url_error[3])

    else:
        await message.answer(url_error[1])


if __name__ == '__main__':
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
