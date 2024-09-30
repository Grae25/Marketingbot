from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Channel URL and ID
CHANNEL_URL = "https://t.me/KlonkarteundFalschgeldzumVerkauf"
YOUR_CHAT_ID = -1002264086096  # Replace with your actual channel ID

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

# Main function to set up the bot and schedule messages
def main():
    app = ApplicationBuilder().token('8059136622:AAEm1qo2-ph3sNjPr-2xG99gzdSYpFtWYJU').read_timeout(10).write_timeout(10).build()  # Increase timeout
    
    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    
    # JobQueue for scheduled messages
    job_queue = app.job_queue
    job_queue.run_repeating(scheduled_promotion_1, interval=3600, first=10)  # Every 1 hour
    job_queue.run_repeating(scheduled_promotion_2, interval=7200, first=30)  # Every 2 hours
    job_queue.run_repeating(scheduled_promotion_3, interval=10800, first=60)  # Every 3 hours
    
    # Start polling for updates
    app.run_polling()

if __name__ == '__main__':
    main()
