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