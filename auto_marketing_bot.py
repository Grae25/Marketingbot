from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CommandHandler
import os

# Channel URL and ID
CHANNEL_URL = "https://t.me/+C8R6wRn_VCBlZDZi"
YOUR_CHAT_ID = -1002264086096  # Replace with your actual channel ID

# Initialize Flask app
app = Flask(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen! Ich bin hier, um Ihren Kanal zu leiten!")

# Function for scheduled promotions
async def scheduled_promotion_1(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID, 
        text=f"🎉 Vergessen Sie nicht, Ihre Freunde einzuladen, um exklusive Vorteile zu erhalten! Treten Sie unserem Kanal bei: {CHANNEL_URL}"
    )

async def scheduled_promotion_2(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID, 
        text=f"🎁 Nehmen Sie an unserem Empfehlungsprogramm teil und gewinnen Sie Belohnungen! Laden Sie weitere Benutzer ein zu {CHANNEL_URL} und verdienen Sie ein exklusives Paket mit kostenloser Lieferung."
    )

async def scheduled_promotion_3(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID, 
        text=f"💬 Bleiben Sie dran! Wir veröffentlichen regelmäßig wertvolle Inhalte. Laden Sie andere ein, davon zu profitieren {CHANNEL_URL}."
    )

# Create the Telegram bot application
app_bot = ApplicationBuilder().token('7670904840:AAHF_YR2JkHkhMWidKL_8j0EjR8E33BSaZY').build()

# Command Handlers
app_bot.add_handler(CommandHandler("start", start))

# JobQueue for scheduled messages
job_queue = app_bot.job_queue
job_queue.run_repeating(scheduled_promotion_1, interval=3600, first=10)  # Every 1 hour
job_queue.run_repeating(scheduled_promotion_2, interval=7200, first=30)  # Every 2 hours
job_queue.run_repeating(scheduled_promotion_3, interval=10800, first=60)  # Every 3 hours

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_bot)
    app_bot.process_update(update)  # Process the incoming update
    return "OK", 200  # Respond to Telegram

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  # Start Flask app
