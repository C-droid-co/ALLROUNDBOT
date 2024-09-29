from telethon import TelegramClient, events
from config import BOT_TOKEN
from database import add_user, get_user, remove_user

# Initialize the bot client
bot = TelegramClient('bot', api_id=YOUR_API_ID, api_hash=YOUR_API_HASH).start(bot_token=BOT_TOKEN)

# /start command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    sender = await event.get_sender()
    user_id = sender.id
    user_data = {"user_id": user_id, "username": sender.username}
    
    # Add user to database
    add_user(user_id, user_data)
    
    await event.respond(f"Hello {sender.username}, welcome to the bot!")
    
# /help command
@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    help_text = """
    Available Commands:
    /start - Start the bot
    /help - Display this help message
    /welcome - Set welcome message
    /lock - Lock group content
    /filter - Add filter words
    """
    await event.respond(help_text)
