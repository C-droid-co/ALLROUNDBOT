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
