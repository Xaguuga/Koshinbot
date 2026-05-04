import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TOKEN")

MAX_WARNINGS = 3
user_warnings = {}

async def is_admin(update: Update):
    user_id = update.effective_user.id
    member = await update.effective_chat.get_member(user_id)
    return member.status in ["administrator", "creator"]

def has_link(text):
    return re.search(r"(https?://|t\.me/)", text)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # SKIP ADMINS
    if await is_admin(update):
        return

    if has_link(update.message.text):
        await update.message.delete()

        user_id = update.effective_user.id
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"⚠️ Link lama ogola!\nWarnings: {user_warnings[user_id]}/3"
        )

        if user_warnings[user_id] >= MAX_WARNINGS:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🚫 User waa la ban gareeyay!"
            )
            user_warnings[user_id] = 0

async def warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w = user_warnings.get(update.effective_user.id, 0)
    await update.message.reply_text(f"Warnings: {w}/3")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(CommandHandler("warnings", warnings))

print("Bot running...")
app.run_polling()
