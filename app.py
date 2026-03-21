from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from RAG.model import generate_answer
# from Vision.caption import process_image  <-- Moved to lazy load inside handle_image

import os
import uuid
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# -----------------------
# /start
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("🤖 Bot is live! Send text or image.")


# -----------------------
# /ask
# -----------------------
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    query = " ".join(context.args) if context.args else ""

    if not query:
        await update.message.reply_text("Please provide a question.")
        return

    try:
        res_dict, sources = generate_answer(query)
        
        answer = res_dict.get("answer", "No answer found.")
        conf = res_dict.get("confidence", 0)
        cat = res_dict.get("category", "General")

        # Memory indicator
        prefix = "💾 [FROM MEMORY]\n\n" if not sources else ""
        
        response = f"{prefix}🤖 *Answer*:\n{answer}\n\n"
        response += f"📊 *Confidence*: {conf*100:.0f}%\n"
        response += f"🏷️ *Category*: {cat}\n\n"

        if sources:
            response += "📚 *Sources*:\n"
            for s in sources[:2]:
                response += f"- {s.get('source', 'Unknown')}\n"

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# -----------------------
# Handle text
# -----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    query = update.message.text

    try:
        res_dict, sources = generate_answer(query)
        
        answer = res_dict.get("answer", "No answer found.")
        conf = res_dict.get("confidence", 0)
        cat = res_dict.get("category", "General")

        prefix = "💾 [FROM MEMORY]\n\n" if not sources else ""
        
        response = f"{prefix}🤖 *Answer*:\n{answer}\n\n"
        response += f"📊 *Confidence*: {conf*100:.0f}%\n"
        response += f"🏷️ *Category*: {cat}\n\n"

        if sources:
            response += "📚 *Sources*:\n"
            for s in sources[:2]:
                response += f"- {s.get('source', 'Unknown')}\n"

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# -----------------------
# 🔥 Handle image input (Python 3.14 safe)
# -----------------------
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    image_path = None

    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # ✅ Unique filename (fixes overwrite + concurrency issues)
        image_path = f"temp_{uuid.uuid4().hex}.jpg"

        # ✅ Correct async download (v20+ compatible)
        await file.download_to_drive(custom_path=image_path)

        # Step 1: OCR / Caption
        try:
            from Vision.caption import process_image
            result = process_image(image_path)
        except Exception as vision_err:
            if "WinError 1114" in str(vision_err) or "torch" in str(vision_err).lower():
                await update.message.reply_text(
                    "❌ Vision feature is currently unavailable on Python 3.14 due to a PyTorch DLL error.\n"
                    "Please wait for official support or use Python 3.12."
                )
            else:
                await update.message.reply_text(f"Vision Error: {str(vision_err)}")
            return

        query = result.get("output", "")

        if not query:
            await update.message.reply_text("Could not understand the image.")
            return

        # Step 2: Send to RAG
        res_dict, sources = generate_answer(query)

        # Step 3: Build response
        answer = res_dict.get("answer", "No answer found.")
        conf = res_dict.get("confidence", 0)
        cat = res_dict.get("category", "General")

        prefix = "💾 [FROM MEMORY]\n\n" if not sources else ""

        response = f"🧠 *Detected ({result.get('type')})*:\n{query}\n\n"
        response += f"{prefix}🤖 *Answer*:\n{answer}\n\n"
        response += f"📊 *Confidence*: {conf*100:.0f}%\n"
        response += f"🏷️ *Category*: {cat}\n\n"

        if sources:
            response += "📚 *Sources*:\n"
            for s in sources[:2]:
                response += f"- {s.get('metadata', {}).get('source', 'Unknown')}\n"

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

    finally:
        # ✅ Safe cleanup (Python 3.14 safe)
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass


# -----------------------
# Main
# -----------------------
def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is missing in the environment.")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))

    # 🔥 Order matters
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()