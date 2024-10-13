# Podcast bot
Telegram-бот, который помогает пользователям легко загружать аудио из видео на YouTube

Стек: aiogram, pyo3, aiobotocore, motor

## Как бот работает?                                                                                      
Бот получает ссылку на YouTube видео, выполняет некоторые проверки, извлекает звуковую дорожку и отправляет ее

## Для запуска проекта вам необходимо:
1) Заменить примеры переменных окружения из файла env.example на собственные значения
2) Выполнить команды:
```shell
# создать виртуальное окружение
python3 -m venv venv 
venv\Scripts\activate.bat # Linux/MacOs
source venv/bin/activate  # Windows

# установить poetry и зависимости проекта
pip install poetry
poetry install

# сборка библиотеки 
maturin develop -m audio-lib/Cargo.toml

# запустить проект
poetry run bot-start 
```

## Про библиотеку для работы с аудио
Библиотека audio_lib используется для получения информации о видео и загрузки звуковых дорожек из видео. 
Эта библиотека была написана мной на языка Rust и может быть найдена в каталоге audio-lib.

Модули:
* audio_lib - предоставляет синхронный вариант функций
* audio_lib.asyncio - предоставляет асинхронный вариант функций

Функции:
```python3
def get_video_info(url: str) -> VideoInfo: ...
"""Предоставляет информацию о видео """

def download_audio(url: str, name: str) -> None: ...
"""Скачивает аудио-дорожку из видео"""
```

Классы:
```python
class VideoInfo:
    """Хранит информацию о видео"""
    id: str
    title: str
    duration: int
    is_live: bool
```