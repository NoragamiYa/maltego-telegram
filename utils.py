import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from maltego_trx.maltego import MaltegoEntity

from lxml import html

from settings import bot_token


def message_is_forwarded_from_another_chat(message, username):
    if hasattr(message, "forward_from_chat") \
        and message.forward_from_chat is not None \
            and message.forward_from_chat.username != username:
                return True

    return False


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


def fetch_web_info(username):
    photo = None
    full_name = None

    response_data = make_http_request(f"https://t.me/{username}")
    tree = html.fromstring(response_data)

    images = tree.cssselect("img.tgme_page_photo_image")
    if images:
        photo = images[0].get("src")
    
    title = tree.cssselect('.tgme_page_title span')
    if title:
        full_name = title[0].text_content()
    
    return {"full_name": full_name, "photo": photo}


def process_profile_entity(profile):
    if profile.username:
        profile_entity = MaltegoEntity("interlinked.telegram.UserProfile", value=profile.username)
        user_info = fetch_web_info(profile.username)
        profile_entity.addProperty("properties.photo", value=user_info["photo"])
    else:
        profile_entity = response.addEntity("interlinked.telegram.UserProfile", value=profile.id)

    profile_entity.addProperty("properties.id", value=profile.id)

    if profile.phone_number:
        profile_entity.addProperty("properties.phone", value=profile.phone_number)

    profile_entity.addProperty("properties.first_name", value=profile.first_name)

    if profile.last_name:
        profile_entity.addProperty("properties.last_name", value=profile.last_name)

    return profile_entity


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