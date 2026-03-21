from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from RAG.model import generate_answer

import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is live! Use /ask <question>")


# /ask
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Please provide a question.")
        return

    try:
        answer, sources = generate_answer(query)

        response = f"{answer}\n\n📚 Sources:\n"
        for s in sources[:2]:
            response += f"- {s}\n"

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


from telegram.ext import MessageHandler, filters

# Handle regular text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    query = update.message.text

    try:
        answer, sources = generate_answer(query)

        response = f"{answer}\n\n📚 Sources:\n"
        for s in sources[:2]:
            response += f"- {s}\n"

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


def main():
    # Run bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()