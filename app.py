import os
import logging
import sqlite3
from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
from flask import Flask, request
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Set to DEBUG for detailed logs
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE = 'users.db'

def setup_database():
    conn = sqlite3.connect(DATABASE)
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )''')
        conn.commit()
    finally:
        conn.close()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the bot!",
        reply_markup=ForceReply(selective=True),
    )
    # Save user to the database
    save_user(user)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

# Function to save user to the database
def save_user(user):
    conn = sqlite3.connect(DATABASE)
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (chat_id, username, first_name, last_name)
                          VALUES (?, ?, ?, ?)''', (user.id, user.username, user.first_name, user.last_name))
        conn.commit()
    finally:
        conn.close()

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sorry, I didn't understand that command.")

# Create the application and pass it your bot's token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7670904840:AAHF_YR2JkHkhMWidKL_8j0EjR8E33BSaZY')
application = ApplicationBuilder().token(TOKEN).build()

# Register command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

@app.route('/')  # Flask route
def home():
    return "Hello, World!"

@app.route('/webhook', methods=['POST'])  # Flask route for webhook
async def webhook():
    logger.debug("Received webhook request.")
    data = request.get_json(force=True)  # Get the JSON data
    logger.debug(f"Data received: {data}")

    try:
        # Process the update
        update = Update.de_json(data, application)
        await application.process_update(update)  # Use await to properly process the update
        return "OK", 200  # Respond to Telegram
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return "Bad Request", 400

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))  # Start Flask app
