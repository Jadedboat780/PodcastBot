import pydub
import os


def split_audio(audio_file, audio_title):
    '''Делит файлы по папкам,
    делит аудио на части по 45 минут и
    удаляет изначальный файл аудио(если оно является слишком большим)'''
    try:
        song = pydub.AudioSegment.from_file(audio_file, bitrate='64k', format="m4a")
        size_in_milliseconds = 2700000
        song_length = len(song)
        num_of_fragments = -(-song_length // size_in_milliseconds)  # вычисляем количество фрагментов

        if not os.path.exists(f'content/{audio_title}'):
            os.makedirs(f'content/{audio_title}')

        # разделяем MP3 файл на фрагменты и выводим каждый фрагмент в новый файл
        for i in range(num_of_fragments):
            start_time = i * size_in_milliseconds
            end_time = min((i + 1) * size_in_milliseconds, song_length)
            fragment = song[start_time:end_time]
            fragment.export(os.path.join(f"content/{audio_title}", f"{audio_title}_{i}.m4a"), format="mp3")
        return os.listdir(f"content/{audio_title}")

    except pydub.exceptions.CouldntDecodeError:
        return None

    finally:
        if audio_file in os.listdir():
            os.remove(audio_file)


def file_list(path):
    '''Возвращает список файлов в папке и удаляет не нужные файлы'''
    if path:
        return os.listdir(path)
    else:
        file_part = [file for file in os.listdir() if file.endswith(".part")]
        file_audio = [file for file in os.listdir() if file.endswith(".m4a")]

        if file_part:
            [os.remove(file) for file in file_part]

        if file_audio:
            [os.remove(file) for file in file_audio]