
import logging
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN = int(os.getenv("ADMIN"))
CHANNEL = int(os.getenv("CHANNEL"))

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

force_join = "your_force_join_channel"  # Optional: set your force-join channel username

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if force_join:
        try:
            user = await client.get_chat_member(force_join, message.from_user.id)
        except:
            return await message.reply(
                "🔐 Please join our channel to use this bot.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Join Channel", url=f"https://t.me/{force_join}")
                ]])
            )
    await message.reply("👋 Send me a file, and I’ll store it for 50 minutes!")

@app.on_message(filters.private & filters.document | filters.video | filters.photo)
async def save_file(client, message: Message):
    if message.from_user.id != ADMIN:
        return await message.reply("🚫 Only the admin can upload files.")

    try:
        sent = await client.copy_message(
            chat_id=CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        file_id = sent.id
        link = f"https://t.me/c/{str(CHANNEL)[4:]}/{file_id}"
        await message.reply(f"✅ File saved!
🔗 [Click here to access]({link})", disable_web_page_preview=True)

        # Schedule delete after 50 minutes
        asyncio.create_task(delete_file(client, CHANNEL, file_id))

    except Exception as e:
        logger.error(f"Error saving file: {e}")
        await message.reply("⚠️ Something went wrong!")

async def delete_file(client, channel_id, msg_id):
    await asyncio.sleep(3000)  # 50 minutes
    try:
        await client.delete_messages(channel_id, msg_id)
        logger.info(f"Auto-deleted file {msg_id} from {channel_id}")
    except Exception as e:
        logger.error(f"Failed to delete file: {e}")

app.run()
