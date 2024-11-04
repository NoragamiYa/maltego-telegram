from pyrogram import Client

import configparser
import asyncio
import os

class Config:
    def __init__(self, filename="config.ini"):
        self.config = configparser.ConfigParser()
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Config file '{filename}' not found.")
        self.config.read(filename)

    def get(self, section, key, fallback=None):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

config = Config()

api_id = int(config.get("telegram", "api_id", fallback=0))
api_hash = config.get("telegram", "api_hash", fallback="")
bot_token = config.get("telegram", "bot_token", fallback="")

app = Client("my_account", api_id, api_hash)
loop = asyncio.get_event_loop()