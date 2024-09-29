# Activate warning system
@client.on(events.NewMessage(pattern='!open warn'))
async def activate_warning_system(event):
    # Code to activate the warning system
    await event.respond("Warning system has been activated.")

# Deactivate warning system
@client.on(events.NewMessage(pattern='!lock warn'))
async def deactivate_warning_system(event):
    # Code to deactivate the warning system
    await event.respond("Warning system has been deactivated.")

# Set the warning number
@client.on(events.NewMessage(pattern='!warn (\d+)'))
async def set_warning_number(event):
    if event.sender_id == CREATOR_ID:  # Replace with the creator's user ID
        warning_number = int(event.message.text.split()[1])
        # Code to set the warning threshold
        await event.respond(f"Warning threshold set to {warning_number}.")
    else:
        await event.respond("Only the creator can execute this command.")

# Manual warn to a user
@client.on(events.NewMessage(pattern='!warn (.+)'))
async def manual_warn_user(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id
        reason = event.message.text.split(maxsplit=1)[1]
        # Code to warn the user (e.g., update the database)
        await event.respond(f"User {user_id} has been warned for: {reason}.")
    else:
        await event.respond("Please reply to the user you want to warn.")

# Clear user alert
@client.on(events.NewMessage(pattern='!!warn'))
async def clear_user_warning(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id
        # Code to clear the user's warnings from the database
        await event.respond(f"Warnings for user {user_id} have been cleared.")
    else:
        await event.respond("Please reply to the user whose warnings you want to clear.")

# Empty warning list
@client.on(events.NewMessage(pattern='!!warn'))
async def empty_warning_list(event):
    # Code to empty the warning list
    await event.respond("All warnings have been removed.")
