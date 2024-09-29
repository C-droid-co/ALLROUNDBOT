# Collect user feedback
@client.on(events.NewMessage(pattern='!feedback (.+)'))
async def collect_feedback(event):
    feedback_message = event.message.text.split(maxsplit=1)[1]
    user_id = event.sender_id
    # Code to save feedback in the database or file
    await event.respond("Thank you for your feedback!")
    # Optionally notify admins
    # admin_id = <your_admin_id>
    # await client.send_message(admin_id, f"User {user_id} submitted feedback: {feedback_message}")

# Show user feedback
@client.on(events.NewMessage(pattern='!showfeedback'))
async def show_feedback(event):
    # Code to retrieve feedback from the database or file
    feedback_list = []  # Replace with actual feedback retrieval logic
    if feedback_list:
        feedback_messages = "\n".join(feedback_list)
        await event.respond(f"User Feedback:\n{feedback_messages}")
    else:
        await event.respond("No feedback available.")
