import telebot
import yt_dlp
import random
import re
from separation_audio import split_audio, file_list
from Podcast_bot_message import welcome_message, commands_dict, base_anecdote, url_error

bot = telebot.TeleBot('Ваш токен')


@bot.message_handler(commands=['start'])
def start(message):
    '''Приветствие нового пользователя'''
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['author'])
def author(message):
    '''Команда, отправляющая пользователю ссылку на профиль создателя бота'''
    bot.send_message(message.chat.id, commands_dict['author'])


@bot.message_handler(commands=['help'])
def help(message):
    '''Объясняет пользователю как работает бот'''
    bot.send_message(message.chat.id, commands_dict['help'])


@bot.message_handler(commands=['GitHub_Directory'])
def github(message):
    '''Команда, отправляющая ссылку на директория бота на GitHub'''
    bot.send_message(message.chat.id, commands_dict['GitHub_Directory'])


def Song(song_url, song_title):
    '''Обработка видео из Ютуб в аудио файл'''
    outtmpl = song_title
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'm4a',
             'preferredquality': '192'},
            {'key': 'FFmpegMetadata'},
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])  # Скачивание видео в виде m4a файла


def refactor_song_url(message):
    '''Обработка ссылки в нужный формат'''
    if '&' in message:
        song_url = re.sub(r'&[\w\S]*', '', message)
    elif 'youtu.be' in message:
        song_url = re.sub('youtu.be/', 'www.youtube.com/watch?v=', message)
    else:
        song_url = message
    return song_url.split('watch?v=')[-1]


def send_audio(file_folder, song_url, id_chat):
    for file in file_folder:
        with open(f'content/{song_url}/{file}', 'rb') as audio:
            bot.send_audio(id_chat, audio=audio)  # Отправка mp3 файла


@bot.message_handler(content_types=['text'])
def download(message):
    '''#Функция принимает URL ссылку в виде текстового сообщения и обрабатывает её'''
    try:
        if 'https://www.youtube.com' == message.text or message.text == 'https://www.youtube.com/':
            bot.send_message(message.chat.id, 'Зачем вы отправляете ссылку на главную страницу ютуба?')
        elif ('www.youtube.com/watch?v=' in message.text) or ('youtu.be' in message.text):
            number = random.randint(1, 24)
            bot.reply_to(message, base_anecdote[number])  # Бот отправляет анекдот
            song_url = refactor_song_url(message.text)

            if song_url in file_list('content'):
                file_folder = file_list(f'content/{song_url}')
                send_audio(file_folder, song_url, message.chat.id)
            else:
                Song(song_url, song_url)
                file_folder = split_audio(f'{song_url}.m4a', song_url)

                if file_folder:
                    send_audio(file_folder, song_url, message.chat.id)
                else:
                    bot.reply_to(message, 'Видео является слишком длинным')
        else:
            bot.send_message(message.chat.id, 'Неверные данные')

    except PermissionError:
        file_list(None)
        bot.send_message(message.chat.id, 'Хватит спамить бота')

    except yt_dlp.utils.DownloadError:
        # Отправка одного из нескольких сообщений, в случае оправки неправильного url
        number = random.randint(1, 5)
        bot.send_message(message.chat.id, url_error[number])


if __name__ == '__main__':
    bot.polling()