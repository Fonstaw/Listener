import os
import re
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ------------------ CONFIG ------------------ #
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNELS = os.environ.get("CHANNELS", "").split(",")

# Clean channel names (remove @ and extra spaces)
CHANNELS = [ch.strip().lstrip("@") for ch in CHANNELS if ch.strip()]

# ------------------ LOGGING ------------------ #
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ------------------ TELETHON CLIENT ------------------ #
tele_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ------------------ TRADE FUNCTION ------------------ #
# Placeholder buy_token function
async def buy_token(token):
    logger.info(f"Executing trade logic for token: {token}")
    # Your existing buy logic goes here

# ------------------ TELETHON LISTENER ------------------ #
@tele_client.on(events.NewMessage(chats=CHANNELS))
async def new_message(event):
    msg = event.message.message
    chat_name = event.chat.username if event.chat else "unknown"
    logger.info(f"New message in {chat_name}: {msg}")

    # Detect token pattern
    token_pattern = r'[1-9A-HJ-NP-Za-km-z]{44}'
    tokens = re.findall(token_pattern, msg)
    for token in tokens:
        base58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        if len(token) == 44 and all(c in base58_chars for c in token):
            logger.info(f"Detected token {token} in {chat_name}")
            await buy_token(token)

# ------------------ MAIN EXECUTION ------------------ #
async def main():
    await tele_client.start()
    logger.info("Telethon client started and listening to channels: %s", CHANNELS)
    await tele_client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
