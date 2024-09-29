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


from telethon import events

# Start a poll
@client.on(events.NewMessage(pattern='!poll (.+)'))
async def create_poll(event):
    poll_question = event.message.text.split(maxsplit=1)[1]
    # Code to save the poll question in the database or file
    await event.respond(f"Poll created: {poll_question}\nVote with !vote <option_number>")

# Vote in a poll
@client.on(events.NewMessage(pattern='!vote (\\d+)'))
async def vote(event):
    option_number = int(event.message.text.split()[1])
    user_id = event.sender_id
    # Code to save the vote in the database or file
    await event.respond(f"Vote recorded: Option {option_number}")

# Show poll results
@client.on(events.NewMessage(pattern='!pollresults'))
async def show_poll_results(event):
    # Code to retrieve poll results from the database or file
    poll_results = {}  # Replace with actual results retrieval logic
    if poll_results:
        results_message = "\n".join(f"Option {key}: {value} votes" for key, value in poll_results.items())
        await event.respond(f"Poll Results:\n{results_message}")
    else:
        await event.respond("No poll results available.")

# Command to create a poll
@client.on(events.NewMessage(pattern='!poll (.+)'))
async def create_poll(event):
    poll_data = event.message.text.split(maxsplit=1)[1]
    question, *options = poll_data.split(';')
    # Code to create a poll message with options
    options_message = "\n".join([f"{index + 1}. {option.strip()}" for index, option in enumerate(options)])
    poll_message = f"Poll: {question}\nOptions:\n{options_message}"
    await event.respond(poll_message)

# Command to vote in a poll
@client.on(events.NewMessage(pattern='!vote (\d+)'))
async def vote(event):
    vote_number = event.message.text.split(maxsplit=1)[1]
    # Code to save the vote in the database or file
    await event.respond(f"Vote registered: Option {vote_number}")
