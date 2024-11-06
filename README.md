# Maltego Telegram

![preview.png](https://github.com/user-attachments/assets/ecfa9540-8736-4d33-be6f-42334dbd409f)

Maltego module for working with Telegram.

Features:

- Indexing of all stickers/emoji in Telegram channel
- Identification of the creator of a set of stickers/emoji

Find out more: [What's wrong with stickers in Telegram? Deanonymize anonymous channels in two clicks](https://hackernoon.com/whats-wrong-with-stickers-in-telegram-deanonymize-anonymous-channels-in-two-clicks)

## Installation

1. Clone the repository

```
git clone https://github.com/vognik/maltego-telegram
```

2. Specify secrets in `config.ini`:
- `api_id` and `api_hash`: instructions [https://core.telegram.org/api/obtaining_api_id](https://core.telegram.org/api/obtaining_api_id)
- `bot_token`: instruction [https://core.telegram.org/bots/tutorial#obtain-your-bot-token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
3. Execute the commands

```
pip install -r requirements.txt
python project.py
python login.py
```

4. Import `entities.mtz` and `maltego.mtz` files using Import Config in Maltego
5. Check if they work: new entities and their associated Transforms should appear in Entity Palette.
