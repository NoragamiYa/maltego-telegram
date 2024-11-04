from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from settings import app, loop, bot_token
from extensions import registry

from pyrogram.enums import MessageEntityType

from utils import media_fetcher
import logging


async def fetch_emojis(username):
    emoji_sets = []
    current_batch = []

    async with app:
        async for message in app.get_chat_history(username):
            if message.entities:
                for entity in message.entities:
                    if (entity.type == MessageEntityType.CUSTOM_EMOJI) and hasattr(entity, "custom_emoji_id"):
                        custom_emoji_id = entity.custom_emoji_id

                        if custom_emoji_id not in current_batch:
                            current_batch.append(custom_emoji_id)

                            if len(current_batch) == 200:
                                emoji_info_list = await app.get_custom_emoji_stickers(custom_emoji_ids=current_batch)
                                emoji_sets.extend(emoji_info_list)
                                current_batch.clear()

        if current_batch:
            emoji_info_list = await app.get_custom_emoji_stickers(custom_emoji_ids=current_batch)
            emoji_sets.extend(emoji_info_list)

    emoji_sets = remove_duplicates(emoji_sets)

    return emoji_sets


def remove_duplicates(emoji_sets):
    seen_set_names = set()
    unique_emoji_sets = []

    for emoji in emoji_sets:
        if emoji.set_name not in seen_set_names:
            seen_set_names.add(emoji.set_name)
            unique_emoji_sets.append(emoji)

    return unique_emoji_sets


@registry.register_transform(display_name="To Emoji Sets", input_entity="interlinked.telegram.Channel",
                             description="Extracts all emoji sets from a Telegram channel",
                             output_entities=["interlinked.telegram.StickerSet"])
class ChannelToEmojiSet(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        username = request.getProperty("properties.channel")
        emoji_sets = loop.run_until_complete(fetch_emojis(username))

        for emoji_set in emoji_sets:
            emoji_entity = response.addEntity("interlinked.telegram.StickerSet", value=emoji_set.set_name)

            thumbnail = media_fetcher.get_media_preview_url(emoji_set.set_name, file_id=emoji_set.thumbs[0].file_id, media_type="emoji")
            emoji_entity.addProperty("properties.thumbnail", value=thumbnail)
            emoji_entity.addProperty("properties.title", value=emoji_set.set_name)

            emoji_entity.setLinkColor('0xFFAEC9')
            emoji_entity.setLinkThickness(2)
