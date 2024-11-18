# Maltego Telegram

![preview.png](https://github.com/user-attachments/assets/ecfa9540-8736-4d33-be6f-42334dbd409f)

Maltego module for working with Telegram.

Features:

- Indexing of all stickers/emoji in Telegram channel
- Identification of the creator of a set of stickers/emoji

Find out more: [What's wrong with stickers in Telegram? Deanonymize anonymous channels in two clicks](https://hackernoon.com/whats-wrong-with-stickers-in-telegram-deanonymize-anonymous-channels-in-two-clicks)

## How does it work?
![work.png](https://github.com/user-attachments/assets/d5ebb835-138f-4d4e-8b52-570dee9babb0)

Each Telegram user has their own UID.

Any sticker pack has its creator's UID hidden in it, which can be seen by any user.

To do this, follow the algorithm:
1. Make an API request to get information about the sticker pack
2. Take the value of the "ID" key from the response
3. Perform a binary shift by 32 to the right.

The resulting UID can be exchanged for a familiar login using the `@tgdb_bot` bot, and thus reveal the user's profile.

**The author of a channel who did not leave contacts can be de-anonymized. To do this, you need to scan his channel and find the sticker packs that he has ever created. And then use the algorithm above to get the real profile.**

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


## How to use as a Maltego transform
Drag and drop an entity from the Entity Pallete, right-click and select the desired Transform.

https://github.com/user-attachments/assets/1fa23899-fd52-435f-830b-0df27cb65439
