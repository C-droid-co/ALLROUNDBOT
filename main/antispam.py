from telethon import events
from db.mongo import add_message_record, is_spamming

@client.on(events.NewMessage)
async def monitor_messages(event):
    user_id = event.sender_id
    group_id = event.chat_id
    
    if is_spamming(group_id, user_id):
        await event.respond("You are sending messages too quickly. Please slow down.")
        # Optional: Mute or kick the user
        await event.chat.kick(user_id)  # Uncomment this to kick the user
    else:
        add_message_record(group_id, user_id)
