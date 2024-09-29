from telethon import events

polls = {}

@client.on(events.NewMessage(pattern='/poll (.+)'))
async def create_poll(event):
    question, *options = event.pattern_match.group(1).split(';')
    options = [option.strip() for option in options]
    
    if len(options) < 2:
        await event.respond("You need to provide at least two options separated by a semicolon (;).")
        return

    poll_message = await event.respond(f"**Poll:** {question}\n" + "\n".join(f"{i + 1}. {option}" for i, option in enumerate(options)))
    
    for i in range(len(options)):
        await poll_message.reply(f"{i + 1}. {options[i]}")

    polls[poll_message.id] = {
        "question": question,
        "options": options,
        "votes": [0] * len(options)
    }

@client.on(events.NewMessage)
async def poll_vote(event):
    if event.reply_to_msg_id in polls:
        poll = polls[event.reply_to_msg_id]
        vote = event.raw_text.strip()

        if vote.isdigit() and 1 <= int(vote) <= len(poll['options']):
            poll['votes'][int(vote) - 1] += 1
            await event.respond(f"Vote for '{poll['options'][int(vote) - 1]}' counted!")
        else:
            await event.respond("Invalid vote. Please reply with the option number.")
