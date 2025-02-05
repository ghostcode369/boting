
# Replace with your actual Telegram Bot Token from BotFather
# API_TOKEN = 'YOUR_BOT_API_TOKEN'
# API_TOKEN = '7773653937:AAFrGnpGw-2LZ6WI1KZwKMhCKgl4XfWtcpw'
# python bot/reminder_bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import asyncio
import nest_asyncio

# Apply nest_asyncio to fix the event loop issue
nest_asyncio.apply()

# Your API Token
API_TOKEN = '7773653937:AAFrGnpGw-2LZ6WI1KZwKMhCKgl4XfWtcpw'

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# List to store reminders
reminders = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with instructions."""
    await update.message.reply_text(
        "Hello! I am your Reminder Bot. Use /setreminder <date> <time> <message> to set reminders.\n"
        "For example: /setreminder 2025-02-06 10:00 MeetingWithTeam"
    )

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parse the input and store a reminder."""
    try:
        reminder_time_str = " ".join(context.args[:-1])
        message = context.args[-1]
        reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
        local_timezone = pytz.timezone("Africa/Addis_Ababa")
        reminder_time = local_timezone.localize(reminder_time)

        reminders.append({
            "time": reminder_time,
            "message": message,
            "chat_id": update.message.chat_id
        })

        await update.message.reply_text(
            f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')} to: {message}"
        )
    except Exception as e:
        await update.message.reply_text(
            "Error setting reminder. Please use the format: /setreminder <YYYY-MM-DD HH:MM> <message>"
        )
        logger.error(f"Error: {e}")

async def view_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the list of reminders."""
    if not reminders:
        await update.message.reply_text("You have no reminders set.")
        return

    reminder_list = "\n".join(
        [f"{reminder['time'].strftime('%Y-%m-%d %H:%M')}: {reminder['message']}" for reminder in reminders]
    )
    await update.message.reply_text(f"Your reminders:\n{reminder_list}")

def send_reminders(application: Application):
    """Check reminders and send any that are due."""
    current_time = datetime.now(pytz.timezone("Africa/Addis_Ababa"))
    for reminder in reminders[:]:
        if reminder['time'] <= current_time:
            application.bot.send_message(
                chat_id=reminder['chat_id'],
                text=f"Reminder: {reminder['message']}"
            )
            reminders.remove(reminder)

async def main():
    # Create the Application with your bot token
    application = Application.builder().token(API_TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setreminder", set_reminder))
    application.add_handler(CommandHandler("viewreminders", view_reminders))

    # Set up a scheduler to check reminders every minute
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_reminders(application), 'interval', seconds=60)
    scheduler.start()

    # Start polling for updates from Telegram
    await application.run_polling()

if __name__ == '__main__':
    # Now use asyncio.run with nest_asyncio to allow it in a nested loop environment
    asyncio.run(main())
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parse the input and store a reminder."""
    try:
        # Ensure that there are enough arguments (date, time, message)
        if len(context.args) < 2:
            await update.message.reply_text(
                "Error: Please provide both date and time followed by the reminder message.\n"
                "Usage: /setreminder <YYYY-MM-DD HH:MM> <message>"
            )
            return
        
        reminder_time_str = " ".join(context.args[:-1])  # Combine date and time as one string
        message = context.args[-1]  # The last argument is the message

        # Try parsing the date and time from the string
        reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
        local_timezone = pytz.timezone("Africa/Addis_Ababa")
        reminder_time = local_timezone.localize(reminder_time)

        reminders.append({
            "time": reminder_time,
            "message": message,
            "chat_id": update.message.chat_id
        })

        await update.message.reply_text(
            f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')} to: {message}"
        )
    except Exception as e:
        await update.message.reply_text(
            "Error: Invalid input format. Please use the format: /setreminder <YYYY-MM-DD HH:MM> <message>"
        )
        logger.error(f"Error: {e}")
