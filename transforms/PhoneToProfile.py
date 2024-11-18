from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from settings import app, loop, bot_token
from extensions import registry

from pyrogram.types import InputPhoneContact

from utils import fetch_user_info

import logging


async def fetch_profile_by_phone(phone: str):
    async with app:
        contacts = await app.import_contacts(
            [
                InputPhoneContact(phone, 'Foo')
            ]
        )
        if contacts.users:
            await app.delete_contacts(contacts.users[0].id)
            return await app.get_users(contacts.users[0].id)

    return


@registry.register_transform(display_name="To Telegram Profile", input_entity="maltego.PhoneNumber",
                             description="Finds a user's Telegram profile by phone number",
                             output_entities=["interlinked.telegram.UserProfile"])
class PhoneToProfile(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        phone = request.getProperty("phonenumber")
        profile = loop.run_until_complete(fetch_profile_by_phone(phone))

        if profile:
            if profile.username:
                profile_entity = response.addEntity("interlinked.telegram.UserProfile", value=profile.username)

                user_info = fetch_user_info(profile.username)
                profile_entity.addProperty("properties.photo", value=user_info["photo"])
            else:
                profile_entity = response.addEntity("interlinked.telegram.UserProfile", value=profile.id)

            profile_entity.addProperty("properties.id", value=profile.id)
            profile_entity.addProperty("properties.phone", value=phone)

            first_name = (profile.first_name.encode('cp1252', errors="ignore")).decode("cp1252")
            profile_entity.addProperty("properties.first_name", value=first_name)

            if profile.last_name:
                last_name = (profile.last_name.encode('cp1252', errors="ignore")).decode("cp1252")
                profile_entity.addProperty("properties.last_name", value=last_name)

            profile_entity.setLinkThickness(2)