import pytest
from re import sub

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

@pytest.mark.parametrize("url, url_id", [("https://www.youtube.com/watch?v=7n_8cOBpQrg", "7n_8cOBpQrg"),
                                         ("https://youtu.be/H8COfDh2cfo?si=LVHRZJawiVrAYOTq", "H8COfDh2cfo"),
                                         ("https://www.youtube.com/watch?v=1HtEPEn4-LY&list=PLlKID9PnOE5hCuNW8L-qxC12U7WPWG6YS&index=1", "1HtEPEn4-LY"),
                                        ("https://www.youtube.com/watch?v=3DNwWKObrsU&t=1858s", "3DNwWKObrsU")])
def test_pattern_url(url, url_id):
    result = pattern_url(url)
    assert result == url_id
