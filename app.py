import os
import logging
import sqlite3
from telegram import Update, ForceReply
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
from flask import Flask, request  # Import Flask and request

# Initialize Flask app
app = Flask(__name__)  # This is your Flask app instance

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE = 'users.db'

def setup_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
    ''')
    conn.commit()
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
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (chat_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (user.id, user.username, user.first_name, user.last_name))
    conn.commit()
    conn.close()

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sorry, I didn't understand that command.")

@app.route('/webhook', methods=['POST'])  # Flask route for webhook
def webhook():
    update = Update.de_json(request.get_json(force=True), application)
    application.process_update(update)  # Process the incoming update
    return "OK", 200  # Respond to Telegram

def main() -> None:
    setup_database()

    # Create the application and pass it your bot's token
    global application  # Declare application as global to access in webhook
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Run the bot until you press Ctrl-C
    application.run_polling()

@app.route('/')  # Flask route
def home():
    return "Hello, World!"

if __name__ == '__main__':
    main()
