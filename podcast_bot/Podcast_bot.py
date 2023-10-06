from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
import aiofiles.os as aos
from audio_lib import async_mod

from re import sub
from random import randint

from messages import welcome_message, commands_dict, base_anecdote, url_error
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


def random_anecdote() -> str:
    '''Возвращает рандомный анекдот'''
    random_num: int = randint(len(base_anecdote))
    return base_anecdote[random_num]


def url_replace(url: str, /) -> str:
    '''Обработка url в нужный формат(возвращает id на видео)'''
    name: str = sub(".+\?[vsi]+=", "", url)
    name: str = sub("&t=[0-9]+s", "", name)
    name: str = sub("&list=.+", "", name)
    return name


async def send_audio(name: str, id: int, /):
    '''Отправляет все аудио, которые есть в папке'''
    dirs: list[str] = await aos.listdir(f'audio/{name}')
    for opus_file in dirs:
        send_file: FSInputFile = FSInputFile(path=f'audio/{name}/{opus_file}')
        await bot.send_audio(chat_id=id, audio=send_file, caption=opus_file)


@dp.message()
async def url_link(message: Message):
    '''Принимает ссылку на видео и производит с ней необходимые действия'''
    url: str = message.text

    if url == "https://www.youtube.com" or url == "https://www.youtube.com/":
        await message.reply(text="Зачем вы отправляете ссылку на главную страницу ютуба?")

    elif any(link in url for link in ("youtube.com", "youtu.be")):
        try:
            anecdote: str = random_anecdote()
            await message.answer(text=anecdote)  # отправка случайного не смешного анекдота

            name: str = url_replace(url)  # хранит id ссылки
            dirs: list[str] = await aos.listdir('audio')  # получение списка сохранённых аудио
            id: int = message.from_user.id  # хранит id пользователя

            if name not in dirs:
                is_streaming: bool = await async_mod.is_streaming(url)  # проверка на стрим

                if is_streaming:
                    raise IOError(url_error[3])
                else:
                    await async_mod.download_audio(url, name)  # скачивание аудио дорожки видео
                    await aos.mkdir(f'audio/{name}')  # создание папки для хранения частей аудио
                    await async_mod.audio_separation(name, 45)  # разделение аудио на несколько частей по 45 минут
                    await aos.unlink(f'{name}.opus')  # удаление исходного аудио
                    await send_audio(name, id)  # отправка сохранённого аудио

            else:
                await send_audio(name, id)  # отправка ранее сохранённого аудио

        except IOError as err:
            await message.reply(text=str(err))

        except BaseException as err:
            await bot.send_message(chat_id=admin_id, text=f"Error: {str(err)}\nLink: {url}")  # отправляет мне сообщение о непредвиденной ошибке
            await message.answer(url_error[2])

    else:
        await message.answer(url_error[1])


if __name__ == '__main__':
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
