from re import sub
from random import randint

from podcast_bot.messages import base_anecdote


def random_anecdote() -> str:
    '''Возвращает рандомный анекдот'''
    random_num: int = randint(len(base_anecdote))
    return base_anecdote[random_num]



def pattern_url(url: str, /) -> str:
    '''Обработка url в нужный формат(возвращает id на видео)'''
    if "www.youtube.com" in url:
        url_id: str = sub(".+\?[vsi]+=", "", url)
        url_id: str = sub("&t=[0-9]+s", "", url_id)
        url_id: str = sub("&list=.+", "", url_id)
    else:
        url_id: str = sub("https://youtu.be/", "", url)
        url_id: str = sub("\?si=.+", "", url_id)

    return url_id