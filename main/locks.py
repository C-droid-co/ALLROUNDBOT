from telethon import events

@client.on(events.NewMessage(pattern='/lock'))
async def lock_group(event):
    user_id = event.sender_id
    group_id = event.chat_id
    
    # Check if user is an admin
    if event.is_group and await event.get_sender() in event.chat.admins:
        set_group_lock(group_id, True)
        await event.respond("The group has been locked. Only admins can send messages.")
    else:
        await event.respond("You don't have permission to lock the group.")

@client.on(events.NewMessage(pattern='/unlock'))
async def unlock_group(event):
    user_id = event.sender_id
    group_id = event.chat_id
    
    # Check if user is an admin
    if event.is_group and await event.get_sender() in event.chat.admins:
        set_group_lock(group_id, False)
        await event.respond("The group has been unlocked. Everyone can send messages.")
    else:
        await event.respond("You don't have permission to unlock the group.")

@client.on(events.NewMessage)
async def restrict_messages(event):
    group_id = event.chat_id
    
    if get_group_lock(group_id):
        # Check if the user is an admin
        if event.sender_id not in [admin.user_id for admin in await event.get_chat().get_admins()]:
            await event.delete()  # Delete the message
            await event.respond("The group is locked. Only admins can send messages.")


# Dictionary to store lock statuses
locks = {
    "voice": False,
    "audio": False,
    "image": False,
    "film": False,
    "file": False,
    "contact": False,
    "game": False,
    "location": False,
    "sticker": False,
    "gif": False,
    "forward": False,
    "link": False,
    "site": False,
    "@": False,
    "welcome": False,
    "user_left_message": False,
    "join_message": False,
    "add_user_message": False,
    "bot": False,
    "delete_welcome": False,
    "warn": False,
    "poll": False,
    "inline_button": False,
    "robot_command": False,
    "chat": False,
    "hashtag": False,
}

@client.on(events.NewMessage(pattern='/lock (.*)'))
async def lock_content(event):
    content_type = event.pattern_match.group(1).strip()
    if content_type in locks:
        locks[content_type] = True
        await event.respond(f"{content_type.capitalize()} locked.")
    else:
        await event.respond("Invalid content type.")

@client.on(events.NewMessage(pattern='/unlock (.*)'))
async def unlock_content(event):
    content_type = event.pattern_match.group(1).strip()
    if content_type in locks:
        locks[content_type] = False
        await event.respond(f"{content_type.capitalize()} unlocked.")
    else:
        await event.respond("Invalid content type.")
