import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from db.mongo import connect_mongo

# Load environment variables
load_dotenv()
api_id = os.getenv("API_ID")  # API ID from Telegram
api_hash = os.getenv("API_HASH")  # API Hash from Telegram
bot_token = os.getenv("BOT_TOKEN")  # Your bot token
mongo_uri = os.getenv("MONGO_URI")  # MongoDB URI

# Create bot instance
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# MongoDB connection
db = connect_mongo(mongo_uri)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome to Group Management Bot! Type /help to get a list of commands.")
    raise events.StopPropagation

@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    commands = """
    /start - Start the bot
    /help - List of commands
    /welcome - Set welcome message
    """
    await event.respond(commands)
    raise events.StopPropagation

if __name__ == '__main__':
    print("Bot is running...")
    client.run_until_disconnected()
