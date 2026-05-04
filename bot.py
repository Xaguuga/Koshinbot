import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TOKEN")

# Check admin
async def is_admin(update: Update):
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in ["administrator", "creator"]

# Detect link
def has_link(text):
    return "http://" in text or "https://" in text or "t.me" in text

# Main function
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # Skip admins
    if await is_admin(update):
        return

    if has_link(update.message.text):
        try:
            await update.message.delete()
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Bot running...")
app.run_polling()
