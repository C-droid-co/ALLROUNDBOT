# Show group link command
@client.on(events.NewMessage(pattern='/link'))
async def link(event):
    group_link = "https://t.me/YourGroupLink"  # Replace with your group link
    await event.respond(f"Group Link: {group_link}")

# Show rules command
@client.on(events.NewMessage(pattern='/rules'))
async def rules(event):
    group_rules = """1. Be respectful to others.
2. No spamming.
3. Follow the group theme.
4. No offensive language.
5. Have fun!"""
    await event.respond(f"Group Rules:\n{group_rules}")

# Notify admins command
@client.on(events.NewMessage(pattern='@admin'))
async def notify_admins(event):
    admins = await event.get_chat().get_admins()
    admin_ids = [admin.user_id for admin in admins]
    await event.respond("Admins notified!")  # You can customize this part to send a specific message to admins
