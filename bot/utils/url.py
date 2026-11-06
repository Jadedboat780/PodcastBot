from functools import lru_cache
from urllib.parse import parse_qs, urlparse


@lru_cache
def url_validation(url: str) -> str | None:
    """Checks the validity of the YouTube url"""
    url_parse = urlparse(url)

    if url_parse.netloc == "youtu.be":
        video_id = url_parse.path.replace("/", "")
        return video_id
    elif url_parse.netloc == "www.youtube.com" and url_parse.path == "/watch":
        query_params = parse_qs(url_parse.query)
        video_ids = query_params.get("v")
        return video_ids[0] if video_ids else None
    elif url_parse.netloc == "www.youtube.com" and "/live" in url_parse.path:
        video_id = url_parse.path.replace("/live/", "")
        return video_id
    else:
        return None
