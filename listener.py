import os
import re
import logging
import asyncio
import threading
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ------------------ CONFIG ------------------ #
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
CHANNELS = os.environ.get("CHANNELS", "").split(",")

# ------------------ LOGGING ------------------ #
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ------------------ TELETHON CLIENT ------------------ #
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ------------------ FLASK SERVER ------------------ #
app_flask = Flask(__name__)

@app_flask.route("/")
def health_check():
    return "Listener running!", 200

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

# ------------------ TELEGRAM LISTENER ------------------ #
@client.on(events.NewMessage)
async def new_message(event):
    msg = event.message.message
    for channel in CHANNELS:
        if event.chat and getattr(event.chat, "username", "").lower() == channel.lower().strip():
            token_pattern = r"[1-9A-HJ-NP-Za-km-z]{44}"
            tokens = re.findall(token_pattern, msg)
            for token in tokens:
                logger.info(f"Detected token: {token} in channel: {channel}")

# ------------------ MAIN ------------------ #
if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()
    logger.info("Flask server started on port 10000")

    # Start Telethon client
    logger.info(f"Telethon client started and listening to channels: {CHANNELS}")
    client.start()
    client.run_until_disconnected()
