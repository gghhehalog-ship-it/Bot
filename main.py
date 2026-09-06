import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ChatJoinRequestHandler,
    filters
)

# @BotFather-dan aldığınız YENİ tokeni yazın
TOKEN = "8986324306:AAH2Ny-kuiieCACGKYM2ZC7zs_9OWqioX_I"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start komandası
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Kanalımız 📢", url="https://t.me/telegram")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Salam! Mən kanal idarəetmə botuyam. Məni kanala admin təyin edin.",
        reply_markup=reply_markup
    )

# Kanala qatılma istəklərini avtomatik təsdiqləmə
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    await context.bot.approve_chat_join_request(
        chat_id=request.chat.id,
        user_id=request.from_user.id
    )
    # Yeni abunəçiyə özəl xoş gəldin mesajı göndərmək (ixtiyari)
    try:
        await context.bot.send_message(
            chat_id=request.from_user.id,
            text="Kanalımıza xoş gəldiniz! İstəyiniz avtomatik təsdiqləndi."
        )
    except Exception:
        pass  # İstifadəçi bota əvvəlcədən /start verməyibsə mesaj getməyə bilər

# Kanaldakı reklamsı/spam linkləri avtomatik silmə
async def clean_channel_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post or not update.channel_post.text:
        return
        
    text = update.channel_post.text
    if "http://" in text or "https://" in text or "t.me/" in text:
        await context.bot.delete_message(
            chat_id=update.channel_post.chat_id,
            message_id=update.channel_post.message_id
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers (İşləyicilər)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(auto_approve))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.TEXT, clean_channel_links))

    print("Bot işə düşdü...")
    app.run_polling()
