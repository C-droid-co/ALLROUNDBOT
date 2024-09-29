from telethon import events
from db.mongo import set_welcome_message, get_welcome_message, toggle_welcome

# Command to set a welcome message
@client.on(events.NewMessage(pattern='/welcome'))
async def set_welcome(event):
    # Ensure the user is an admin
    if not await event.get_sender().is_admin:
        await event.respond("You must be an admin to set a welcome message.")
        return
    
    message = event.message.message.split(maxsplit=1)
    if len(message) < 2:
        await event.respond("Please provide a welcome message. Example: /welcome Welcome to the group!")
        return

    welcome_message = message[1]
    group_id = event.chat_id

    # Save the welcome message to MongoDB
    if set_welcome_message(group_id, welcome_message):
        await event.respond(f"Welcome message set to: {welcome_message}")
    else:
        await event.respond("Error setting the welcome message. Try again.")

# Command to toggle the welcome message on or off
@client.on(events.NewMessage(pattern='/toggle_welcome'))
async def toggle_welcome_status(event):
    # Ensure the user is an admin
    if not await event.get_sender().is_admin:
        await event.respond("You must be an admin to toggle the welcome message.")
        return
    
    group_id = event.chat_id
    _, is_enabled = get_welcome_message(group_id)

    # Toggle the welcome message status
    new_status = not is_enabled
    if toggle_welcome(group_id, new_status):
        status = "enabled" if new_status else "disabled"
        await event.respond(f"Welcome messages are now {status}.")
    else:
        await event.respond("Error toggling the welcome message status. Try again.")


# Listener for new users joining the group
@client.on(events.ChatAction)
async def on_user_join(event):
    if event.user_added or event.user_joined:
        group_id = event.chat_id
        welcome_message, is_enabled = get_welcome_message(group_id)
        
        # If welcome messages are enabled, send the welcome message
        if is_enabled and welcome_message:
            for user in event.users:
                await client.send_message(event.chat_id, f"{welcome_message} {user.first_name}")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id
        
        # Fetch the welcome message (you can customize this)
        welcome_message = f"Welcome {new_member.first_name}! Please read the group rules and enjoy your stay!"

        await event.respond(welcome_message)


# Initialize a variable to hold the custom welcome message
custom_welcome_message = "Welcome to the group!"

@client.on(events.NewMessage(pattern='/set_welcome'))
async def set_welcome(event):
    global custom_welcome_message
    new_message = event.message.message.split(' ', 1)
    if len(new_message) < 2:
        await event.respond("Please provide a welcome message.")
        return
    custom_welcome_message = new_message[1]
    await event.respond(f"Custom welcome message set to: {custom_welcome_message}")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id
        
        # Use the custom welcome message
        welcome_message = custom_welcome_message.replace('!name', new_member.first_name)

        await event.respond(welcome_message)

# Initialize variables for the welcome button
welcome_button_active = False
welcome_button_url = ""

@client.on(events.NewMessage(pattern='/welcome_btn'))
async def set_welcome_button(event):
    global welcome_button_active, welcome_button_url
    command = event.message.message.split(' ', 2)
    
    if len(command) < 3:
        await event.respond("Please provide a command (add/remove) and a URL.")
        return
    
    action = command[1]
    
    if action == '++':
        welcome_button_url = command[2]
        welcome_button_active = True
        await event.respond(f"Welcome button activated with URL: {welcome_button_url}")
    elif action == '--':
        welcome_button_active = False
        welcome_button_url = ""
        await event.respond("Welcome button deactivated.")
    else:
        await event.respond("Invalid action. Use '++' to activate or '--' to deactivate.")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id
        
        # Use the custom welcome message
        welcome_message = custom_welcome_message.replace('!name', new_member.first_name)

        if welcome_button_active:
            buttons = [[Button.url("Join Now", welcome_button_url)]]
            await event.respond(welcome_message, buttons=buttons)
        else:
            await event.respond(welcome_message)


import asyncio

# Initialize auto-delete variable
auto_delete_welcome = True

@client.on(events.NewMessage(pattern='/open_Deletewelcome'))
async def activate_auto_delete(event):
    global auto_delete_welcome
    auto_delete_welcome = True
    await event.respond("Auto delete for welcome messages activated.")

@client.on(events.NewMessage(pattern='/lock_Deletewelcome'))
async def deactivate_auto_delete(event):
    global auto_delete_welcome
    auto_delete_welcome = False
    await event.respond("Auto delete for welcome messages deactivated.")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id
        
        # Use the custom welcome message
        welcome_message = custom_welcome_message.replace('!name', new_member.first_name)
        message = await event.respond(welcome_message)
        
        if auto_delete_welcome:
            # Wait for 10 seconds (or your desired duration) and delete the message
            await asyncio.sleep(10)  # Change the number to your desired time in seconds
            await message.delete()

from datetime import datetime

# Initialize show_time_and_date variable
show_time_and_date = True

@client.on(events.NewMessage(pattern='/open Welcome date'))
async def activate_show_time(event):
    global show_time_and_date
    show_time_and_date = True
    await event.respond("Time and date will now be shown in welcome messages.")

@client.on(events.NewMessage(pattern='/lock Welcome date'))
async def deactivate_show_time(event):
    global show_time_and_date
    show_time_and_date = False
    await event.respond("Time and date will no longer be shown in welcome messages.")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id
        
        # Use the custom welcome message
        welcome_message = custom_welcome_message.replace('!name', new_member.first_name)
        
        # Check if time and date should be shown
        if show_time_and_date:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            welcome_message += f"\nCurrent Time: {current_time}"
        
        message = await event.respond(welcome_message)
        
        if auto_delete_welcome:
            await asyncio.sleep(10)  # Change the number to your desired time in seconds
            await message.delete()


import random

# Initialize a list to hold random welcome messages
random_welcome_messages = []

@client.on(events.NewMessage(pattern='/random_welcome (.+)'))
async def add_random_welcome(event):
    message = event.pattern_match.group(1)
    random_welcome_messages.append(message)
    await event.respond(f"Added random welcome message: {message}")

@client.on(events.NewMessage(pattern='!!random_welcome'))
async def clear_random_welcome(event):
    random_welcome_messages.clear()
    await event.respond("Cleared all random welcome messages.")

@client.on(events.ChatAction)
async def welcome_new_members(event):
    if event.user_added or event.user_joined:
        new_member = event.users[0]
        group_id = event.chat_id

        # Determine which welcome message to use
        if random_welcome_messages:
            welcome_message = random.choice(random_welcome_messages).replace('!name', new_member.first_name)
        else:
            welcome_message = custom_welcome_message.replace('!name', new_member.first_name)

        # Check if time and date should be shown
        if show_time_and_date:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            welcome_message += f"\nCurrent Time: {current_time}"

        message = await event.respond(welcome_message)

        if auto_delete_welcome:
            await asyncio.sleep(10)  # Change the number to your desired time in seconds
            await message.delete()

from datetime import datetime

# Initialize a variable to control the time and date display
show_time_and_date = False

@client.on(events.NewMessage(pattern='/toggle_time_date'))
async def toggle_time_date(event):
    global show_time_and_date
    show_time_and_date = not show_time_and_date
    status = "enabled" if show_time_and_date else "disabled"
    await event.respond(f"Current time and date display is now {status}.")


# Initialize a list to store random welcome messages
random_welcome_messages = []

@client.on(events.NewMessage(pattern='/add_random_welcome (.+)'))
async def add_random_welcome(event):
    global random_welcome_messages
    message = event.pattern_match.group(1)
    random_welcome_messages.append(message)
    await event.respond(f"Added random welcome message: {message}")

@client.on(events.NewMessage(pattern='/clear_random_welcome'))
async def clear_random_welcome(event):
    global random_welcome_messages
    random_welcome_messages.clear()
    await event.respond("Cleared all random welcome messages.")

@client.on(events.NewMessage(pattern='/welcome_new_member'))
async def welcome_new_member(event):
    if random_welcome_messages:
        welcome_message = random.choice(random_welcome_messages)
        await event.respond(welcome_message)
    else:
        await event.respond("No welcome messages available.")

@client.on(events.NewMessage(pattern='/set_welcome_media'))
async def set_welcome_media(event):
    if event.message.reply_to:
        media = event.message.reply_to.media
        if media:
            await event.respond("Welcome media set successfully.")
            # Store media ID in the database or in memory
            # For simplicity, we can use a variable here
            global welcome_media
            welcome_media = media
        else:
            await event.respond("Please reply to the media you want to set as welcome.")
    else:
        await event.respond("Please reply to a media message.")

@client.on(events.NewMessage(pattern='/welcome_new_member'))
async def welcome_new_member(event):
    if random_welcome_messages:
        welcome_message = random.choice(random_welcome_messages)
        await event.respond(welcome_message)

        if welcome_media:
            await event.respond(welcome_media)
    else:
        await event.respond("No welcome messages available.")



# Variables for welcome and farewell messages
welcome_message = "Welcome to the group!"
farewell_message = "Goodbye! We'll miss you!"

@client.on(events.NewMessage(pattern='/set_welcome (.*)'))
async def set_welcome(event):
    global welcome_message
    welcome_message = event.pattern_match.group(1).strip()
    await event.respond("Welcome message updated!")

@client.on(events.NewMessage(pattern='/set_farewell (.*)'))
async def set_farewell(event):
    global farewell_message
    farewell_message = event.pattern_match.group(1).strip()
    await event.respond("Farewell message updated!")

@client.on(events.ChatAction)
async def welcome_or_farewell(event):
    if event.user_joined:
        await event.respond(welcome_message)
    elif event.user_left:
        await event.respond(farewell_message)

from telethon import events
from pymongo import MongoClient
from datetime import datetime

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with actual MongoDB URI
db = client['bot_database']  # Replace with your DB
welcome_col = db['welcome_messages']  # Collection for welcome messages

# Welcome message template
default_welcome_msg = "Hello !name, welcome!"

# Command: Activate welcome
@bot.on(events.NewMessage(pattern=r'!open welcome'))
async def activate_welcome(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"welcome_active": True}}, upsert=True)
    await event.reply("Welcome messages activated.")

# Command: Deactivate welcome
@bot.on(events.NewMessage(pattern=r'!lock welcome'))
async def deactivate_welcome(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"welcome_active": False}}, upsert=True)
    await event.reply("Welcome messages deactivated.")

# Command: Set custom welcome text
@bot.on(events.NewMessage(pattern=r'!welcome (.+)'))
async def set_welcome(event):
    custom_msg = event.pattern_match.group(1)
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"welcome_msg": custom_msg}}, upsert=True)
    await event.reply(f"Custom welcome message set: {custom_msg}")

# Command: Greet new members
@bot.on(events.ChatAction)
async def greet_new_member(event):
    if event.user_joined or event.user_added:
        welcome_data = welcome_col.find_one({"chat_id": event.chat_id})
        if welcome_data and welcome_data.get('welcome_active', False):
            welcome_msg = welcome_data.get('welcome_msg', default_welcome_msg)
            welcome_msg = welcome_msg.replace('!name', event.user.first_name)
            await event.reply(welcome_msg)

# Command: Add button to welcome text
@bot.on(events.NewMessage(pattern=r'!welcome_btn (.+)'))
async def add_welcome_button(event):
    url = event.pattern_match.group(1)
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"welcome_button": url}}, upsert=True)
    await event.reply(f"Button added to welcome message: {url}")

# Command: Delete welcome message after some time
@bot.on(events.NewMessage(pattern=r'!open Delete welcome'))
async def activate_auto_delete(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"auto_delete_welcome": True}}, upsert=True)
    await event.reply("Auto-delete welcome messages activated.")

@bot.on(events.NewMessage(pattern=r'!lock Delete welcome'))
async def deactivate_auto_delete(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"auto_delete_welcome": False}}, upsert=True)
    await event.reply("Auto-delete welcome messages deactivated.")

# Command: Show time and date in welcome message
@bot.on(events.NewMessage(pattern=r'!open Welcome date'))
async def activate_welcome_date(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"show_date": True}}, upsert=True)
    await event.reply("Date and time will be shown in welcome messages.")

@bot.on(events.NewMessage(pattern=r'!lock Welcome date'))
async def deactivate_welcome_date(event):
    welcome_col.update_one({"chat_id": event.chat_id}, {"$set": {"show_date": False}}, upsert=True)
    await event.reply("Date and time removed from welcome messages.")

from telethon import events
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['group_management']
welcome_collection = db['welcome_messages']

async def send_welcome(event):
    # Check if welcome is activated
    welcome_status = welcome_collection.find_one({"group_id": event.chat_id, "feature": "welcome_status"})
    if welcome_status and welcome_status['status'] == 'active':
        welcome_msg = welcome_collection.find_one({"group_id": event.chat_id, "feature": "welcome_text"})
        if welcome_msg:
            welcome_text = welcome_msg['text'].replace('!name', event.sender.first_name)
            await event.reply(welcome_text)

# Telethon event handler for new users
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined or event.user_added:
        await send_welcome(event)

# Command to activate/deactivate the welcome message
@client.on(events.NewMessage(pattern=r'!open welcome|!lock welcome'))
async def toggle_welcome(event):
    group_id = event.chat_id
    command = event.raw_text.strip()

    if command == '!open welcome':
        welcome_collection.update_one({"group_id": group_id, "feature": "welcome_status"}, {"$set": {"status": "active"}}, upsert=True)
        await event.respond('Welcome message activated.')
    elif command == '!lock welcome':
        welcome_collection.update_one({"group_id": group_id, "feature": "welcome_status"}, {"$set": {"status": "inactive"}}, upsert=True)
        await event.respond('Welcome message deactivated.')

# Command to set a custom welcome message
@client.on(events.NewMessage(pattern=r'!welcome '))
async def set_welcome(event):
    group_id = event.chat_id
    welcome_text = event.raw_text[len('!welcome '):]

    welcome_collection.update_one({"group_id": group_id, "feature": "welcome_text"}, {"$set": {"text": welcome_text}}, upsert=True)
    await event.respond(f"Custom welcome message set: {welcome_text}")

