# -*- coding: utf-8 -*-
import requests, re, threading, os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- جزء السيرفر الوهمي لحل مشكلة Render ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Iptv24_Bot is Running!"

def run_flask():
    # Render يعطينا البورت تلقائياً في متغير البيئة PORT
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)
# -----------------------------------------

BOT_TOKEN = '8312066648:AAEWpmkMX6WG-wZt9pLQkKPhbRCULoMfQXk'
PHOTO_URL = 'https://telegra.ph/file/your_image_link.jpg' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⚡️ استخراج كود IPTV", callback_data='gen')],
                [InlineKeyboardButton("📖 دليل التشغيل", callback_data='help')]]
    
    welcome_text = "👋 **أهلاً بك في Iptv24_Bot الرسمي**\n━━━━━━━━━━━━━━\nاضغط للبدء 👇"
    
    try:
        await update.message.reply_photo(photo=PHOTO_URL, caption=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    except:
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'gen':
        await query.edit_message_caption(caption="🔄 **جاري سحب البيانات...**")
        # كود السحب هنا (نفس الكود السابق)
        # ...

if __name__ == '__main__':
    # تشغيل السيرفر الوهمي في خلفية الكود لإرضاء Render
    threading.Thread(target=run_flask).start()
    
    # تشغيل البوت
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling(drop_pending_updates=True)
