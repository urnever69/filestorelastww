from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN = int(os.environ.get("ADMIN"))
CHANNEL = int(os.environ.get("CHANNEL"))

app = Client("file_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply("Send me a file and I will save it in the channel. Only admin can upload files.")

@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def handle_file(client, message):
    if message.from_user.id != ADMIN:
        return await message.reply("🚫 Only the admin can upload files.")

    sent = await message.forward(CHANNEL)
    link = f"https://t.me/c/{str(CHANNEL)[4:]}/{sent.message_id}"

    await message.reply_text(
        f"✅ File Saved!
🔗 Link: {link}

⚠️ Link will expire in 50 minutes.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open File", url=link)]])
    )

    await asyncio.sleep(3000)  # 50 minutes
    try:
        await client.delete_messages(CHANNEL, sent.message_id)
    except:
        pass

app.run()