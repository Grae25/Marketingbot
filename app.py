from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TELEGRAM_TOKEN = '7715473023:AAFoUUmtIu-rOHShYF-BxRqVEnbBdlXcmzk'
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

# Define command handler functions
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Welcome to the bot!')

# Register command handlers
updater.dispatcher.add_handler(CommandHandler('start', start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the update from the webhook
    update = Update.de_json(request.get_json(force=True), updater.bot)
    # Process the update using the bot
    updater.dispatcher.process_update(update)
    return 'ok', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
