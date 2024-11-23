# Maltego Telegram

![preview.png](https://github.com/user-attachments/assets/5463e9a9-9db3-4b0d-a888-bd19f5190cac)

Maltego Transforms for working with Telegram.

Features:

- Getting Telegram profile by phone number
- Getting a linked Telegram channel group
- Getting a list of Telegram group administrators
- Getting a list of authors of a Telegram channel
- Collect all forwarded & similar channels by Channel
- Indexing of all stickers/emoji in Telegram channel
- Identification of the creator of a set of stickers/emoji

## How does it work?
![work.png](https://github.com/user-attachments/assets/d5ebb835-138f-4d4e-8b52-570dee9babb0)

Each Telegram user has their own UID.

Each sticker set that a user creates has its ID hidden in it.

To reveal it, my Transform executes the following algorithm:
1. Make an API request to get information about the sticker set
2. Take the value of the "ID" key from the response
3. Perform a binary shift by 32 to the right.

The resulting UID can be exchanged for a familiar login using the `@tgdb_bot` bot, and thus reveal the user's profile.

**The author of a channel who did not leave contacts can be de-anonymized. To do this, you need to scan his channel and find the sticker packs that he has ever created. My Transform for Maltego does this automatically.**

Find out more: [What's wrong with stickers in Telegram? Deanonymize anonymous channels in two clicks](https://hackernoon.com/whats-wrong-with-stickers-in-telegram-deanonymize-anonymous-channels-in-two-clicks)

## Installation

1. Clone the repository

```
git clone https://github.com/vognik/maltego-telegram
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Specify secrets in `config.ini`:
- `api_id` and `api_hash`: guide [https://core.telegram.org/api/obtaining_api_id](https://core.telegram.org/api/obtaining_api_id)
- `bot_token`: guide [https://core.telegram.org/bots/tutorial#obtain-your-bot-token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)

4. Log in to Telegram

```
python login.py
```

5. Generate Transforms Import File

```
python project.py
```

6. Import `entities.mtz` and `telegram.mtz` files using Import Config in Maltego
7. Check if they work: new Entities and Transforms should appear in Maltego

![imports.png](https://github.com/user-attachments/assets/e9ce7b6f-b14e-4239-83cd-2510ac3db9d5)


## Usage
Drag and drop an entity from the Entity Pallete, right-click and select the desired Transform.

https://github.com/user-attachments/assets/1fa23899-fd52-435f-830b-0df27cb65439
