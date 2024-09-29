from telethon import events


# Variables to track filter and bad words
filter_words = set()
bad_words = set()

@client.on(events.NewMessage(pattern='/filter (.*)'))
async def add_filter(event):
    word = event.pattern_match.group(1).strip()
    filter_words.add(word)
    await event.respond(f"Word '{word}' has been added to the filter list.")

@client.on(events.NewMessage(pattern='!!filter (.*)'))
async def remove_filter(event):
    word = event.pattern_match.group(1).strip()
    if word in filter_words:
        filter_words.remove(word)
        await event.respond(f"Word '{word}' has been removed from the filter list.")
    else:
        await event.respond(f"Word '{word}' is not in the filter list.")

@client.on(events.NewMessage(pattern='/badword (.*)'))
async def add_bad_word(event):
    word = event.pattern_match.group(1).strip()
    bad_words.add(word)
    await event.respond(f"Bad word '{word}' has been added to the list.")

@client.on(events.NewMessage(pattern='!!badword (.*)'))
async def remove_bad_word(event):
    word = event.pattern_match.group(1).strip()
    if word in bad_words:
        bad_words.remove(word)
        await event.respond(f"Bad word '{word}' has been removed from the list.")
    else:
        await event.respond(f"Bad word '{word}' is not in the list.")

@client.on(events.NewMessage)
async def filter_words_handler(event):
    for word in filter_words:
        if word in event.raw_text:
            await event.delete()  # Delete the message
            await event.respond(f"Your message contains a forbidden word: '{word}'")
            break

    for word in bad_words:
        if word in event.raw_text:
            await event.delete()  # Delete the message
            await event.respond(f"Your message contains a bad word: '{word}'")
            break
