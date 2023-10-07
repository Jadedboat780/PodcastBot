import pytest
import aiofiles.os as aos
from audio_lib import async_mod
import time


@pytest.mark.skip
@pytest.mark.asyncio
async def test_is_stream():
    url = "Вставте ссылку на стрим перед запуском теста"
    result = await async_mod.is_streaming(url)
    assert result == True


@pytest.mark.parametrize("url, name, acceptable_time",
                         [("https://www.youtube.com/watch?v=m-_N56RDBJw", "m-_N56RDBJw", 15),
                          ("https://www.youtube.com/watch?v=7ab5qqvCjOg", "7ab5qqvCjOg", 17)])
@pytest.mark.asyncio
async def test_speed_download(url, name, acceptable_time):
    start = time.perf_counter()
    await async_mod.download_audio(url, name)
    speed_time = time.perf_counter() - start
    await aos.unlink(f'{name}.opus')
    assert speed_time < acceptable_time


@pytest.mark.xfail(reason='Намеренный провал')
@pytest.mark.asyncio
async def test_wrong_url():
    await async_mod.download_audio("https://www.youtube.com/watch?v=dfdfg_dfvdi", "video1")
