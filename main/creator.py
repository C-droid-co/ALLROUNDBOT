# Enable only creator commands
@client.on(events.NewMessage(pattern='!enable'))
async def enable_creator_commands(event):
    if event.sender_id == CREATOR_ID:  # Replace with the creator's user ID
        # Code to enable creator commands
        await event.respond("Creator commands have been enabled.")
    else:
        await event.respond("Only the creator can execute this command.")

# Disable only creator commands
@client.on(events.NewMessage(pattern='!disable'))
async def disable_creator_commands(event):
    if event.sender_id == CREATOR_ID:  # Replace with the creator's user ID
        # Code to disable creator commands
        await event.respond("Creator commands have been disabled.")
    else:
        await event.respond("Only the creator can execute this command.")
