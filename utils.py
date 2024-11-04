import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from settings import bot_token


def make_http_request(url, method="GET", params=None, retries=3, backoff_factor=0.3, timeout=10):
    try:
        session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

        try:
            response = session.request(method, url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except ValueError:
            return response.content

    except requests.RequestException as e:
        logging.error(f"HTTP request failed for {url}: {e}")
        return None


class MediaFetcher:
    def __init__(self):
        self.bot_token = bot_token
        self.base_url = "https://api.telegram.org"

    def get_media_file_id(self, name, media_type="sticker"):
        url = (
            f"{self.base_url}/bot{self.bot_token}/getStickerSet"
            if media_type == "sticker"
            else f"{self.base_url}/bot{self.bot_token}/getCustomEmojiStickers"
        )
        params = {"name": name} if media_type == "sticker" else {"custom_emoji_ids": [name]}
        response_data = make_http_request(url, params=params)

        if response_data:
            if media_type == "sticker":
                return response_data["result"]["stickers"][0]["thumbnail"].get("file_id")
            elif media_type == "emoji":
                return response_data["result"][0]["thumbnail"]
        return None

    def get_file_path(self, file_id):
        url = f"{self.base_url}/bot{self.bot_token}/getFile"
        params = {"file_id": file_id}
        response_data = make_http_request(url, params=params)
        return response_data["result"].get("file_path") if response_data else None

    def get_media_preview_url(self, name, file_id=None, media_type="sticker"):
        file_id = self.get_media_file_id(name, media_type=media_type) if file_id is None else file_id
        if file_id:
            file_path = self.get_file_path(file_id)
            return f"{self.base_url}/file/bot{self.bot_token}/{file_path}" if file_path else None
        return None


media_fetcher = MediaFetcher()