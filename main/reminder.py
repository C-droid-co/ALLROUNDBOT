import asyncio
from datetime import datetime, timedelta

reminders = {}

@client.on(events.NewMessage(pattern='/remindme (.+) in (\d+) (seconds|minutes|hours|days)'))
async def set_reminder(event):
    message = event.pattern_match.group(1)
    time_amount = int(event.pattern_match.group(2))
    time_unit = event.pattern_match.group(3)

    time_mapping = {
        "seconds": timedelta(seconds=time_amount),
        "minutes": timedelta(minutes=time_amount),
        "hours": timedelta(hours=time_amount),
        "days": timedelta(days=time_amount)
    }

    if time_unit in time_mapping:
        reminder_time = datetime.now() + time_mapping[time_unit]
        reminder_id = event.message.id

        reminders[reminder_id] = (message, reminder_time)

        await event.respond(f"Reminder set for {message} in {time_amount} {time_unit}.")
        
        # Wait until the time is up
        await asyncio.sleep(time_mapping[time_unit].total_seconds())
        
        await event.respond(f"Reminder: {message}")

    else:
        await event.respond("Invalid time unit. Use seconds, minutes, hours, or days.")


from datetime import datetime, timedelta
import asyncio

reminders = {}

# Command to set a reminder
@client.on(events.NewMessage(pattern='!remindme (\d+) (.+)'))
async def set_reminder(event):
    time_in_minutes = int(event.message.text.split()[1])
    reminder_text = event.message.text.split(maxsplit=2)[2]
    reminder_time = datetime.now() + timedelta(minutes=time_in_minutes)
    
    # Store the reminder
    reminders[event.sender_id] = (reminder_time, reminder_text)
    
    await event.respond(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Wait until the reminder time
    await asyncio.sleep(time_in_minutes * 60)
    if event.sender_id in reminders:
        await event.respond(f"Reminder: {reminder_text}")
        del reminders[event.sender_id]  # Remove the reminder after notifying
