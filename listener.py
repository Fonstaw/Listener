import os
import logging
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read your credentials from environment
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_NAME = os.environ.get("SESSION_NAME", "anon")  # can be any string

# The channel you want to watch (use username without @)
CHANNEL = os.environ.get("CHANNEL")  # e.g. "mychannel" not "@mychannel"

# Create client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    # print everything you receive
    logger.info(f"Got message in chat_id={event.chat_id} username={getattr(event.chat, 'username', None)} "
                f"text={event.raw_text[:100]}")

    # if you want to only show your channel:
    if CHANNEL and getattr(event.chat, "username", None) == CHANNEL.lstrip("@"):
        logger.info(f"Matched your channel: {CHANNEL} text={event.raw_text[:100]}")

async def main():
    logger.info(f"Starting Telethon client. Watching channel={CHANNEL}")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())